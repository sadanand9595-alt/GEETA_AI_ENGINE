"""
==============================================================================
GEETA AI Engine

File        : git_listener.py
Package     : listeners
Description : Git Repository Listener

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import subprocess
import threading
import time
from pathlib import Path

from config.logger import get_logger
from core.event_bus import publish

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Git Listener
###############################################################################


class GitListener:
    """
    Monitors Git repository changes.

    Detects:

    - Current branch
    - Modified files
    - Added files
    - Deleted files
    - Git status changes
    """

    def __init__(
        self,
        repository: Path,
        interval: float = 2.0,
    ) -> None:

        self.repository = repository

        self.interval = interval

        self._running = False

        self._thread: threading.Thread | None = None

        self._last_status = ""

    ###########################################################################

    @property
    def running(self) -> bool:
        """
        Return listener state.
        """

        return self._running

    ###########################################################################

    def start(self) -> None:
        """
        Start monitoring Git repository.
        """

        if self._running:
            return

        logger.info(
            "Starting Git Listener..."
        )

        self._running = True

        self._thread = threading.Thread(
            target=self._monitor,
            daemon=True,
            name="GitListener",
        )

        self._thread.start()

        logger.info(
            "Git Listener Started."
        )

    ###########################################################################

    def stop(self) -> None:
        """
        Stop monitoring.
        """

        if not self._running:
            return

        logger.info(
            "Stopping Git Listener..."
        )

        self._running = False

        if self._thread:

            self._thread.join(timeout=2)

        logger.info(
            "Git Listener Stopped."
        )

    ###########################################################################

    def _git_status(self) -> str:
        """
        Return git status.
        """

        result = subprocess.run(
            [
                "git",
                "status",
                "--porcelain",
            ],
            cwd=self.repository,
            capture_output=True,
            text=True,
            check=False,
        )

        return result.stdout

    ###########################################################################

    def _monitor(self) -> None:
        """
        Monitor repository continuously.
        """

        while self._running:

            try:

                status = self._git_status()

                if status != self._last_status:

                    logger.info(
                        "Git repository changed."
                    )

                    publish(
                        "git.changed",
                        status=status,
                    )

                    self._last_status = status

            except Exception:

                logger.exception(
                    "Git listener failed."
                )

            time.sleep(self.interval)
###############################################################################
# Git Information
###############################################################################

    def current_branch(self) -> str:
        """
        Return the current Git branch.
        """

        result = subprocess.run(
            [
                "git",
                "branch",
                "--show-current",
            ],
            cwd=self.repository,
            capture_output=True,
            text=True,
            check=False,
        )

        return result.stdout.strip()

    ###########################################################################

    def restart(self) -> None:
        """
        Restart the Git listener.
        """

        logger.info(
            "Restarting Git Listener..."
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


def start_git_listener(
    repository: Path,
    interval: float = 2.0,
) -> GitListener:
    """
    Create and start a Git listener.
    """

    listener = GitListener(
        repository=repository,
        interval=interval,
    )

    listener.start()

    return listener


def stop_git_listener(
    listener: GitListener,
) -> None:
    """
    Stop a running Git listener.
    """

    listener.stop()


###############################################################################
# Exports
###############################################################################

__all__ = [
    "GitListener",
    "start_git_listener",
    "stop_git_listener",
]