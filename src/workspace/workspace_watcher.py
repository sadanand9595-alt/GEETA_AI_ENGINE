"""
==============================================================================
GEETA AI IDE

File        : workspace_watcher.py
Package     : workspace
Description : Enterprise Workspace Watcher

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import asyncio

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Event Type
###############################################################################


class WorkspaceEventType(str, Enum):

    CREATED = "created"

    MODIFIED = "modified"

    DELETED = "deleted"

    MOVED = "moved"

###############################################################################
# Watcher Status
###############################################################################


class WatcherStatus(str, Enum):

    STOPPED = "stopped"

    RUNNING = "running"

    PAUSED = "paused"

###############################################################################
# Workspace Event
###############################################################################


@dataclass(slots=True)
class WorkspaceEvent:
    """
    Workspace event.
    """

    event_type: WorkspaceEventType

    path: str

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )

###############################################################################
# Workspace Watcher
###############################################################################


class WorkspaceWatcher:
    """
    Enterprise Workspace Watcher.

    Responsibilities

    - File monitoring
    - Event queue
    - Ignore rules
    - AI notifications
    - Workspace synchronization
    """

    ###########################################################################

    def __init__(
        self,
        workspace: str,
    ) -> None:

        self.workspace = Path(
            workspace,
        )

        self.status = (
            WatcherStatus.STOPPED
        )

        self._events: list[
            WorkspaceEvent
        ] = []

        self._ignored = {

            ".git",

            "__pycache__",

            ".idea",

            ".vscode",

            "node_modules",

            ".pytest_cache",

            ".mypy_cache",
        }

        logger.info(
            "Workspace Watcher initialized."
        )

###############################################################################
# Start
###############################################################################

    async def start(
        self,
    ) -> None:
        """
        Start watcher.
        """

        self.status = (
            WatcherStatus.RUNNING
        )

        logger.info(
            "Workspace watcher started."
        )

###############################################################################
# Stop
###############################################################################

    async def stop(
        self,
    ) -> None:
        """
        Stop watcher.
        """

        self.status = (
            WatcherStatus.STOPPED
        )

        logger.info(
            "Workspace watcher stopped."
        )

###############################################################################
# Pause
###############################################################################

    def pause(
        self,
    ) -> None:

        self.status = (
            WatcherStatus.PAUSED
        )

###############################################################################
# Resume
###############################################################################

    def resume(
        self,
    ) -> None:

        self.status = (
            WatcherStatus.RUNNING
        )
###############################################################################
# Ignore Rule
###############################################################################

    def ignored(
        self,
        path: Path,
    ) -> bool:
        """
        Check whether path should be ignored.
        """

        return any(
            part in self._ignored
            for part in path.parts
        )

###############################################################################
# Recursive Scan
###############################################################################

    def scan(
        self,
    ) -> list[Path]:
        """
        Scan workspace recursively.
        """

        files: list[Path] = []

        for path in self.workspace.rglob("*"):

            if self.ignored(path):

                continue

            if path.is_file():

                files.append(path)

        return files

###############################################################################
# Queue Event
###############################################################################

    def queue_event(
        self,
        event: WorkspaceEvent,
    ) -> None:
        """
        Queue workspace event.
        """

        self._events.append(
            event,
        )

###############################################################################
# Next Event
###############################################################################

    def next_event(
        self,
    ) -> WorkspaceEvent | None:
        """
        Return next queued event.
        """

        if not self._events:

            return None

        return self._events.pop(0)

###############################################################################
# Debounce
###############################################################################

    async def debounce(
        self,
        delay: float = 0.25,
    ) -> None:
        """
        Debounce file events.
        """

        await asyncio.sleep(
            delay,
        )

###############################################################################
# Detect Changes
###############################################################################

    async def detect_changes(
        self,
    ) -> None:
        """
        Detect workspace changes.
        """

        for path in self.scan():

            self.queue_event(

                WorkspaceEvent(

                    event_type=(
                        WorkspaceEventType.MODIFIED
                    ),

                    path=str(path),
                )
            )

###############################################################################
# Monitor Loop
###############################################################################

    async def monitor(
        self,
    ) -> None:
        """
        Background monitoring loop.
        """

        while (
            self.status
            == WatcherStatus.RUNNING
        ):

            try:

                await self.detect_changes()

                await self.debounce()

            except asyncio.CancelledError:

                raise

            except Exception:

                logger.exception(
                    "Workspace monitoring failed."
                )

                await asyncio.sleep(
                    1.0,
                )
###############################################################################
# File Created
###############################################################################

    def on_created(
        self,
        path: str,
    ) -> None:
        """
        Handle file creation.
        """

        self.queue_event(
            WorkspaceEvent(
                event_type=WorkspaceEventType.CREATED,
                path=path,
            )
        )

        logger.info(
            "Created: %s",
            path,
        )

###############################################################################
# File Modified
###############################################################################

    def on_modified(
        self,
        path: str,
    ) -> None:
        """
        Handle file modification.
        """

        self.queue_event(
            WorkspaceEvent(
                event_type=WorkspaceEventType.MODIFIED,
                path=path,
            )
        )

###############################################################################
# File Deleted
###############################################################################

    def on_deleted(
        self,
        path: str,
    ) -> None:
        """
        Handle file deletion.
        """

        self.queue_event(
            WorkspaceEvent(
                event_type=WorkspaceEventType.DELETED,
                path=path,
            )
        )

###############################################################################
# File Renamed
###############################################################################

    def on_moved(
        self,
        source: str,
        destination: str,
    ) -> None:
        """
        Handle file rename.
        """

        self.queue_event(
            WorkspaceEvent(
                event_type=WorkspaceEventType.MOVED,
                path=destination,
            )
        )

        logger.info(
            "%s -> %s",
            source,
            destination,
        )

###############################################################################
# Refresh AI Context
###############################################################################

    async def refresh_context(
        self,
    ) -> None:
        """
        Notify AI Context Manager.
        """

        logger.info(
            "Refreshing AI context."
        )

###############################################################################
# Re-index Workspace
###############################################################################

    async def reindex(
        self,
    ) -> None:
        """
        Trigger workspace re-index.
        """

        logger.info(
            "Workspace re-index started."
        )

###############################################################################
# Event Dispatcher
###############################################################################

    async def dispatch(
        self,
    ) -> None:
        """
        Dispatch queued events.
        """

        while True:

            event = self.next_event()

            if event is None:

                break

            logger.info(
                "%s : %s",
                event.event_type.value,
                event.path,
            )

            await self.refresh_context()

            await self.reindex()

###############################################################################
# VS Code Sync
###############################################################################

    async def sync_vscode(
        self,
    ) -> None:
        """
        Synchronize with VS Code Bridge.
        """

        logger.info(
            "Synchronizing VS Code."
        )

###############################################################################
# Event Subscribers
###############################################################################

    def subscribe(
        self,
        callback,
    ) -> None:
        """
        Register event subscriber.
        """

        if not hasattr(
            self,
            "_subscribers",
        ):

            self._subscribers = []

        self._subscribers.append(
            callback,
        )

###############################################################################
# Notify Subscribers
###############################################################################

    async def notify(
        self,
        event: WorkspaceEvent,
    ) -> None:
        """
        Notify subscribers.
        """

        for callback in getattr(
            self,
            "_subscribers",
            [],
        ):

            await callback(
                event,
            )
###############################################################################
# File Created
###############################################################################

    def on_created(
        self,
        path: str,
    ) -> None:
        """
        Handle file creation.
        """

        self.queue_event(
            WorkspaceEvent(
                event_type=WorkspaceEventType.CREATED,
                path=path,
            )
        )

        logger.info(
            "Created: %s",
            path,
        )

###############################################################################
# File Modified
###############################################################################

    def on_modified(
        self,
        path: str,
    ) -> None:
        """
        Handle file modification.
        """

        self.queue_event(
            WorkspaceEvent(
                event_type=WorkspaceEventType.MODIFIED,
                path=path,
            )
        )

###############################################################################
# File Deleted
###############################################################################

    def on_deleted(
        self,
        path: str,
    ) -> None:
        """
        Handle file deletion.
        """

        self.queue_event(
            WorkspaceEvent(
                event_type=WorkspaceEventType.DELETED,
                path=path,
            )
        )

###############################################################################
# File Renamed
###############################################################################

    def on_moved(
        self,
        source: str,
        destination: str,
    ) -> None:
        """
        Handle file rename.
        """

        self.queue_event(
            WorkspaceEvent(
                event_type=WorkspaceEventType.MOVED,
                path=destination,
            )
        )

        logger.info(
            "%s -> %s",
            source,
            destination,
        )

###############################################################################
# Refresh AI Context
###############################################################################

    async def refresh_context(
        self,
    ) -> None:
        """
        Notify AI Context Manager.
        """

        logger.info(
            "Refreshing AI context."
        )

###############################################################################
# Re-index Workspace
###############################################################################

    async def reindex(
        self,
    ) -> None:
        """
        Trigger workspace re-index.
        """

        logger.info(
            "Workspace re-index started."
        )

###############################################################################
# Event Dispatcher
###############################################################################

    async def dispatch(
        self,
    ) -> None:
        """
        Dispatch queued events.
        """

        while True:

            event = self.next_event()

            if event is None:

                break

            logger.info(
                "%s : %s",
                event.event_type.value,
                event.path,
            )

            await self.refresh_context()

            await self.reindex()

###############################################################################
# VS Code Sync
###############################################################################

    async def sync_vscode(
        self,
    ) -> None:
        """
        Synchronize with VS Code Bridge.
        """

        logger.info(
            "Synchronizing VS Code."
        )

###############################################################################
# Event Subscribers
###############################################################################

    def subscribe(
        self,
        callback,
    ) -> None:
        """
        Register event subscriber.
        """

        if not hasattr(
            self,
            "_subscribers",
        ):

            self._subscribers = []

        self._subscribers.append(
            callback,
        )

###############################################################################
# Notify Subscribers
###############################################################################

    async def notify(
        self,
        event: WorkspaceEvent,
    ) -> None:
        """
        Notify subscribers.
        """

        for callback in getattr(
            self,
            "_subscribers",
            [],
        ):

            await callback(
                event,
            )
###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Workspace watcher statistics.
        """

        return {

            "events": len(
                self._events,
            ),

            "subscribers": len(
                getattr(
                    self,
                    "_subscribers",
                    [],
                )
            ),

            "ignored": len(
                self._ignored,
            ),

            "workspace_files": len(
                self.scan(),
            ),
        }

