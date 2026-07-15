"""
==============================================================================
GEETA AI Engine

File        : git_diagnostics.py
Package     : git
Description : Git Diagnostics

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import shutil
import subprocess
from typing import Any

from config.logger import get_logger

from git.git_manager import git_manager
from git.git_monitor import git_monitor

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Git Diagnostics
###############################################################################


class GitDiagnostics:
    """
    Git diagnostics service.

    Responsibilities

    - Git installation validation
    - Repository validation
    - Working tree diagnostics
    - Branch diagnostics
    - Remote diagnostics
    - Health reporting
    """

    def __init__(self) -> None:

        logger.info(
            "Git Diagnostics initialized."
        )

    ###########################################################################

    def git_available(
        self,
    ) -> bool:
        """
        Check whether Git is installed.
        """

        return shutil.which(
            "git",
        ) is not None

    ###########################################################################

    def repository_available(
        self,
    ) -> bool:
        """
        Check whether a repository is open.
        """

        return (
            git_manager.repository()
            is not None
        )

    ###########################################################################

    def detached_head(
        self,
    ) -> bool:
        """
        Detect detached HEAD state.
        """

        repository = git_manager.repository()

        if repository is None:

            return False

        result = subprocess.run(
            [
                "git",
                "symbolic-ref",
                "--quiet",
                "HEAD",
            ],
            cwd=repository,
            text=True,
            capture_output=True,
            check=False,
        )

        return result.returncode != 0

    ###########################################################################

    def working_tree_clean(
        self,
    ) -> bool:
        """
        Check whether the working tree is clean.
        """

        repository = git_manager.repository()

        if repository is None:

            return False

        status = git_manager.status()

        return (
            status.stdout.strip() == ""
        )

    ###########################################################################

    def health(
        self,
    ) -> dict[str, Any]:
        """
        Return repository health.
        """

        return {
            "git_available": (
                self.git_available()
            ),
            "repository_available": (
                self.repository_available()
            ),
            "working_tree_clean": (
                self.working_tree_clean()
            ),
            "detached_head": (
                self.detached_head()
            ),
        }
###############################################################################
# Recommendations
###############################################################################

    def recommendations(
        self,
    ) -> list[str]:
        """
        Return diagnostic recommendations.
        """

        recommendations: list[str] = []

        if not self.git_available():

            recommendations.append(
                "Install Git and ensure it is available on PATH."
            )

        if not self.repository_available():

            recommendations.append(
                "Open or initialize a Git repository."
            )

        if (
            self.repository_available()
            and not self.working_tree_clean()
        ):

            recommendations.append(
                "Commit or stash pending changes."
            )

        if self.detached_head():

            recommendations.append(
                "Checkout a branch to leave detached HEAD state."
            )

        if not recommendations:

            recommendations.append(
                "Git repository is healthy."
            )

        return recommendations

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return Git diagnostics statistics.
        """

        health = self.health()

        return {
            "git_available": health["git_available"],
            "repository_available": (
                health["repository_available"]
            ),
            "working_tree_clean": (
                health["working_tree_clean"]
            ),
            "detached_head": (
                health["detached_head"]
            ),
            "monitor_running": (
                git_monitor.statistics()["running"]
            ),
            "recommendations": len(
                self.recommendations()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return complete diagnostics report.
        """

        return {
            "health": self.health(),
            "statistics": self.statistics(),
            "recommendations": (
                self.recommendations()
            ),
            "monitor": (
                git_monitor.report()
            ),
        }

###############################################################################
# Global Git Diagnostics
###############################################################################

git_diagnostics = GitDiagnostics()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "GitDiagnostics",
    "git_diagnostics",
]