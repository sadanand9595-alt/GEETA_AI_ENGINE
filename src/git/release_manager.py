"""
==============================================================================
GEETA AI Engine

File        : release_manager.py
Package     : git
Description : Release Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import subprocess
from typing import Any

from config.logger import get_logger

from git.commit_manager import commit_manager
from git.diff_manager import diff_manager
from git.tag_manager import tag_manager

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Release Manager
###############################################################################


class ReleaseManager:
    """
    High-level release manager.

    Responsibilities

    - Release creation
    - Semantic versioning
    - Changelog generation
    - Release notes
    - Tag integration
    - Release validation
    """

    def __init__(self) -> None:

        logger.info(
            "Release Manager initialized."
        )

    ###########################################################################

    def create_release(
        self,
        version: str,
        message: str,
        annotated: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        """
        Create a Git release tag.
        """

        if annotated:

            return tag_manager.create_annotated(
                version,
                message,
            )

        return tag_manager.create(
            version,
        )

    ###########################################################################

    def changelog(
        self,
        limit: int = 20,
    ) -> str:
        """
        Generate a changelog.
        """

        commits = commit_manager.history(
            limit=limit,
        )

        return "\n".join(
            f"- {commit}"
            for commit in commits
        )

    ###########################################################################

    def release_notes(
        self,
        limit: int = 20,
    ) -> str:
        """
        Generate release notes.
        """

        return (
            "Release Notes\n"
            "=============\n\n"
            + self.changelog(limit)
        )

    ###########################################################################

    def validate(
        self,
    ) -> bool:
        """
        Validate release readiness.
        """

        stats = diff_manager.statistics()

        return (
            stats["files_changed"] == 0
        )
###############################################################################
# Semantic Version
###############################################################################

    def latest_version(
        self,
    ) -> str | None:
        """
        Return the latest release version.
        """

        return tag_manager.latest_version()

    ###########################################################################

    def next_patch_version(
        self,
    ) -> str:
        """
        Calculate the next patch version.

        Placeholder implementation.
        Future versions will implement
        complete Semantic Versioning.
        """

        latest = self.latest_version()

        if latest is None:

            return "v0.1.0"

        return latest

###############################################################################
# AI Release Summary
###############################################################################

    def summary(
        self,
        limit: int = 20,
    ) -> str:
        """
        Generate a release summary.

        Placeholder implementation.
        Future versions will integrate
        with the AI Engine.
        """

        commits = commit_manager.history(
            limit,
        )

        return (
            f"Release contains "
            f"{len(commits)} commit(s)."
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return release statistics.
        """

        return {
            "latest_version": (
                self.latest_version()
            ),
            "release_ready": (
                self.validate()
            ),
            "commit_count": len(
                commit_manager.history()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return release manager report.
        """

        return {
            "statistics": self.statistics(),
            "summary": self.summary(),
            "release_notes": (
                self.release_notes()
            ),
        }

###############################################################################
# Global Release Manager
###############################################################################

release_manager = ReleaseManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "ReleaseManager",
    "release_manager",
]