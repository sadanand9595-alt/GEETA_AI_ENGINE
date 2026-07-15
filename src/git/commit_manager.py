"""
==============================================================================
GEETA AI Engine

File        : commit_manager.py
Package     : git
Description : Git Commit Manager

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
# Commit Manager
###############################################################################


class CommitManager:
    """
    High-level Git commit manager.

    Responsibilities

    - Commit creation
    - Commit amendment
    - Commit history
    - Conventional commits
    - Commit validation
    - AI commit message generation
    """

    def __init__(self) -> None:

        logger.info(
            "Commit Manager initialized."
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

    def commit(
        self,
        message: str,
    ) -> subprocess.CompletedProcess[str]:
        """
        Create a Git commit.
        """

        return subprocess.run(
            [
                "git",
                "commit",
                "-m",
                message,
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

    ###########################################################################

    def amend(
        self,
        message: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """
        Amend the latest commit.
        """

        command = [
            "git",
            "commit",
            "--amend",
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

    def history(
        self,
        limit: int = 20,
    ) -> list[str]:
        """
        Return commit history.
        """

        result = subprocess.run(
            [
                "git",
                "log",
                f"-{limit}",
                "--oneline",
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

    def validate_message(
        self,
        message: str,
    ) -> bool:
        """
        Validate commit message.
        """

        return (
            bool(message.strip())
            and len(message) <= 72
        )
###############################################################################
# Conventional Commit
###############################################################################

    def conventional_commit(
        self,
        commit_type: str,
        description: str,
        scope: str | None = None,
    ) -> str:
        """
        Generate a Conventional Commit message.
        """

        if scope:

            return (
                f"{commit_type}"
                f"({scope}): {description}"
            )

        return (
            f"{commit_type}: {description}"
        )

###############################################################################
# AI Commit Message
###############################################################################

    def generate_message(
        self,
        summary: str,
    ) -> str:
        """
        Generate a commit message.

        Placeholder implementation.
        Future versions will integrate with
        the AI Code Review Engine and LLMs.
        """

        return self.conventional_commit(
            commit_type="feat",
            description=summary.strip(),
        )

###############################################################################
# Commit Metadata
###############################################################################

    def metadata(
        self,
        reference: str = "HEAD",
    ) -> dict[str, str]:
        """
        Return commit metadata.
        """

        result = subprocess.run(
            [
                "git",
                "show",
                "--quiet",
                "--format=%H%n%an%n%ae%n%ad%n%s",
                reference,
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

        lines = result.stdout.splitlines()

        return {
            "hash": lines[0] if len(lines) > 0 else "",
            "author": lines[1] if len(lines) > 1 else "",
            "email": lines[2] if len(lines) > 2 else "",
            "date": lines[3] if len(lines) > 3 else "",
            "subject": lines[4] if len(lines) > 4 else "",
        }

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return commit statistics.
        """

        history = self.history()

        return {
            "commit_count": len(history),
            "latest_commit": (
                history[0]
                if history
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
        Return commit manager report.
        """

        return {
            "statistics": self.statistics(),
            "history": self.history(),
        }

###############################################################################
# Global Commit Manager
###############################################################################

commit_manager = CommitManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "CommitManager",
    "commit_manager",
]