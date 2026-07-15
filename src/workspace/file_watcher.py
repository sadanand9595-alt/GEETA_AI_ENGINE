"""
==============================================================================
GEETA AI Engine

File        : file_watcher.py
Package     : workspace
Description : File Watcher

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from watchdog.events import (
    FileSystemEvent,
    FileSystemEventHandler,
)
from watchdog.observers import Observer

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# File Watcher
###############################################################################


class WorkspaceEventHandler(FileSystemEventHandler):
    """
    Handles filesystem events.
    """

    def __init__(
        self,
        callback: Callable[[FileSystemEvent], None],
    ) -> None:

        super().__init__()

        self._callback = callback

    ###########################################################################

    def on_created(
        self,
        event: FileSystemEvent,
    ) -> None:

        self._callback(event)

    ###########################################################################

    def on_modified(
        self,
        event: FileSystemEvent,
    ) -> None:

        self._callback(event)

    ###########################################################################

    def on_deleted(
        self,
        event: FileSystemEvent,
    ) -> None:

        self._callback(event)

    ###########################################################################

    def on_moved(
        self,
        event: FileSystemEvent,
    ) -> None:

        self._callback(event)

###############################################################################
# File Watcher
###############################################################################


class FileWatcher:
    """
    Real-time workspace file watcher.

    Responsibilities

    - File create
    - File modify
    - File delete
    - File rename
    - Folder changes
    """

    def __init__(self) -> None:

        self._observer = Observer()

        self._handler = WorkspaceEventHandler(
            self._handle_event,
        )

        self._workspace: Path | None = None

        self._running = False

        logger.info(
            "File Watcher initialized."
        )

    ###########################################################################

    def start(
        self,
        workspace: str | Path,
    ) -> None:
        """
        Start watching workspace.
        """

        workspace = Path(workspace).resolve()

        self._workspace = workspace

        self._observer.schedule(
            self._handler,
            str(workspace),
            recursive=True,
        )

        self._observer.start()

        self._running = True

        logger.info(
            "Watching workspace: %s",
            workspace,
        )

    ###########################################################################

    def stop(
        self,
    ) -> None:
        """
        Stop watcher.
        """

        self._observer.stop()

        self._observer.join()

        self._running = False

        logger.info(
            "File Watcher stopped."
        )
###############################################################################
# Event Handling
###############################################################################

    def _handle_event(
        self,
        event: FileSystemEvent,
    ) -> None:
        """
        Handle filesystem events.
        """

        if event.is_directory:

            return

        logger.info(
            "%s: %s",
            event.event_type,
            event.src_path,
        )

###############################################################################
# Status
###############################################################################

    @property
    def running(
        self,
    ) -> bool:
        """
        Return watcher status.
        """

        return self._running

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, object]:
        """
        Return watcher statistics.
        """

        return {
            "running": self._running,
            "workspace": (
                str(self._workspace)
                if self._workspace
                else None
            ),
            "observer_alive": (
                self._observer.is_alive()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return watcher report.
        """

        return {
            "statistics": self.statistics(),
        }

###############################################################################
# Global Watcher
###############################################################################

file_watcher = FileWatcher()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "FileWatcher",
    "WorkspaceEventHandler",
    "file_watcher",
]