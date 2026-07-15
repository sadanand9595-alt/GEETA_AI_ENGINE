"""
==============================================================================
GEETA AI IDE

File        : folding_range_provider.py
Package     : lsp
Description : LSP Folding Range Provider

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
# Folding Range
###############################################################################


@dataclass(slots=True)
class FoldingRange:
    """
    Represents an LSP folding range.
    """

    start_line: int

    end_line: int

    start_character: int | None = None

    end_character: int | None = None

    kind: str = "region"

    collapsed_text: str = ""

###############################################################################
# Folding Range Provider
###############################################################################


class FoldingRangeProvider:
    """
    Enterprise Folding Range Provider.

    Responsibilities

    - Region folding
    - Import folding
    - Comment folding
    - Custom regions
    - Folding cache
    """

    ###########################################################################

    def __init__(
        self,
        client: LSPClient,
    ) -> None:

        self._client = client

        self._cache: dict[
            str,
            list[FoldingRange],
        ] = {}

        logger.info(
            "Folding Range Provider initialized."
        )

###############################################################################
# Request
###############################################################################

    def request(
        self,
        uri: str,
    ) -> int:
        """
        Request folding ranges.
        """

        return self._client.send_request(
            "textDocument/foldingRange",
            {
                "textDocument": {
                    "uri": uri,
                }
            },
        )

###############################################################################
# Cache
###############################################################################

    def cache(
        self,
        uri: str,
        ranges: list[FoldingRange],
    ) -> None:
        """
        Cache folding ranges.
        """

        self._cache[
            uri
        ] = ranges

###############################################################################
# Lookup
###############################################################################

    def cached(
        self,
        uri: str,
    ) -> list[FoldingRange]:
        """
        Return cached folding ranges.
        """

        return list(
            self._cache.get(
                uri,
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
        Clear folding cache.
        """

        self._cache.clear()
###############################################################################
# Range Lookup
###############################################################################

    def range_at(
        self,
        uri: str,
        line: int,
    ) -> FoldingRange | None:
        """
        Return folding range containing the given line.
        """

        for folding_range in self.cached(
            uri,
        ):

            if (
                folding_range.start_line
                <= line
                <= folding_range.end_line
            ):

                return folding_range

        return None

###############################################################################
# Filter
###############################################################################

    def by_kind(
        self,
        uri: str,
        kind: str,
    ) -> list[FoldingRange]:
        """
        Return folding ranges filtered by kind.
        """

        return [
            folding_range
            for folding_range
            in self.cached(uri)
            if folding_range.kind == kind
        ]

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return folding statistics.
        """

        return {
            "cached_documents": len(
                self._cache
            ),
            "cached_ranges": sum(
                len(ranges)
                for ranges
                in self._cache.values()
            ),
            "region_ranges": sum(
                len(
                    [
                        r
                        for r in ranges
                        if r.kind == "region"
                    ]
                )
                for ranges
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
        Return provider report.
        """

        return {
            "statistics": self.statistics(),
            "documents": {
                uri: len(ranges)
                for uri, ranges
                in self._cache.items()
            },
        }

###############################################################################
# Global Provider
###############################################################################

folding_range_provider: (
    FoldingRangeProvider | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "FoldingRange",
    "FoldingRangeProvider",
    "folding_range_provider",
]