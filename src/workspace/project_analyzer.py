"""
==============================================================================
GEETA AI Engine

File        : project_analyzer.py
Package     : workspace
Description : Project Analyzer

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from config.logger import get_logger
from workspace.workspace_manager import workspace_manager

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Project Analyzer
###############################################################################


class ProjectAnalyzer:
    """
    Performs static analysis of an entire workspace.

    Responsibilities

    - Project discovery
    - Framework detection
    - Language detection
    - Dependency analysis
    - Entry point detection
    - Architecture analysis
    """

    def __init__(self) -> None:

        logger.info(
            "Project Analyzer initialized."
        )

    ###########################################################################

    def analyze(
        self,
    ) -> dict[str, Any]:
        """
        Analyze the current workspace.
        """

        if not workspace_manager.is_open():

            raise RuntimeError(
                "No workspace is open."
            )

        return {
            "workspace": str(
                workspace_manager.workspace
            ),
            "project_type": (
                workspace_manager.detect_project_type()
            ),
            "languages": self.detect_languages(),
            "entry_points": self.find_entry_points(),
            "statistics": self.statistics(),
        }

    ###########################################################################

    def detect_languages(
        self,
    ) -> list[str]:
        """
        Detect programming languages.
        """

        extensions = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".cpp": "C++",
            ".c": "C",
            ".cs": "C#",
            ".java": "Java",
            ".go": "Go",
            ".rs": "Rust",
        }

        languages: set[str] = set()

        for file in workspace_manager.scan_files():

            language = extensions.get(
                file.suffix.lower()
            )

            if language:

                languages.add(language)

        return sorted(languages)

    ###########################################################################

    def find_entry_points(
        self,
    ) -> list[Path]:
        """
        Locate probable project entry points.
        """

        candidates = {
            "main.py",
            "app.py",
            "manage.py",
            "run.py",
            "index.js",
            "server.js",
            "main.rs",
            "Program.cs",
        }

        result: list[Path] = []

        for file in workspace_manager.scan_files():

            if file.name in candidates:

                result.append(file)

        return result
###############################################################################
# Dependency Analysis
###############################################################################

    def dependency_summary(
        self,
    ) -> dict[str, int]:
        """
        Return a simple dependency summary.

        A full dependency graph will be implemented
        by the Dependency Graph Engine.
        """

        return {
            "source_files": len(
                workspace_manager.scan_files("*.py")
            ),
            "entry_points": len(
                self.find_entry_points()
            ),
        }

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return project statistics.
        """

        files = workspace_manager.scan_files()

        return {
            "files": len(files),
            "languages": len(
                self.detect_languages()
            ),
            "entry_points": len(
                self.find_entry_points()
            ),
        }

###############################################################################
# Project Summary
###############################################################################

    def summary(
        self,
    ) -> str:
        """
        Return project summary.
        """

        project_type = (
            workspace_manager.detect_project_type()
        )

        return (
            f"{project_type} project with "
            f"{len(self.detect_languages())} "
            f"language(s) and "
            f"{len(self.find_entry_points())} "
            f"entry point(s)."
        )

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return complete project analysis report.
        """

        return {
            "analysis": self.analyze(),
            "dependency_summary": (
                self.dependency_summary()
            ),
            "summary": self.summary(),
        }


###############################################################################
# Global Analyzer
###############################################################################

project_analyzer = ProjectAnalyzer()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "ProjectAnalyzer",
    "project_analyzer",
]