"""
==============================================================================
GEETA AI Engine

File        : outline_view.py
Package     : editor
Description : Outline View

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Outline Node
###############################################################################


@dataclass(slots=True)
class OutlineNode:
    """
    Represents a document symbol.
    """

    name: str

    kind: str

    line: int

    column: int = 0

    children: list["OutlineNode"] = field(
        default_factory=list,
    )

    expanded: bool = True

###############################################################################
# Outline View
###############################################################################


class OutlineView:
    """
    Document outline manager.

    Responsibilities

    - Symbol tree
    - Hierarchical navigation
    - Expand/Collapse
    - Search
    - Document structure
    """

    def __init__(
        self,
    ) -> None:

        self._nodes: list[
            OutlineNode
        ] = []

        logger.info(
            "Outline View initialized."
        )

###############################################################################
# Node Management
###############################################################################

    def add_node(
        self,
        node: OutlineNode,
    ) -> None:
        """
        Add an outline node.
        """

        self._nodes.append(
            node,
        )

    ###########################################################################

    def clear(
        self,
    ) -> None:
        """
        Clear outline.
        """

        self._nodes.clear()

###############################################################################
# Lookup
###############################################################################

    def nodes(
        self,
    ) -> list[OutlineNode]:
        """
        Return root nodes.
        """

        return list(
            self._nodes
        )

###############################################################################
# Search
###############################################################################

    def search(
        self,
        text: str,
    ) -> list[OutlineNode]:
        """
        Search outline nodes.
        """

        query = text.lower()

        return [
            node
            for node
            in self._nodes
            if query in node.name.lower()
        ]

###############################################################################
# Expand / Collapse
###############################################################################

    def expand_all(
        self,
    ) -> None:
        """
        Expand all nodes.
        """

        for node in self._nodes:

            node.expanded = True

    ###########################################################################

    def collapse_all(
        self,
    ) -> None:
        """
        Collapse all nodes.
        """

        for node in self._nodes:

            node.expanded = False
###############################################################################
# Recursive Traversal
###############################################################################

    def walk(
        self,
    ) -> list[OutlineNode]:
        """
        Return every outline node.
        """

        result: list[
            OutlineNode
        ] = []

        def visit(
            node: OutlineNode,
        ) -> None:

            result.append(
                node,
            )

            for child in node.children:

                visit(
                    child,
                )

        for node in self._nodes:

            visit(
                node,
            )

        return result

###############################################################################
# Lookup
###############################################################################

    def node_at_line(
        self,
        line: int,
    ) -> OutlineNode | None:
        """
        Return the closest symbol for a line.
        """

        candidate: OutlineNode | None = None

        for node in self.walk():

            if node.line <= line:

                if (
                    candidate is None
                    or node.line > candidate.line
                ):

                    candidate = node

        return candidate

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return outline statistics.
        """

        return {
            "root_nodes": len(
                self._nodes
            ),
            "total_nodes": len(
                self.walk()
            ),
            "expanded_nodes": sum(
                node.expanded
                for node
                in self.walk()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return outline report.
        """

        return {
            "statistics": (
                self.statistics()
            ),
            "symbols": [
                {
                    "name": node.name,
                    "kind": node.kind,
                    "line": node.line,
                    "expanded": node.expanded,
                }
                for node
                in self.walk()
            ],
        }

###############################################################################
# Global Outline View
###############################################################################

outline_view = OutlineView()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "OutlineNode",
    "OutlineView",
    "outline_view",
]