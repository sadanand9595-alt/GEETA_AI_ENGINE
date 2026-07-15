"""
==============================================================================
GEETA AI Engine

File        : file_listener.py
Package     : listeners
Description : Project File System Listener

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from pathlib import Path
from threading import RLock

from watchdog.events import (
    FileSystemEvent,
    FileSystemEventHandler,
)

from watchdog.observers import Observer

from config.logger import get_logger
from core.event_bus import publish

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# File Listener
###############################################################################


class FileListener(FileSystemEventHandler):
    """
    Monitors project file changes.
    """

    def __init__(
        self,
        workspace: Path,
    ) -> None:

        super().__init__()

        self.workspace = workspace

        self._observer = Observer()

        self._lock = RLock()

        self._running = False

    ###########################################################################

    @property
    def running(self) -> bool:

        return self._running

    ###########################################################################

    def start(self) -> None:
        """
        Start file monitoring.
        """

        if self._running:
            return

        logger.info(
            "Starting File Listener..."
        )

        self._observer.schedule(
            self,
            str(self.workspace),
            recursive=True,
        )

        self._observer.start()

        self._running = True

        logger.info(
            "File Listener Started."
        )

    ###########################################################################

    def stop(self) -> None:
        """
        Stop monitoring.
        """

        if not self._running:
            return

        logger.info(
            "Stopping File Listener..."
        )

        self._observer.stop()

        self._observer.join()

        self._running = False

        logger.info(
            "File Listener Stopped."
        )

    ###########################################################################
    # Watchdog Events
    ###########################################################################

    def on_created(
        self,
        event: FileSystemEvent,
    ) -> None:

        if event.is_directory:
            return

        logger.info(
            "Created : %s",
            event.src_path,
        )

        publish(
            "file.created",
            path=event.src_path,
        )

    ###########################################################################

    def on_modified(
        self,
        event: FileSystemEvent,
    ) -> None:

        if event.is_directory:
            return

        logger.info(
            "Modified : %s",
            event.src_path,
        )

        publish(
            "file.modified",
            path=event.src_path,
        )

    ###########################################################################

    def on_deleted(
        self,
        event: FileSystemEvent,
    ) -> None:

        if event.is_directory:
            return

        logger.info(
            "Deleted : %s",
            event.src_path,
        )

        publish(
            "file.deleted",
            path=event.src_path,
        )
###############################################################################
# Move / Rename Events
###############################################################################

    def on_moved(
        self,
        event: FileSystemEvent,
    ) -> None:
        """
        Handle file move/rename events.
        """

        if event.is_directory:
            return

        logger.info(
            "Moved : %s -> %s",
            event.src_path,
            event.dest_path,
        )

        publish(
            "file.moved",
            source=event.src_path,
            destination=event.dest_path,
        )

###############################################################################
# Listener Control
###############################################################################

    def restart(self) -> None:
        """
        Restart the file listener.
        """

        logger.info(
            "Restarting File Listener..."
        )

        self.stop()

        self.start()

###############################################################################
# Context Manager
###############################################################################

    def __enter__(self):
        """
        Context manager entry.
        """

        self.start()

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        """
        Context manager exit.
        """

        self.stop()

###############################################################################
# Helper Functions
###############################################################################


def start_listener(
    workspace: Path,
) -> FileListener:
    """
    Create and start a file listener.
    """

    listener = FileListener(workspace)

    listener.start()

    return listener


def stop_listener(
    listener: FileListener,
) -> None:
    """
    Stop an active listener.
    """

    listener.stop()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "FileListener",
    "start_listener",
    "stop_listener",
]