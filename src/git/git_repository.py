"""
==============================================================================
GEETA AI Engine

File        : git_repository.py
Package     : git
Description : Git Repository Model

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from config.logger import get_logger

from git.git_manager import git_manager

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Git Repository
###############################################################################


class GitRepository:
    """
    High-level Git repository abstraction.

    Responsibilities

    - Repository metadata
    - Branches
    - Tags
    - Remotes
    - Commit history
    - Repository health
    """

    def __init__(
        self,
        path: str | Path,
    ) -> None:

        self._path = Path(path).resolve()

        git_manager.open_repository(
            self._path,
        )

        logger.info(
            "Git Repository loaded: %s",
            self._path,
        )

    ###########################################################################

    @property
    def path(
        self,
    ) -> Path:
        """
        Return repository path.
        """

        return self._path

    ###########################################################################

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
            cwd=self._path,
            text=True,
            capture_output=True,
            check=False,
        )

        return [
            branch.strip()
            for branch in result.stdout.splitlines()
            if branch.strip()
        ]

    ###########################################################################

    def tags(
        self,
    ) -> list[str]:
        """
        Return repository tags.
        """

        result = subprocess.run(
            [
                "git",
                "tag",
            ],
            cwd=self._path,
            text=True,
            capture_output=True,
            check=False,
        )

        return [
            tag.strip()
            for tag in result.stdout.splitlines()
            if tag.strip()
        ]

    ###########################################################################

    def remotes(
        self,
    ) -> list[str]:
        """
        Return configured remotes.
        """

        result = subprocess.run(
            [
                "git",
                "remote",
            ],
            cwd=self._path,
            text=True,
            capture_output=True,
            check=False,
        )

        return [
            remote.strip()
            for remote in result.stdout.splitlines()
            if remote.strip()
        ]
###############################################################################
# Commit History
###############################################################################

    def commit_history(
        self,
        limit: int = 20,
    ) -> list[str]:
        """
        Return recent commit history.
        """

        result = subprocess.run(
            [
                "git",
                "log",
                f"-{limit}",
                "--oneline",
            ],
            cwd=self._path,
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
# Repository Health
###############################################################################

    def health(
        self,
    ) -> dict[str, Any]:
        """
        Return repository health information.
        """

        return {
            "path": str(self._path),
            "branch_count": len(
                self.branches()
            ),
            "tag_count": len(
                self.tags()
            ),
            "remote_count": len(
                self.remotes()
            ),
        }

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return repository statistics.
        """

        return {
            "current_branch": (
                git_manager.current_branch()
            ),
            "branches": len(
                self.branches()
            ),
            "tags": len(
                self.tags()
            ),
            "remotes": len(
                self.remotes()
            ),
            "recent_commits": len(
                self.commit_history()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return repository report.
        """

        return {
            "health": self.health(),
            "statistics": self.statistics(),
            "recent_commits": (
                self.commit_history()
            ),
        }

###############################################################################
# Exports
###############################################################################

__all__ = [
    "GitRepository",
]