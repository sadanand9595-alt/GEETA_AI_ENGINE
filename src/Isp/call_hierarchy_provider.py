"""
==============================================================================
GEETA AI IDE

File        : call_hierarchy_provider.py
Package     : lsp
Description : LSP Call Hierarchy Provider

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from config.logger import get_logger
from lsp.lsp_client import LSPClient

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Call Hierarchy Item
###############################################################################


@dataclass(slots=True)
class CallHierarchyItem:
    """
    Represents a call hierarchy item.
    """

    name: str

    kind: str

    uri: str

    line: int

    character: int

###############################################################################
# Call Hierarchy
###############################################################################


@dataclass(slots=True)
class CallHierarchy:
    """
    Represents call hierarchy.
    """

    root: CallHierarchyItem

    incoming: list[
        CallHierarchyItem
    ] = field(
        default_factory=list,
    )

    outgoing: list[
        CallHierarchyItem
    ] = field(
        default_factory=list,
    )

###############################################################################
# Call Hierarchy Provider
###############################################################################


class CallHierarchyProvider:
    """
    LSP Call Hierarchy Provider.

    Responsibilities

    - Incoming calls
    - Outgoing calls
    - Call graph
    - Call hierarchy cache
    - Recursive call detection
    """

    ###########################################################################

    def __init__(
        self,
        client: LSPClient,
    ) -> None:

        self._client = client

        self._cache: dict[
            tuple[str, int, int],
            CallHierarchy,
        ] = {}

        logger.info(
            "Call Hierarchy Provider initialized."
        )

###############################################################################
# Prepare
###############################################################################

    def prepare(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> int:
        """
        Prepare call hierarchy.
        """

        return self._client.send_request(
            "textDocument/prepareCallHierarchy",
            {
                "textDocument": {
                    "uri": uri,
                },
                "position": {
                    "line": line,
                    "character": character,
                },
            },
        )

###############################################################################
# Incoming Calls
###############################################################################

    def incoming_calls(
        self,
        item: dict[str, Any],
    ) -> int:
        """
        Request incoming calls.
        """

        return self._client.send_request(
            "callHierarchy/incomingCalls",
            {
                "item": item,
            },
        )

###############################################################################
# Outgoing Calls
###############################################################################

    def outgoing_calls(
        self,
        item: dict[str, Any],
    ) -> int:
        """
        Request outgoing calls.
        """

        return self._client.send_request(
            "callHierarchy/outgoingCalls",
            {
                "item": item,
            },
        )

###############################################################################
# Cache
###############################################################################

    def cache(
        self,
        uri: str,
        line: int,
        character: int,
        hierarchy: CallHierarchy,
    ) -> None:
        """
        Cache call hierarchy.
        """

        self._cache[
            (
                uri,
                line,
                character,
            )
        ] = hierarchy
###############################################################################
# Lookup
###############################################################################

    def hierarchy(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> CallHierarchy | None:
        """
        Return cached call hierarchy.
        """

        return self._cache.get(
            (
                uri,
                line,
                character,
            )
        )

###############################################################################
# Recursive Call Detection
###############################################################################

    def is_recursive(
        self,
        hierarchy: CallHierarchy,
    ) -> bool:
        """
        Detect recursive calls.
        """

        root = hierarchy.root.name

        for item in hierarchy.outgoing:

            if item.name == root:

                return True

        return False

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return call hierarchy statistics.
        """

        return {
            "cached_hierarchies": len(
                self._cache
            ),
            "incoming_calls": sum(
                len(item.incoming)
                for item
                in self._cache.values()
            ),
            "outgoing_calls": sum(
                len(item.outgoing)
                for item
                in self._cache.values()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return call hierarchy report.
        """

        return {
            "statistics": self.statistics(),
            "hierarchies": [
                {
                    "uri": key[0],
                    "line": key[1],
                    "character": key[2],
                    "symbol": value.root.name,
                    "recursive": self.is_recursive(
                        value,
                    ),
                }
                for key, value
                in self._cache.items()
            ],
        }

###############################################################################
# Global Provider
###############################################################################

call_hierarchy_provider: (
    CallHierarchyProvider | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "CallHierarchyItem",
    "CallHierarchy",
    "CallHierarchyProvider",
    "call_hierarchy_provider",
]