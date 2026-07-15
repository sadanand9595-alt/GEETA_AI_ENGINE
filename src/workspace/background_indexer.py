"""
==============================================================================
GEETA AI Engine

File        : background_indexer.py
Package     : workspace
Description : Background Indexer

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import threading
import time
from pathlib import Path
from typing import Any

from config.logger import get_logger

from workspace.project_index import project_index
from workspace.workspace_manager import workspace_manager

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Background Indexer
###############################################################################


class BackgroundIndexer:
    """
    Background workspace indexer.

    Responsibilities

    - Monitor workspace
    - Incremental indexing
    - Debounced refresh
    - Auto project updates
    - Symbol refresh
    - Semantic refresh
    """

    def __init__(
        self,
        interval: float = 5.0,
    ) -> None:

        self._interval = interval

        self._thread: threading.Thread | None = None

        self._running = False

        self._last_scan: dict[
            Path,
            float,
        ] = {}

        logger.info(
            "Background Indexer initialized."
        )

    ###########################################################################

    def start(
        self,
    ) -> None:
        """
        Start background worker.
        """

        if self._running:

            return

        self._running = True

        self._thread = threading.Thread(
            target=self._worker,
            daemon=True,
            name="BackgroundIndexer",
        )

        self._thread.start()

        logger.info(
            "Background indexer started."
        )

    ###########################################################################

    def stop(
        self,
    ) -> None:
        """
        Stop background worker.
        """

        self._running = False

        logger.info(
            "Background indexer stopped."
        )

    ###########################################################################

    def _worker(
        self,
    ) -> None:
        """
        Worker loop.
        """

        while self._running:

            try:

                self.scan()

            except Exception:

                logger.exception(
                    "Background indexing failed."
                )

            time.sleep(
                self._interval,
            )

    ###########################################################################

    def scan(
        self,
    ) -> None:
        """
        Scan workspace for file changes.
        """

        if not workspace_manager.is_open():

            return

        changed = False

        for file in workspace_manager.scan_files():

            timestamp = file.stat().st_mtime

            previous = self._last_scan.get(
                file,
            )

            if previous != timestamp:

                self._last_scan[file] = timestamp

                changed = True

        if changed:

            logger.info(
                "Workspace changes detected."
            )

            project_index.refresh()
###############################################################################
# Manual Refresh
###############################################################################

    def refresh(
        self,
    ) -> None:
        """
        Force a complete project refresh.
        """

        logger.info(
            "Manual project refresh requested."
        )

        project_index.refresh()

###############################################################################
# Status
###############################################################################

    @property
    def running(
        self,
    ) -> bool:
        """
        Return worker status.
        """

        return self._running

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return background indexer statistics.
        """

        return {
            "running": self._running,
            "scan_interval": self._interval,
            "tracked_files": len(
                self._last_scan
            ),
            "thread_alive": (
                self._thread.is_alive()
                if self._thread
                else False
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return background indexer report.
        """

        return {
            "statistics": self.statistics(),
            "workspace_open": (
                workspace_manager.is_open()
            ),
        }

###############################################################################
# Global Indexer
###############################################################################

background_indexer = BackgroundIndexer()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "BackgroundIndexer",
    "background_indexer",
]