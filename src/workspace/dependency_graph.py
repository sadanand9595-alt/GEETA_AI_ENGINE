"""
==============================================================================
GEETA AI Engine

File        : dependency_graph.py
Package     : workspace
Description : Dependency Graph

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from config.logger import get_logger
from workspace.workspace_manager import workspace_manager

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Dependency Graph
###############################################################################


class DependencyGraph:
    """
    Project dependency graph.

    Responsibilities

    - Module dependencies
    - Import graph
    - Include graph
    - Cross-file references
    - Circular dependency detection
    - Architecture graph
    """

    def __init__(self) -> None:

        self._graph: dict[
            str,
            set[str],
        ] = defaultdict(set)

        logger.info(
            "Dependency Graph initialized."
        )

    ###########################################################################

    def add_dependency(
        self,
        source: str,
        target: str,
    ) -> None:
        """
        Register dependency.
        """

        self._graph[source].add(
            target,
        )

    ###########################################################################

    def dependencies(
        self,
        source: str,
    ) -> list[str]:
        """
        Return direct dependencies.
        """

        return sorted(
            self._graph.get(
                source,
                set(),
            )
        )

    ###########################################################################

    def nodes(
        self,
    ) -> list[str]:
        """
        Return graph nodes.
        """

        return sorted(
            self._graph.keys()
        )

    ###########################################################################

    def build(
        self,
    ) -> None:
        """
        Build dependency graph.

        Full AST-based dependency analysis
        will be implemented in the parser
        pipeline.
        """

        self._graph.clear()

        for file in workspace_manager.scan_files(
            "*.py",
        ):

            self._graph[
                str(file)
            ]

        logger.info(
            "Dependency graph built."
        )

    ###########################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return graph statistics.
        """

        edges = sum(
            len(value)
            for value in self._graph.values()
        )

        return {
            "nodes": len(
                self._graph
            ),
            "edges": edges,
        }
###############################################################################
# Reverse Dependencies
###############################################################################

    def reverse_dependencies(
        self,
        target: str,
    ) -> list[str]:
        """
        Return all nodes that depend on the target.
        """

        result: list[str] = []

        for source, dependencies in self._graph.items():

            if target in dependencies:

                result.append(source)

        return sorted(result)


###############################################################################
# Circular Dependency Detection
###############################################################################

    def has_cycle(
        self,
    ) -> bool:
        """
        Detect circular dependencies.

        Uses depth-first search.
        """

        visited: set[str] = set()

        active: set[str] = set()

        def dfs(node: str) -> bool:

            if node in active:
                return True

            if node in visited:
                return False

            visited.add(node)

            active.add(node)

            for dependency in self._graph.get(
                node,
                set(),
            ):

                if dfs(dependency):

                    return True

            active.remove(node)

            return False

        for node in self._graph:

            if dfs(node):

                return True

        return False


###############################################################################
# Impact Analysis
###############################################################################

    def impact_analysis(
        self,
        node: str,
    ) -> dict[str, Any]:
        """
        Return dependency impact information.
        """

        return {
            "node": node,
            "depends_on": self.dependencies(
                node,
            ),
            "used_by": self.reverse_dependencies(
                node,
            ),
        }


###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return dependency graph report.
        """

        return {
            "statistics": self.statistics(),
            "nodes": self.nodes(),
            "has_cycle": self.has_cycle(),
        }


###############################################################################
# Global Graph
###############################################################################

dependency_graph = DependencyGraph()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "DependencyGraph",
    "dependency_graph",
]