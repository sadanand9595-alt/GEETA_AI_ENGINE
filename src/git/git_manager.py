"""
==============================================================================
GEETA AI Engine

File        : git_manager.py
Package     : git
Description : Git Repository Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Git Manager
###############################################################################


class GitManager:
    """
    Central Git repository manager.

    Responsibilities

    - Repository detection
    - Repository initialization
    - Status inspection
    - Branch management
    - Commit support
    - Diff generation
    """

    def __init__(self) -> None:

        self._repository: Path | None = None

        logger.info(
            "Git Manager initialized."
        )

    ###########################################################################

    def open_repository(
        self,
        path: str | Path,
    ) -> None:
        """
        Open a Git repository.
        """

        repository = Path(path).resolve()

        if not (repository / ".git").exists():

            raise RuntimeError(
                "Not a Git repository."
            )

        self._repository = repository

        logger.info(
            "Opened repository: %s",
            repository,
        )

    ###########################################################################

    def initialize(
        self,
        path: str | Path,
    ) -> subprocess.CompletedProcess[str]:
        """
        Initialize a Git repository.
        """

        repository = Path(path)

        result = subprocess.run(
            [
                "git",
                "init",
            ],
            cwd=repository,
            text=True,
            capture_output=True,
            check=False,
        )

        if result.returncode == 0:

            self._repository = repository.resolve()

        return result

    ###########################################################################

    def repository(
        self,
    ) -> Path | None:
        """
        Return active repository.
        """

        return self._repository

    ###########################################################################

    def status(
        self,
    ) -> subprocess.CompletedProcess[str]:
        """
        Execute git status.
        """

        if self._repository is None:

            raise RuntimeError(
                "Repository not opened."
            )

        return subprocess.run(
            [
                "git",
                "status",
                "--short",
            ],
            cwd=self._repository,
            text=True,
            capture_output=True,
            check=False,
        )

    ###########################################################################

    def current_branch(
        self,
    ) -> str:
        """
        Return current branch name.
        """

        result = subprocess.run(
            [
                "git",
                "branch",
                "--show-current",
            ],
            cwd=self._repository,
            text=True,
            capture_output=True,
            check=False,
        )

        return result.stdout.strip()
###############################################################################
# Staging
###############################################################################

    def add(
        self,
        *files: str,
    ) -> subprocess.CompletedProcess[str]:
        """
        Stage files.
        """

        return subprocess.run(
            [
                "git",
                "add",
                *files,
            ],
            cwd=self._repository,
            text=True,
            capture_output=True,
            check=False,
        )

###############################################################################
# Commit
###############################################################################

    def commit(
        self,
        message: str,
    ) -> subprocess.CompletedProcess[str]:
        """
        Create a commit.
        """

        return subprocess.run(
            [
                "git",
                "commit",
                "-m",
                message,
            ],
            cwd=self._repository,
            text=True,
            capture_output=True,
            check=False,
        )

###############################################################################
# Diff
###############################################################################

    def diff(
        self,
    ) -> subprocess.CompletedProcess[str]:
        """
        Return repository diff.
        """

        return subprocess.run(
            [
                "git",
                "diff",
            ],
            cwd=self._repository,
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
        Return Git repository statistics.
        """

        return {
            "repository": (
                str(self._repository)
                if self._repository
                else None
            ),
            "branch": (
                self.current_branch()
                if self._repository
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
        Return Git manager report.
        """

        return {
            "statistics": self.statistics(),
            "status": (
                self.status().stdout
                if self._repository
                else ""
            ),
        }

###############################################################################
# Global Git Manager
###############################################################################

git_manager = GitManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "GitManager",
    "git_manager",
]