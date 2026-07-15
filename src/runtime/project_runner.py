"""
==============================================================================
GEETA AI Engine

File        : project_runner.py
Package     : runtime
Description : Project Runner

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from config.logger import get_logger

from runtime.execution_engine import execution_engine
from workspace.project_analyzer import project_analyzer
from workspace.workspace_manager import workspace_manager

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Project Runner
###############################################################################


class ProjectRunner:
    """
    Executes complete software projects.

    Responsibilities

    - Project detection
    - Entry-point discovery
    - Build execution
    - Application launch
    - Test execution
    - Runtime diagnostics
    """

    def __init__(self) -> None:

        logger.info(
            "Project Runner initialized."
        )

    ###########################################################################

    def run(
        self,
    ) -> int:
        """
        Run the current project.
        """

        if not workspace_manager.is_open():

            raise RuntimeError(
                "No workspace is open."
            )

        entry = self.entry_point()

        if entry is None:

            raise RuntimeError(
                "Project entry point not found."
            )

        logger.info(
            "Running project: %s",
            entry,
        )

        return execution_engine.execute_command(
            f'python "{entry}"',
            cwd=workspace_manager.workspace,
        )

    ###########################################################################

    def entry_point(
        self,
    ) -> Path | None:
        """
        Return the primary entry point.
        """

        entries = (
            project_analyzer.find_entry_points()
        )

        if entries:

            return entries[0]

        return None

    ###########################################################################

    def run_tests(
        self,
    ) -> int:
        """
        Execute project tests.
        """

        return execution_engine.run_tests(
            workspace_manager.workspace
            or ".",
        )

    ###########################################################################

    def diagnose(
        self,
        source: str,
        error: str,
    ) -> str:
        """
        Perform runtime diagnostics.
        """

        return execution_engine.diagnose(
            source,
            error,
        )
###############################################################################
# Build Support
###############################################################################

    def build(
        self,
    ) -> int:
        """
        Build the current project.

        Placeholder implementation.
        Future versions will support
        Python, Node.js, Rust, Go,
        Java and C/C++ build systems.
        """

        logger.info(
            "Building project..."
        )

        return 0

###############################################################################
# Development Server
###############################################################################

    def run_development_server(
        self,
        command: str,
    ) -> int:
        """
        Start a development server.
        """

        logger.info(
            "Starting development server..."
        )

        return execution_engine.execute_command(
            command,
            cwd=workspace_manager.workspace,
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return project runner statistics.
        """

        return {
            "project_type": (
                workspace_manager.detect_project_type()
            ),
            "entry_point": (
                str(self.entry_point())
                if self.entry_point()
                else None
            ),
            "workspace_open": (
                workspace_manager.is_open()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return project runner report.
        """

        return {
            "statistics": self.statistics(),
            "analysis": (
                project_analyzer.report()
            ),
            "execution": (
                execution_engine.report()
            ),
        }

###############################################################################
# Global Project Runner
###############################################################################

project_runner = ProjectRunner()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "ProjectRunner",
    "project_runner",
]