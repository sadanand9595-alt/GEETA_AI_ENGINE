"""
==============================================================================
GEETA AI IDE

File        : selection_range_provider.py
Package     : lsp
Description : LSP Selection Range Provider

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from config.logger import get_logger
from lsp.lsp_client import LSPClient

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Selection Range
###############################################################################


@dataclass(slots=True)
class SelectionRange:
    """
    Represents an LSP selection range.
    """

    start_line: int

    start_character: int

    end_line: int

    end_character: int

    parent: "SelectionRange | None" = None

###############################################################################
# Selection Range Provider
###############################################################################


class SelectionRangeProvider:
    """
    Enterprise Selection Range Provider.

    Responsibilities

    - Expand Selection
    - Shrink Selection
    - Nested selections
    - AST-aware selections
    - Selection cache
    """

    ###########################################################################

    def __init__(
        self,
        client: LSPClient,
    ) -> None:

        self._client = client

        self._cache: dict[
            tuple[str, int, int],
            SelectionRange,
        ] = {}

        logger.info(
            "Selection Range Provider initialized."
        )

###############################################################################
# Request
###############################################################################

    def request(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> int:
        """
        Request selection range.
        """

        return self._client.send_request(
            "textDocument/selectionRange",
            {
                "textDocument": {
                    "uri": uri,
                },
                "positions": [
                    {
                        "line": line,
                        "character": character,
                    }
                ],
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
        selection: SelectionRange,
    ) -> None:
        """
        Cache selection range.
        """

        self._cache[
            (
                uri,
                line,
                character,
            )
        ] = selection

###############################################################################
# Lookup
###############################################################################

    def cached(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> SelectionRange | None:
        """
        Return cached selection range.
        """

        return self._cache.get(
            (
                uri,
                line,
                character,
            )
        )

###############################################################################
# Clear Cache
###############################################################################

    def clear_cache(
        self,
    ) -> None:
        """
        Clear selection range cache.
        """

        self._cache.clear()
###############################################################################
# Expand Selection
###############################################################################

    def expand(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> SelectionRange | None:
        """
        Expand selection to its parent.
        """

        selection = self.cached(
            uri,
            line,
            character,
        )

        if selection is None:

            return None

        return selection.parent

###############################################################################
# Shrink Selection
###############################################################################

    def shrink(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> SelectionRange | None:
        """
        Return the smallest cached selection.
        """

        return self.cached(
            uri,
            line,
            character,
        )

###############################################################################
# Selection Hierarchy
###############################################################################

    def hierarchy(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> list[SelectionRange]:
        """
        Return the complete selection hierarchy.
        """

        result: list[
            SelectionRange
        ] = []

        selection = self.cached(
            uri,
            line,
            character,
        )

        while selection is not None:

            result.append(
                selection,
            )

            selection = selection.parent

        return result

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return provider statistics.
        """

        return {
            "cached_requests": len(
                self._cache
            ),
            "selection_hierarchies": sum(
                len(
                    self.hierarchy(
                        uri,
                        line,
                        character,
                    )
                )
                for (
                    uri,
                    line,
                    character,
                )
                in self._cache.keys()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return provider report.
        """

        return {
            "statistics": self.statistics(),
            "cached": [
                {
                    "uri": key[0],
                    "line": key[1],
                    "character": key[2],
                    "depth": len(
                        self.hierarchy(
                            key[0],
                            key[1],
                            key[2],
                        )
                    ),
                }
                for key
                in self._cache
            ],
        }

###############################################################################
# Global Provider
###############################################################################

selection_range_provider: (
    SelectionRangeProvider | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "SelectionRange",
    "SelectionRangeProvider",
    "selection_range_provider",
]