###############################################################################
# Cleanup
###############################################################################

    def cleanup(
        self,
    ) -> None:
        """
        Reset watcher state.
        """

        self._events.clear()

        if hasattr(
            self,
            "_subscribers",
        ):

            self._subscribers.clear()

        self.status = (
            WatcherStatus.STOPPED
        )

        logger.info(
            "Workspace Watcher cleaned."
        )

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Generate watcher report.
        """

        return {

            "workspace": str(
                self.workspace,
            ),

            "status": self.status.value,

            "statistics": self.statistics(),

            "ignored_directories": sorted(
                self._ignored,
            ),
        }

###############################################################################
# AI Context Integration
###############################################################################

    async def notify_context_manager(
        self,
    ) -> None:
        """
        Notify AI Context Manager.
        """

        logger.info(
            "AI Context Manager notified."
        )

###############################################################################
# Workspace Index Integration
###############################################################################

    async def notify_workspace_indexer(
        self,
    ) -> None:
        """
        Notify Workspace Indexer.
        """

        logger.info(
            "Workspace Indexer notified."
        )

###############################################################################
# VS Code Bridge Integration
###############################################################################

    async def notify_vscode_bridge(
        self,
    ) -> None:
        """
        Notify VS Code Bridge.
        """

        logger.info(
            "VS Code Bridge notified."
        )

###############################################################################
# Global Workspace Watcher
###############################################################################

workspace_watcher: (
    WorkspaceWatcher | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "WorkspaceEventType",
    "WatcherStatus",
    "WorkspaceEvent",
    "WorkspaceWatcher",
    "workspace_watcher",
]