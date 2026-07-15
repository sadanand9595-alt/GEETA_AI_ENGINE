"""
==============================================================================
GEETA AI Engine

File        : diff_manager.py
Package     : git
Description : Git Diff Manager

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
# Diff Manager
###############################################################################


class DiffManager:
    """
    High-level Git diff manager.

    Responsibilities

    - Working tree diff
    - Staged diff
    - Commit comparison
    - Branch comparison
    - Diff statistics
    - AI-ready summaries
    """

    def __init__(self) -> None:

        logger.info(
            "Diff Manager initialized."
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

    def working_tree_diff(
        self,
    ) -> str:
        """
        Return working tree diff.
        """

        result = subprocess.run(
            [
                "git",
                "diff",
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

        return result.stdout

    ###########################################################################

    def staged_diff(
        self,
    ) -> str:
        """
        Return staged diff.
        """

        result = subprocess.run(
            [
                "git",
                "diff",
                "--cached",
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

        return result.stdout

    ###########################################################################

    def commit_diff(
        self,
        source: str,
        target: str,
    ) -> str:
        """
        Compare two commits.
        """

        result = subprocess.run(
            [
                "git",
                "diff",
                source,
                target,
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

        return result.stdout

    ###########################################################################

    def branch_diff(
        self,
        source: str,
        target: str,
    ) -> str:
        """
        Compare two branches.
        """

        result = subprocess.run(
            [
                "git",
                "diff",
                f"{source}..{target}",
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

        return result.stdout
###############################################################################
# Diff Statistics
###############################################################################

    def statistics(
        self,
        diff: str | None = None,
    ) -> dict[str, Any]:
        """
        Return basic diff statistics.
        """

        if diff is None:

            diff = self.working_tree_diff()

        lines = diff.splitlines()

        added = sum(
            1
            for line in lines
            if line.startswith("+")
            and not line.startswith("+++")
        )

        removed = sum(
            1
            for line in lines
            if line.startswith("-")
            and not line.startswith("---")
        )

        files = sum(
            1
            for line in lines
            if line.startswith("diff --git")
        )

        return {
            "files_changed": files,
            "lines_added": added,
            "lines_removed": removed,
        }

###############################################################################
# AI Summary
###############################################################################

    def summarize(
        self,
        diff: str | None = None,
    ) -> str:
        """
        Generate a simple diff summary.

        Placeholder implementation.
        Future versions will integrate with
        the AI Code Review Engine.
        """

        stats = self.statistics(
            diff,
        )

        return (
            f"Modified {stats['files_changed']} file(s), "
            f"added {stats['lines_added']} line(s), "
            f"removed {stats['lines_removed']} line(s)."
        )

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return diff manager report.
        """

        diff = self.working_tree_diff()

        return {
            "statistics": self.statistics(
                diff,
            ),
            "summary": self.summarize(
                diff,
            ),
        }

###############################################################################
# Global Diff Manager
###############################################################################

diff_manager = DiffManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "DiffManager",
    "diff_manager",
]