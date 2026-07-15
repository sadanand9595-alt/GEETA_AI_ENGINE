"""
==============================================================================
GEETA AI Engine

File        : tag_manager.py
Package     : git
Description : Git Tag Manager

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
# Tag Manager
###############################################################################


class TagManager:
    """
    High-level Git tag manager.

    Responsibilities

    - Lightweight tags
    - Annotated tags
    - Tag deletion
    - Tag inspection
    - Semantic version tags
    - Release management
    """

    def __init__(self) -> None:

        logger.info(
            "Tag Manager initialized."
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
        Create a lightweight tag.
        """

        return subprocess.run(
            [
                "git",
                "tag",
                name,
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

    ###########################################################################

    def create_annotated(
        self,
        name: str,
        message: str,
    ) -> subprocess.CompletedProcess[str]:
        """
        Create an annotated tag.
        """

        return subprocess.run(
            [
                "git",
                "tag",
                "-a",
                name,
                "-m",
                message,
            ],
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
        Return repository tags.
        """

        result = subprocess.run(
            [
                "git",
                "tag",
            ],
            cwd=self.repository,
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

    def delete(
        self,
        name: str,
    ) -> subprocess.CompletedProcess[str]:
        """
        Delete a local tag.
        """

        return subprocess.run(
            [
                "git",
                "tag",
                "-d",
                name,
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )
###############################################################################
# Tag Inspection
###############################################################################

    def show(
        self,
        name: str,
    ) -> str:
        """
        Show tag information.
        """

        result = subprocess.run(
            [
                "git",
                "show",
                "--no-patch",
                name,
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

        return result.stdout

###############################################################################
# Remote Tag Operations
###############################################################################

    def push(
        self,
        name: str,
        remote: str = "origin",
    ) -> subprocess.CompletedProcess[str]:
        """
        Push a tag to a remote.
        """

        return subprocess.run(
            [
                "git",
                "push",
                remote,
                name,
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

    ###########################################################################

    def delete_remote(
        self,
        name: str,
        remote: str = "origin",
    ) -> subprocess.CompletedProcess[str]:
        """
        Delete a remote tag.
        """

        return subprocess.run(
            [
                "git",
                "push",
                remote,
                "--delete",
                name,
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

###############################################################################
# Semantic Version Helper
###############################################################################

    def latest_version(self) -> str | None:
        """
        Return the latest semantic version tag.

        This implementation performs a
        lexicographical sort. Future versions
        will support full semantic versioning.
        """

        tags = sorted(
            self.list(),
        )

        if not tags:

            return None

        return tags[-1]

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return tag statistics.
        """

        tags = self.list()

        return {
            "tag_count": len(tags),
            "latest_tag": self.latest_version(),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return tag manager report.
        """

        return {
            "statistics": self.statistics(),
            "tags": self.list(),
        }

###############################################################################
# Global Tag Manager
###############################################################################

tag_manager = TagManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "TagManager",
    "tag_manager",
]