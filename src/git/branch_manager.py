"""
==============================================================================
GEETA AI Engine

File        : branch_manager.py
Package     : git
Description : Git Branch Manager

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
# Branch Manager
###############################################################################


class BranchManager:
    """
    High-level Git branch manager.

    Responsibilities

    - Branch creation
    - Branch deletion
    - Branch switching
    - Branch renaming
    - Upstream management
    - Branch comparison
    """

    def __init__(self) -> None:

        logger.info(
            "Branch Manager initialized."
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

    def create(
        self,
        name: str,
    ) -> subprocess.CompletedProcess[str]:
        """
        Create a new branch.
        """

        return subprocess.run(
            [
                "git",
                "branch",
                name,
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

    ###########################################################################

    def checkout(
        self,
        name: str,
    ) -> subprocess.CompletedProcess[str]:
        """
        Switch to a branch.
        """

        return subprocess.run(
            [
                "git",
                "checkout",
                name,
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

    ###########################################################################

    def create_and_checkout(
        self,
        name: str,
    ) -> subprocess.CompletedProcess[str]:
        """
        Create and switch to a branch.
        """

        return subprocess.run(
            [
                "git",
                "checkout",
                "-b",
                name,
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

    ###########################################################################

    def delete(
        self,
        name: str,
        force: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        """
        Delete a branch.
        """

        command = [
            "git",
            "branch",
            "-D" if force else "-d",
            name,
        ]

        return subprocess.run(
            command,
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )
###############################################################################
# Branch Rename
###############################################################################

    def rename(
        self,
        old_name: str,
        new_name: str,
    ) -> subprocess.CompletedProcess[str]:
        """
        Rename a branch.
        """

        return subprocess.run(
            [
                "git",
                "branch",
                "-m",
                old_name,
                new_name,
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

###############################################################################
# Branch Listing
###############################################################################

    def branches(
        self,
    ) -> list[str]:
        """
        Return all local branches.
        """

        result = subprocess.run(
            [
                "git",
                "branch",
                "--format=%(refname:short)",
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
# Branch Comparison
###############################################################################

    def compare(
        self,
        source: str,
        target: str,
    ) -> subprocess.CompletedProcess[str]:
        """
        Compare two branches.
        """

        return subprocess.run(
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

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return branch statistics.
        """

        branches = self.branches()

        return {
            "current_branch": (
                git_manager.current_branch()
            ),
            "branch_count": len(
                branches
            ),
            "branches": branches,
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return branch manager report.
        """

        return {
            "statistics": self.statistics(),
        }

###############################################################################
# Global Branch Manager
###############################################################################

branch_manager = BranchManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "BranchManager",
    "branch_manager",
]