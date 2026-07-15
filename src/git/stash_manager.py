"""
==============================================================================
GEETA AI Engine

File        : stash_manager.py
Package     : git
Description : Git Stash Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import subprocess
from typing import Any

from config.logger import get_logger

from git.git_manager import git_manager

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Stash Manager
###############################################################################


class StashManager:
    """
    High-level Git stash manager.

    Responsibilities

    - Create stashes
    - Named stashes
    - Apply stashes
    - Pop stashes
    - Drop stashes
    - Stash inspection
    """

    def __init__(self) -> None:

        logger.info(
            "Stash Manager initialized."
        )

    ###########################################################################

    @property
    def repository(self):
        """
        Return active repository.
        """

        repository = git_manager.repository()

        if repository is None:

            raise RuntimeError(
                "No Git repository opened."
            )

        return repository

    ###########################################################################

    def save(
        self,
        message: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """
        Create a stash.
        """

        command = [
            "git",
            "stash",
            "push",
        ]

        if message:

            command.extend(
                [
                    "-m",
                    message,
                ]
            )

        return subprocess.run(
            command,
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

    ###########################################################################

    def list(
        self,
    ) -> list[str]:
        """
        Return available stashes.
        """

        result = subprocess.run(
            [
                "git",
                "stash",
                "list",
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

        return [
            line.strip()
            for line in result.stdout.splitlines()
            if line.strip()
        ]

    ###########################################################################

    def apply(
        self,
        stash: str = "stash@{0}",
    ) -> subprocess.CompletedProcess[str]:
        """
        Apply a stash.
        """

        return subprocess.run(
            [
                "git",
                "stash",
                "apply",
                stash,
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

    ###########################################################################

    def pop(
        self,
        stash: str = "stash@{0}",
    ) -> subprocess.CompletedProcess[str]:
        """
        Apply and remove a stash.
        """

        return subprocess.run(
            [
                "git",
                "stash",
                "pop",
                stash,
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )
###############################################################################
# Drop Stash
###############################################################################

    def drop(
        self,
        stash: str = "stash@{0}",
    ) -> subprocess.CompletedProcess[str]:
        """
        Drop a stash entry.
        """

        return subprocess.run(
            [
                "git",
                "stash",
                "drop",
                stash,
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

###############################################################################
# Clear All Stashes
###############################################################################

    def clear(
        self,
    ) -> subprocess.CompletedProcess[str]:
        """
        Remove all stash entries.
        """

        return subprocess.run(
            [
                "git",
                "stash",
                "clear",
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

###############################################################################
# Stash Inspection
###############################################################################

    def show(
        self,
        stash: str = "stash@{0}",
    ) -> str:
        """
        Show the contents of a stash.
        """

        result = subprocess.run(
            [
                "git",
                "stash",
                "show",
                "-p",
                stash,
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

        return result.stdout

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return stash statistics.
        """

        stashes = self.list()

        return {
            "stash_count": len(
                stashes
            ),
            "latest_stash": (
                stashes[0]
                if stashes
                else None
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return stash manager report.
        """

        return {
            "statistics": self.statistics(),
            "stashes": self.list(),
        }

###############################################################################
# Global Stash Manager
###############################################################################

stash_manager = StashManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "StashManager",
    "stash_manager",
]