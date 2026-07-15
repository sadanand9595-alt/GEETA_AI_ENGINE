"""
==============================================================================
GEETA AI Engine

File        : remote_manager.py
Package     : git
Description : Git Remote Manager

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
# Remote Manager
###############################################################################


class RemoteManager:
    """
    High-level Git remote manager.

    Responsibilities

    - Remote discovery
    - Add / Remove remotes
    - Fetch
    - Pull
    - Push
    - Remote health
    """

    def __init__(self) -> None:

        logger.info(
            "Remote Manager initialized."
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

    def list(
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
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

        return [
            remote.strip()
            for remote in result.stdout.splitlines()
            if remote.strip()
        ]

    ###########################################################################

    def add(
        self,
        name: str,
        url: str,
    ) -> subprocess.CompletedProcess[str]:
        """
        Add a remote.
        """

        return subprocess.run(
            [
                "git",
                "remote",
                "add",
                name,
                url,
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

    ###########################################################################

    def remove(
        self,
        name: str,
    ) -> subprocess.CompletedProcess[str]:
        """
        Remove a remote.
        """

        return subprocess.run(
            [
                "git",
                "remote",
                "remove",
                name,
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

    ###########################################################################

    def rename(
        self,
        old: str,
        new: str,
    ) -> subprocess.CompletedProcess[str]:
        """
        Rename a remote.
        """

        return subprocess.run(
            [
                "git",
                "remote",
                "rename",
                old,
                new,
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )
###############################################################################
# Fetch
###############################################################################

    def fetch(
        self,
        remote: str = "origin",
    ) -> subprocess.CompletedProcess[str]:
        """
        Fetch updates from a remote.
        """

        return subprocess.run(
            [
                "git",
                "fetch",
                remote,
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

###############################################################################
# Pull
###############################################################################

    def pull(
        self,
        remote: str = "origin",
        branch: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """
        Pull changes from a remote.
        """

        command = [
            "git",
            "pull",
            remote,
        ]

        if branch:

            command.append(branch)

        return subprocess.run(
            command,
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

###############################################################################
# Push
###############################################################################

    def push(
        self,
        remote: str = "origin",
        branch: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """
        Push changes to a remote.
        """

        command = [
            "git",
            "push",
            remote,
        ]

        if branch:

            command.append(branch)

        return subprocess.run(
            command,
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

###############################################################################
# Remote URLs
###############################################################################

    def urls(
        self,
    ) -> dict[str, str]:
        """
        Return configured remote URLs.
        """

        result = subprocess.run(
            [
                "git",
                "remote",
                "-v",
            ],
            cwd=self.repository,
            text=True,
            capture_output=True,
            check=False,
        )

        urls: dict[str, str] = {}

        for line in result.stdout.splitlines():

            parts = line.split()

            if len(parts) >= 2:

                urls[parts[0]] = parts[1]

        return urls

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return remote manager statistics.
        """

        remotes = self.list()

        return {
            "remote_count": len(remotes),
            "remotes": remotes,
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return remote manager report.
        """

        return {
            "statistics": self.statistics(),
            "urls": self.urls(),
        }

###############################################################################
# Global Remote Manager
###############################################################################

remote_manager = RemoteManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "RemoteManager",
    "remote_manager",
]