"""
==============================================================================
GEETA AI IDE

File        : linked_editing_provider.py
Package     : lsp
Description : LSP Linked Editing Provider

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from config.logger import get_logger
from lsp.lsp_client import LSPClient

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Linked Editing Range
###############################################################################


@dataclass(slots=True)
class LinkedEditingRange:
    """
    Represents a linked editing range.
    """

    start_line: int

    start_character: int

    end_line: int

    end_character: int

###############################################################################
# Linked Editing Provider
###############################################################################


class LinkedEditingProvider:
    """
    Enterprise Linked Editing Provider.

    Responsibilities

    - Linked editing
    - HTML/XML tag editing
    - Paired symbol editing
    - Rename while typing
    - Cache management
    """

    ###########################################################################

    def __init__(
        self,
        client: LSPClient,
    ) -> None:

        self._client = client

        self._cache: dict[
            tuple[str, int, int],
            list[LinkedEditingRange],
        ] = {}

        logger.info(
            "Linked Editing Provider initialized."
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
        Request linked editing ranges.
        """

        return self._client.send_request(
            "textDocument/linkedEditingRange",
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
# Cache
###############################################################################

    def cache(
        self,
        uri: str,
        line: int,
        character: int,
        ranges: list[
            LinkedEditingRange
        ],
    ) -> None:
        """
        Cache linked editing ranges.
        """

        self._cache[
            (
                uri,
                line,
                character,
            )
        ] = ranges

###############################################################################
# Lookup
###############################################################################

    def cached(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> list[
        LinkedEditingRange
    ]:
        """
        Return cached linked editing ranges.
        """

        return list(
            self._cache.get(
                (
                    uri,
                    line,
                    character,
                ),
                [],
            )
        )

###############################################################################
# Clear Cache
###############################################################################

    def clear_cache(
        self,
    ) -> None:
        """
        Clear linked editing cache.
        """

        self._cache.clear()
###############################################################################
# Range Lookup
###############################################################################

    def range_at(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> LinkedEditingRange | None:
        """
        Return linked editing range at position.
        """

        for linked_range in self.cached(
            uri,
            line,
            character,
        ):

            if (
                linked_range.start_line
                <= line
                <= linked_range.end_line
            ):

                return linked_range

        return None

###############################################################################
# Active Linked Ranges
###############################################################################

    def active_ranges(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> list[LinkedEditingRange]:
        """
        Return active linked editing ranges.
        """

        return self.cached(
            uri,
            line,
            character,
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return provider statistics.
        """

        return {
            "cached_requests": len(
                self._cache
            ),
            "cached_ranges": sum(
                len(ranges)
                for ranges
                in self._cache.values()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
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
                    "ranges": len(value),
                }
                for key, value
                in self._cache.items()
            ],
        }

###############################################################################
# Global Provider
###############################################################################

linked_editing_provider: (
    LinkedEditingProvider | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "LinkedEditingRange",
    "LinkedEditingProvider",
    "linked_editing_provider",
]