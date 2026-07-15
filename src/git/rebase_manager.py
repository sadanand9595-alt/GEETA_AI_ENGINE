"""
==============================================================================
GEETA AI Engine

File        : rebase_manager.py
Package     : git
Description : Git Rebase Manager

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
# Rebase Manager
###############################################################################


class RebaseManager:
    """
    High-level Git rebase manager.

    Responsibilities

    - Branch rebasing
    - Interactive rebase
    - Conflict detection
    - Continue / Skip / Abort
    - Rebase validation
    - Status inspection
    """

    def __init__(self) -> None:

        logger.info(
            "Rebase Manager initialized."
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

    def rebase(
        self,
        branch: str,
    ) -> subprocess.CompletedProcess[str]:
        """
        Rebase onto another branch.
        """

        return subprocess.run(
            [
                "git",
                "rebase",
                branch,
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

    ###########################################################################

    def interactive(
        self,
        upstream: str,
    ) -> subprocess.CompletedProcess[str]:
        """
        Start an interactive rebase.
        """

        return subprocess.run(
            [
                "git",
                "rebase",
                "-i",
                upstream,
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

    ###########################################################################

    def continue_rebase(
        self,
    ) -> subprocess.CompletedProcess[str]:
        """
        Continue a paused rebase.
        """

        return subprocess.run(
            [
                "git",
                "rebase",
                "--continue",
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

    ###########################################################################

    def skip(
        self,
    ) -> subprocess.CompletedProcess[str]:
        """
        Skip the current rebase commit.
        """

        return subprocess.run(
            [
                "git",
                "rebase",
                "--skip",
            ],
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
        Abort the current rebase.
        """

        return subprocess.run(
            [
                "git",
                "rebase",
                "--abort",
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )
###############################################################################
# Conflict Detection
###############################################################################

    def has_conflicts(
        self,
    ) -> bool:
        """
        Check whether the current rebase
        has unresolved conflicts.
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
# Rebase Status
###############################################################################

    def status(
        self,
    ) -> dict[str, Any]:
        """
        Return rebase status.
        """

        result = subprocess.run(
            [
                "git",
                "status",
                "--short",
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

        return {
            "conflicts": self.has_conflicts(),
            "working_tree": result.stdout.strip(),
        }

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return rebase manager statistics.
        """

        status = self.status()

        return {
            "repository": str(
                self.repository,
            ),
            "has_conflicts": status[
                "conflicts"
            ],
            "working_tree_clean": (
                not bool(
                    status["working_tree"]
                )
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return rebase manager report.
        """

        return {
            "status": self.status(),
            "statistics": self.statistics(),
        }

###############################################################################
# Global Rebase Manager
###############################################################################

rebase_manager = RebaseManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "RebaseManager",
    "rebase_manager",
]