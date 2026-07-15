"""
==============================================================================
GEETA AI Engine

File        : git_monitor.py
Package     : git
Description : Git Repository Monitor

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import threading
import time
from typing import Any

from config.logger import get_logger

from git.git_events import (
    git_events,
)
from git.git_manager import (
    git_manager,
)

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Git Monitor
###############################################################################


class GitMonitor:
    """
    Repository monitoring service.

    Responsibilities

    - Repository monitoring
    - Branch monitoring
    - Status monitoring
    - Event publishing
    - Background monitoring
    """

    def __init__(
        self,
        interval: float = 2.0,
    ) -> None:

        self._interval = interval

        self._running = False

        self._thread: threading.Thread | None = None

        self._last_status = ""

        logger.info(
            "Git Monitor initialized."
        )

    ###########################################################################

    def start(
        self,
    ) -> None:
        """
        Start repository monitoring.
        """

        if self._running:

            return

        self._running = True

        self._thread = threading.Thread(
            target=self._loop,
            daemon=True,
            name="GitMonitor",
        )

        self._thread.start()

        logger.info(
            "Git Monitor started."
        )

    ###########################################################################

    def stop(
        self,
    ) -> None:
        """
        Stop repository monitoring.
        """

        self._running = False

        if self._thread:

            self._thread.join()

        logger.info(
            "Git Monitor stopped."
        )

    ###########################################################################

    def _loop(
        self,
    ) -> None:
        """
        Background monitoring loop.
        """

        while self._running:

            self.refresh()

            time.sleep(
                self._interval,
            )

    ###########################################################################

    def refresh(
        self,
    ) -> None:
        """
        Refresh repository state.
        """

        repository = git_manager.repository()

        if repository is None:

            return

        status = git_manager.status().stdout

        if status != self._last_status:

            self._last_status = status

            git_events.publish(
                "repository.changed",
                status=status,
            )

            logger.info(
                "Repository change detected."
            )
###############################################################################
# Repository Information
###############################################################################

    def current_branch(
        self,
    ) -> str | None:
        """
        Return the current branch.
        """

        repository = git_manager.repository()

        if repository is None:

            return None

        return git_manager.current_branch()

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return Git monitor statistics.
        """

        repository = git_manager.repository()

        return {
            "running": self._running,
            "interval": self._interval,
            "repository_open": repository is not None,
            "current_branch": self.current_branch(),
            "status_cached": bool(
                self._last_status
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return Git monitor report.
        """

        return {
            "statistics": self.statistics(),
            "last_status": self._last_status,
        }

###############################################################################
# Global Git Monitor
###############################################################################

git_monitor = GitMonitor()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "GitMonitor",
    "git_monitor",
]