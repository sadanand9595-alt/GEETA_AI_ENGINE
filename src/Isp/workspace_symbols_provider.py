"""
==============================================================================
GEETA AI IDE

File        : workspace_symbols_provider.py
Package     : lsp
Description : LSP Workspace Symbols Provider

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
# Workspace Symbol
###############################################################################


@dataclass(slots=True)
class WorkspaceSymbol:
    """
    Represents a workspace symbol.
    """

    name: str

    kind: str

    uri: str

    line: int

    character: int

    container_name: str = ""

###############################################################################
# Workspace Symbols Provider
###############################################################################


class WorkspaceSymbolsProvider:
    """
    LSP Workspace Symbols Provider.

    Responsibilities

    - Workspace symbol search
    - Global navigation
    - Fuzzy search
    - Symbol cache
    - Cross-file discovery
    """

    ###########################################################################

    def __init__(
        self,
        client: LSPClient,
    ) -> None:

        self._client = client

        self._cache: dict[
            str,
            list[WorkspaceSymbol],
        ] = {}

        logger.info(
            "Workspace Symbols Provider initialized."
        )

###############################################################################
# Request
###############################################################################

    def request(
        self,
        query: str,
    ) -> int:
        """
        Request workspace symbols.
        """

        return self._client.send_request(
            "workspace/symbol",
            {
                "query": query,
            },
        )

###############################################################################
# Cache
###############################################################################

    def cache(
        self,
        query: str,
        symbols: list[
            WorkspaceSymbol
        ],
    ) -> None:
        """
        Cache workspace symbol results.
        """

        self._cache[
            query
        ] = symbols

###############################################################################
# Lookup
###############################################################################

    def cached(
        self,
        query: str,
    ) -> list[
        WorkspaceSymbol
    ]:
        """
        Return cached workspace symbols.
        """

        return list(
            self._cache.get(
                query,
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
        Clear workspace symbol cache.
        """

        self._cache.clear()
###############################################################################
# Symbol Lookup
###############################################################################

    def find(
        self,
        query: str,
        name: str,
    ) -> WorkspaceSymbol | None:
        """
        Find a workspace symbol by name.
        """

        for symbol in self.cached(
            query,
        ):

            if symbol.name == name:

                return symbol

        return None

###############################################################################
# Fuzzy Filter
###############################################################################

    def fuzzy_search(
        self,
        query: str,
        pattern: str,
    ) -> list[WorkspaceSymbol]:
        """
        Perform simple fuzzy matching.
        """

        pattern = pattern.lower()

        return [
            symbol
            for symbol
            in self.cached(query)
            if pattern in symbol.name.lower()
        ]

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
            "cached_queries": len(
                self._cache
            ),
            "cached_symbols": sum(
                len(symbols)
                for symbols
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
            "queries": {
                query: len(symbols)
                for query, symbols
                in self._cache.items()
            },
        }

###############################################################################
# Global Provider
###############################################################################

workspace_symbols_provider: (
    WorkspaceSymbolsProvider | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "WorkspaceSymbol",
    "WorkspaceSymbolsProvider",
    "workspace_symbols_provider",
]