"""
==============================================================================
GEETA AI Engine

File        : project_index.py
Package     : workspace
Description : Project Index

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Any

from config.logger import get_logger

from workspace.workspace_manager import workspace_manager
from workspace.project_analyzer import project_analyzer
from workspace.context_builder import context_builder
from workspace.dependency_graph import dependency_graph

from memory.project_memory import ProjectMemory
from memory.semantic_memory import SemanticMemory
from memory.symbol_memory import SymbolMemory

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Project Index
###############################################################################


class ProjectIndex:
    """
    Central AI project index.

    Responsibilities

    - Workspace indexing
    - AI context aggregation
    - Symbol indexing
    - Semantic indexing
    - Dependency graph integration
    - Project memory synchronization
    """

    def __init__(self) -> None:

        self._project_memory = ProjectMemory()

        self._semantic_memory = SemanticMemory()

        self._symbol_memory = SymbolMemory()

        logger.info(
            "Project Index initialized."
        )

    ###########################################################################

    def build(
        self,
    ) -> None:
        """
        Build complete project index.
        """

        logger.info(
            "Building project index..."
        )

        dependency_graph.build()

        analysis = project_analyzer.report()

        self._project_memory.store(
            "analysis",
            analysis,
        )

        self._project_memory.store(
            "workspace",
            workspace_manager.report(),
        )

        logger.info(
            "Project index built."
        )

    ###########################################################################

    def context(
        self,
        request: str,
    ) -> dict[str, Any]:
        """
        Return AI-ready project context.
        """

        return context_builder.build(
            request,
        )

    ###########################################################################

    def analysis(
        self,
    ) -> dict[str, Any]:
        """
        Return cached project analysis.
        """

        return self._project_memory.retrieve(
            "analysis",
        )
###############################################################################
# Index Management
###############################################################################

    def refresh(
        self,
    ) -> None:
        """
        Refresh the project index.
        """

        logger.info(
            "Refreshing project index..."
        )

        self.build()

    ###########################################################################

    def clear(
        self,
    ) -> None:
        """
        Clear cached project information.
        """

        self._project_memory.clear()

        self._semantic_memory.clear()

        self._symbol_memory.clear()

        logger.info(
            "Project index cleared."
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return project index statistics.
        """

        return {
            "workspace": workspace_manager.statistics(),
            "analysis": project_analyzer.statistics(),
            "dependencies": dependency_graph.statistics(),
            "project_memory": (
                self._project_memory.statistics()
            ),
            "semantic_memory": (
                self._semantic_memory.statistics()
            ),
            "symbol_memory": (
                self._symbol_memory.statistics()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return complete project index report.
        """

        return {
            "analysis": self.analysis(),
            "statistics": self.statistics(),
            "dependency_graph": (
                dependency_graph.report()
            ),
            "workspace": (
                workspace_manager.report()
            ),
        }

###############################################################################
# Global Project Index
###############################################################################

project_index = ProjectIndex()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "ProjectIndex",
    "project_index",
]