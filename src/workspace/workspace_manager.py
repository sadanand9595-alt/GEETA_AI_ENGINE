"""
==============================================================================
GEETA AI Engine

File        : workspace_manager.py
Package     : workspace
Description : Workspace Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Workspace Manager
###############################################################################


class WorkspaceManager:
    """
    Central workspace manager.

    Responsibilities:

    - Workspace loading
    - Project scanning
    - File discovery
    - Background indexing
    - Workspace metadata
    - Context management
    """

    def __init__(self) -> None:

        self._workspace: Path | None = None

        self._metadata: dict[str, Any] = {}

        logger.info(
            "Workspace Manager initialized."
        )

    ###########################################################################

    def open_workspace(
        self,
        path: str | Path,
    ) -> None:
        """
        Open a workspace.
        """

        workspace = Path(path).resolve()

        if not workspace.exists():

            raise FileNotFoundError(
                workspace
            )

        self._workspace = workspace

        logger.info(
            "Workspace opened: %s",
            workspace,
        )

    ###########################################################################

    @property
    def workspace(
        self,
    ) -> Path | None:
        """
        Return current workspace.
        """

        return self._workspace

    ###########################################################################

    def is_open(
        self,
    ) -> bool:
        """
        Return True if a workspace is open.
        """

        return self._workspace is not None

    ###########################################################################

    def close_workspace(
        self,
    ) -> None:
        """
        Close current workspace.
        """

        logger.info(
            "Workspace closed."
        )

        self._workspace = None

        self._metadata.clear()

    ###########################################################################

    def metadata(
        self,
    ) -> dict[str, Any]:
        """
        Return workspace metadata.
        """

        return dict(
            self._metadata
        )
###############################################################################
# Workspace Scanning
###############################################################################

    def scan_files(
        self,
        pattern: str = "*",
    ) -> list[Path]:
        """
        Scan workspace recursively.
        """

        if self._workspace is None:

            return []

        return sorted(
            path
            for path in self._workspace.rglob(
                pattern,
            )
            if path.is_file()
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return workspace statistics.
        """

        files = self.scan_files()

        return {
            "workspace": (
                str(self._workspace)
                if self._workspace
                else None
            ),
            "total_files": len(files),
        }

###############################################################################
# Project Root Detection
###############################################################################

    def detect_project_type(
        self,
    ) -> str:
        """
        Detect project type.
        """

        if self._workspace is None:

            return "Unknown"

        if (
            self._workspace / "pyproject.toml"
        ).exists():

            return "Python"

        if (
            self._workspace / "package.json"
        ).exists():

            return "Node.js"

        if (
            self._workspace / "Cargo.toml"
        ).exists():

            return "Rust"

        return "Generic"

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return workspace report.
        """

        return {
            "metadata": self.metadata(),
            "statistics": self.statistics(),
            "project_type": (
                self.detect_project_type()
            ),
        }

###############################################################################
# Global Manager
###############################################################################

workspace_manager = WorkspaceManager()

###############################################################################
# Helper Functions
###############################################################################


def current_workspace() -> Path | None:
    """
    Return active workspace.
    """

    return workspace_manager.workspace


###############################################################################
# Exports
###############################################################################

__all__ = [
    "WorkspaceManager",
    "workspace_manager",
    "current_workspace",
]