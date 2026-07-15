"""
==============================================================================
GEETA AI Engine

File        : index_pipeline.py
Package     : workspace
Description : Workspace Index Pipeline

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import time
from typing import Any

from config.logger import get_logger

from workspace.workspace_manager import workspace_manager
from workspace.project_analyzer import project_analyzer
from workspace.dependency_graph import dependency_graph
from workspace.project_index import project_index
from workspace.context_builder import context_builder

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Index Pipeline
###############################################################################


class IndexPipeline:
    """
    Master indexing pipeline.

    Responsibilities

    - Workspace indexing
    - Project analysis
    - Dependency graph
    - Project memory
    - Semantic indexing
    - Context refresh
    """

    def __init__(self) -> None:

        self._last_index_time: float = 0.0

        self._running = False

        logger.info(
            "Index Pipeline initialized."
        )

    ###########################################################################

    def full_index(
        self,
    ) -> None:
        """
        Execute complete indexing pipeline.
        """

        logger.info(
            "Starting full project indexing..."
        )

        self._running = True

        start = time.perf_counter()

        dependency_graph.build()

        project_index.build()

        project_analyzer.report()

        context_builder.statistics()

        self._last_index_time = (
            time.perf_counter() - start
        )

        self._running = False

        logger.info(
            "Index completed in %.3f sec",
            self._last_index_time,
        )

    ###########################################################################

    def incremental_index(
        self,
    ) -> None:
        """
        Perform incremental indexing.
        """

        logger.info(
            "Running incremental index..."
        )

        project_index.refresh()

    ###########################################################################

    @property
    def running(
        self,
    ) -> bool:
        """
        Return pipeline status.
        """

        return self._running
###############################################################################
# Pipeline Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return pipeline statistics.
        """

        return {
            "running": self._running,
            "last_index_time": round(
                self._last_index_time,
                3,
            ),
            "workspace_open": (
                workspace_manager.is_open()
            ),
        }

###############################################################################
# Progress
###############################################################################

    def progress(
        self,
    ) -> dict[str, Any]:
        """
        Return current indexing progress.
        """

        return {
            "status": (
                "Running"
                if self._running
                else "Idle"
            ),
            "completion": (
                0
                if self._running
                else 100
            ),
        }

###############################################################################
# Error Recovery
###############################################################################

    def safe_index(
        self,
    ) -> bool:
        """
        Execute indexing with error recovery.
        """

        try:

            self.full_index()

            return True

        except Exception:

            logger.exception(
                "Index pipeline failed."
            )

            self._running = False

            return False

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return complete pipeline report.
        """

        return {
            "statistics": self.statistics(),
            "progress": self.progress(),
            "workspace": (
                workspace_manager.report()
            ),
            "project": (
                project_index.report()
            ),
        }

###############################################################################
# Global Pipeline
###############################################################################

index_pipeline = IndexPipeline()

###############################################################################
# Helper Functions
###############################################################################

def rebuild_project() -> bool:
    """
    Execute a complete project rebuild.
    """

    return index_pipeline.safe_index()


###############################################################################
# Exports
###############################################################################

__all__ = [
    "IndexPipeline",
    "index_pipeline",
    "rebuild_project",
]