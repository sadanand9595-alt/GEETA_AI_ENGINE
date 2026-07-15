"""
==============================================================================
GEETA AI Engine

File        : merge_manager.py
Package     : git
Description : Git Merge Manager

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
# Merge Manager
###############################################################################


class MergeManager:
    """
    High-level Git merge manager.

    Responsibilities

    - Branch merging
    - Merge status
    - Conflict detection
    - Merge abort
    - Merge continue
    - Merge strategies
    """

    def __init__(self) -> None:

        logger.info(
            "Merge Manager initialized."
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

    def merge(
        self,
        branch: str,
        strategy: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """
        Merge a branch.
        """

        command = [
            "git",
            "merge",
        ]

        if strategy:

            command.extend(
                [
                    "--strategy",
                    strategy,
                ]
            )

        command.append(
            branch,
        )

        return subprocess.run(
            command,
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

    ###########################################################################

    def abort(
        self,
    ) -> subprocess.CompletedProcess[str]:
        """
        Abort an active merge.
        """

        return subprocess.run(
            [
                "git",
                "merge",
                "--abort",
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

    ###########################################################################

    def continue_merge(
        self,
    ) -> subprocess.CompletedProcess[str]:
        """
        Continue an interrupted merge.
        """

        return subprocess.run(
            [
                "git",
                "merge",
                "--continue",
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

    ###########################################################################

    def has_conflicts(
        self,
    ) -> bool:
        """
        Check whether merge conflicts exist.
        """

        result = subprocess.run(
            [
                "git",
                "diff",
                "--name-only",
                "--diff-filter=U",
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

        return bool(
            result.stdout.strip()
        )
###############################################################################
# Fast-Forward Detection
###############################################################################

    def can_fast_forward(
        self,
        source: str,
        target: str,
    ) -> bool:
        """
        Check whether target can be fast-forwarded.
        """

        result = subprocess.run(
            [
                "git",
                "merge-base",
                "--is-ancestor",
                source,
                target,
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

        return result.returncode == 0

###############################################################################
# Conflict Files
###############################################################################

    def conflict_files(
        self,
    ) -> list[str]:
        """
        Return files with merge conflicts.
        """

        result = subprocess.run(
            [
                "git",
                "diff",
                "--name-only",
                "--diff-filter=U",
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

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return merge manager statistics.
        """

        conflicts = self.conflict_files()

        return {
            "has_conflicts": bool(conflicts),
            "conflict_count": len(conflicts),
            "conflict_files": conflicts,
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return merge manager report.
        """

        return {
            "statistics": self.statistics(),
        }

###############################################################################
# Global Merge Manager
###############################################################################

merge_manager = MergeManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "MergeManager",
    "merge_manager",
]