"""Concurrent, cache-backed workspace indexing orchestration."""

from __future__ import annotations

import hashlib
import json
import os
import threading
import time
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path
from queue import Empty, Queue
from tempfile import NamedTemporaryFile
from typing import Any

from config.logger import get_logger
from workspace.dependency_graph import dependency_graph
from workspace.project_index import project_index
from workspace.semantic_indexer import semantic_indexer
from workspace.symbol_indexer import symbol_indexer
from workspace.workspace_manager import workspace_manager

logger = get_logger(__name__)


@dataclass(frozen=True, slots=True)
class FileFingerprint:
    """Stable file state used for incremental change detection."""

    modified_ns: int
    size: int
    digest: str


@dataclass(frozen=True, slots=True)
class IndexChange:
    """A source file addition, modification, or removal."""

    path: Path
    kind: str


@dataclass(frozen=True, slots=True)
class IndexReport:
    """Result of one workspace indexing transaction."""

    full: bool
    indexed: int
    deleted: int
    unchanged: int
    duration_seconds: float


class WorkspaceIndexer:
    """Coordinates project, symbol, dependency, and semantic indexes.

    The indexer owns the workspace file manifest.  It uses filesystem metadata
    as the fast path and hashes only files whose metadata changed, making it
    safe against timestamp-only changes while avoiding unnecessary reads.
    """

    CACHE_DIRECTORY = ".geeta"
    CACHE_FILENAME = "workspace-index.json"
    DEFAULT_EXTENSIONS = frozenset({".py", ".pyi", ".json", ".yaml", ".yml", ".md", ".txt", ".sql"})
    SOURCE_EXTENSIONS = frozenset({".py", ".pyi"})
    IGNORED_DIRECTORIES = frozenset({".git", ".geeta", ".idea", ".mypy_cache", ".pytest_cache", ".ruff_cache", ".tox", ".venv", "__pycache__", "build", "dist", "node_modules", "venv"})

    def __init__(
        self,
        *,
        workspace: Path | None = None,
        project: Any = project_index,
        symbols: Any = symbol_indexer,
        dependencies: Any = dependency_graph,
        semantic: Any = semantic_indexer,
        extensions: Iterable[str] | None = None,
        max_file_size: int = 2 * 1024 * 1024,
        debounce_seconds: float = 0.35,
    ) -> None:
        if max_file_size <= 0:
            raise ValueError("max_file_size must be positive")
        if debounce_seconds < 0:
            raise ValueError("debounce_seconds cannot be negative")
        self._workspace = workspace.resolve() if workspace else None
        self._project = project
        self._symbols = symbols
        self._dependencies = dependencies
        self._semantic = semantic
        self._extensions = frozenset(extension.lower() for extension in (extensions or self.DEFAULT_EXTENSIONS))
        self._max_file_size = max_file_size
        self._debounce_seconds = debounce_seconds
        self._manifest: dict[str, FileFingerprint] = {}
        self._lock = threading.RLock()
        self._queue: Queue[Path] = Queue()
        self._stop_event = threading.Event()
        self._wake_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._last_report: IndexReport | None = None
        self._load_cache()
        logger.info("Workspace Indexer initialized.")

    @property
    def workspace(self) -> Path | None:
        """Return the explicitly configured or currently open workspace."""
        return self._workspace or workspace_manager.workspace

    @property
    def running(self) -> bool:
        """Whether the background worker is active."""
        with self._lock:
            return self._thread is not None and self._thread.is_alive()

    def set_workspace(self, workspace: str | Path) -> None:
        """Switch indexing state to a workspace and load its persisted cache."""
        root = Path(workspace).resolve()
        if not root.is_dir():
            raise NotADirectoryError(root)
        with self._lock:
            self.stop()
            self._workspace = root
            self._manifest.clear()
            self._last_report = None
            self._load_cache()

    def full_index(self) -> IndexReport:
        """Build every downstream index and replace the cached manifest."""
        root = self._require_workspace()
        started = time.perf_counter()
        with self._lock:
            manifest = self._snapshot(root)
            files = [root / relative for relative in manifest]
            self._dependencies.build()
            self._symbols.build()
            self._semantic.build()
            self._project.build()
            self._manifest = manifest
            self._save_cache()
            self._last_report = IndexReport(True, len(files), 0, 0, time.perf_counter() - started)
        logger.info("Full workspace index completed: %d files in %.3fs", self._last_report.indexed, self._last_report.duration_seconds)
        return self._last_report

    def incremental_index(self) -> IndexReport:
        """Detect and apply workspace deltas without rebuilding unchanged files."""
        root = self._require_workspace()
        started = time.perf_counter()
        with self._lock:
            current = self._snapshot(root)
            changes = self._diff(current, root)
            for change in changes:
                self._apply_change(change)
            if changes:
                self._dependencies.build()
                self._project.refresh()
            self._manifest = current
            self._save_cache()
            indexed = sum(change.kind != "deleted" for change in changes)
            deleted = sum(change.kind == "deleted" for change in changes)
            self._last_report = IndexReport(False, indexed, deleted, len(current) - indexed, time.perf_counter() - started)
        if changes:
            logger.info("Incremental workspace index applied: %d indexed, %d deleted", indexed, deleted)
        return self._last_report

    def notify_change(self, path: str | Path) -> None:
        """Queue a filesystem notification; duplicate notifications are harmless."""
        candidate = Path(path).resolve()
        root = self.workspace
        if root is None or not self._is_candidate(candidate, root):
            return
        self._queue.put(candidate)
        self._wake_event.set()

    def start(self, interval_seconds: float = 5.0) -> None:
        """Start the bounded-latency background indexing worker."""
        if interval_seconds <= 0:
            raise ValueError("interval_seconds must be positive")
        self._require_workspace()
        with self._lock:
            if self.running:
                return
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._run, args=(interval_seconds,), daemon=True, name="WorkspaceIndexer")
            self._thread.start()
        logger.info("Workspace indexer background worker started.")

    def stop(self, timeout: float = 10.0) -> None:
        """Stop the worker and wait for its current indexing transaction."""
        with self._lock:
            thread = self._thread
            self._stop_event.set()
            self._wake_event.set()
        if thread is not None and thread is not threading.current_thread():
            thread.join(timeout=timeout)
        with self._lock:
            if thread is self._thread and (thread is None or not thread.is_alive()):
                self._thread = None

    def statistics(self) -> dict[str, Any]:
        """Return safe operational metrics for health checks and diagnostics."""
        with self._lock:
            return {
                "workspace": str(self.workspace) if self.workspace else None,
                "running": self.running,
                "tracked_files": len(self._manifest),
                "queued_notifications": self._queue.qsize(),
                "last_report": asdict(self._last_report) if self._last_report else None,
            }

    def _run(self, interval_seconds: float) -> None:
        while not self._stop_event.is_set():
            self._wake_event.wait(interval_seconds)
            self._wake_event.clear()
            if self._stop_event.is_set():
                break
            self._drain_notifications()
            if self._debounce_seconds:
                self._stop_event.wait(self._debounce_seconds)
            try:
                self.incremental_index()
            except (OSError, ValueError):
                logger.exception("Background workspace indexing failed.")

    def _drain_notifications(self) -> None:
        while True:
            try:
                self._queue.get_nowait()
            except Empty:
                return

    def _apply_change(self, change: IndexChange) -> None:
        if change.kind == "deleted":
            self._symbols.remove_file(change.path)
            self._semantic.remove_file(change.path)
            return
        if change.path.suffix.lower() in self.SOURCE_EXTENSIONS:
            self._symbols.reindex_file(change.path)
        if change.path.suffix.lower() in self.SOURCE_EXTENSIONS:
            self._semantic.reindex_file(change.path)

    def _diff(self, current: dict[str, FileFingerprint], root: Path) -> list[IndexChange]:
        changes: list[IndexChange] = []
        for relative, fingerprint in current.items():
            previous = self._manifest.get(relative)
            if previous != fingerprint:
                changes.append(IndexChange(root / relative, "created" if previous is None else "modified"))
        changes.extend(IndexChange(root / relative, "deleted") for relative in self._manifest.keys() - current.keys())
        return sorted(changes, key=lambda change: str(change.path))

    def _iter_files(self, root: Path) -> Iterable[Path]:
        for directory, names, files in os.walk(root):
            names[:] = [name for name in names if name not in self.IGNORED_DIRECTORIES]
            base = Path(directory)
            for name in files:
                path = base / name
                if self._is_indexable(path, root):
                    yield path

    def _snapshot(self, root: Path) -> dict[str, FileFingerprint]:
        """Capture a manifest while tolerating concurrent file replacement."""
        snapshot: dict[str, FileFingerprint] = {}
        for path in self._iter_files(root):
            try:
                snapshot[self._relative(path, root)] = self._fingerprint(path)
            except OSError:
                logger.debug("File changed while scanning and will be retried: %s", path)
        return snapshot

    def _is_candidate(self, path: Path, root: Path) -> bool:
        """Check event-path eligibility without requiring the file to exist."""
        try:
            relative = path.relative_to(root.resolve())
            return not any(part in self.IGNORED_DIRECTORIES for part in relative.parts) and path.suffix.lower() in self._extensions
        except ValueError:
            return False

    def _is_indexable(self, path: Path, root: Path) -> bool:
        try:
            return self._is_candidate(path.resolve(), root) and path.is_file() and path.stat().st_size <= self._max_file_size
        except (OSError, ValueError):
            return False

    @staticmethod
    def _fingerprint(path: Path) -> FileFingerprint:
        stat = path.stat()
        digest = hashlib.blake2b(path.read_bytes(), digest_size=16).hexdigest()
        return FileFingerprint(stat.st_mtime_ns, stat.st_size, digest)

    @staticmethod
    def _relative(path: Path, root: Path) -> str:
        return path.relative_to(root).as_posix()

    def _require_workspace(self) -> Path:
        root = self.workspace
        if root is None or not root.is_dir():
            raise RuntimeError("A workspace must be open before indexing")
        return root.resolve()

    def _cache_path(self) -> Path | None:
        root = self.workspace
        return root / self.CACHE_DIRECTORY / self.CACHE_FILENAME if root else None

    def _load_cache(self) -> None:
        path = self._cache_path()
        if path is None or not path.is_file():
            return
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            self._manifest = {name: FileFingerprint(**value) for name, value in data.get("manifest", {}).items()}
        except (OSError, ValueError, TypeError):
            logger.warning("Ignoring invalid workspace index cache: %s", path)
            self._manifest = {}

    def _save_cache(self) -> None:
        path = self._cache_path()
        if path is None:
            return
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            payload = json.dumps({"version": 1, "manifest": {name: asdict(value) for name, value in self._manifest.items()}}, sort_keys=True, separators=(",", ":"))
            with NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
                handle.write(payload)
                temporary = Path(handle.name)
            temporary.replace(path)
        except OSError:
            logger.exception("Unable to persist workspace index cache: %s", path)


workspace_indexer = WorkspaceIndexer()

__all__ = ["FileFingerprint", "IndexChange", "IndexReport", "WorkspaceIndexer", "workspace_indexer"]
