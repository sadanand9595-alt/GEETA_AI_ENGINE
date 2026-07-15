"""
==============================================================================
GEETA AI IDE

File        : document_symbols_provider.py
Package     : lsp
Description : LSP Document Symbols Provider

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
# Document Symbol
###############################################################################


@dataclass(slots=True)
class DocumentSymbol:
    """
    Represents a document symbol.
    """

    name: str

    kind: str

    detail: str = ""

    line: int = 0

    character: int = 0

    children: list["DocumentSymbol"] = field(
        default_factory=list,
    )

###############################################################################
# Document Symbols Provider
###############################################################################


class DocumentSymbolsProvider:
    """
    LSP Document Symbols Provider.

    Responsibilities

    - Outline view
    - Breadcrumbs
    - Symbol hierarchy
    - Namespace support
    - Symbol cache
    """

    ###########################################################################

    def __init__(
        self,
        client: LSPClient,
    ) -> None:

        self._client = client

        self._cache: dict[
            str,
            list[DocumentSymbol],
        ] = {}

        logger.info(
            "Document Symbols Provider initialized."
        )

###############################################################################
# Request
###############################################################################

    def request(
        self,
        uri: str,
    ) -> int:
        """
        Request document symbols.
        """

        return self._client.send_request(
            "textDocument/documentSymbol",
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
        symbols: list[
            DocumentSymbol
        ],
    ) -> None:
        """
        Cache document symbols.
        """

        self._cache[
            uri
        ] = symbols

###############################################################################
# Lookup
###############################################################################

    def cached(
        self,
        uri: str,
    ) -> list[
        DocumentSymbol
    ]:
        """
        Return cached symbols.
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
        Clear symbol cache.
        """

        self._cache.clear()
###############################################################################
# Symbol Lookup
###############################################################################

    def find(
        self,
        uri: str,
        name: str,
    ) -> DocumentSymbol | None:
        """
        Find a symbol by name.
        """

        for symbol in self.flatten(uri):

            if symbol.name == name:

                return symbol

        return None

###############################################################################
# Flatten Hierarchy
###############################################################################

    def flatten(
        self,
        uri: str,
    ) -> list[DocumentSymbol]:
        """
        Return a flattened symbol hierarchy.
        """

        result: list[
            DocumentSymbol
        ] = []

        def visit(
            symbol: DocumentSymbol,
        ) -> None:

            result.append(
                symbol,
            )

            for child in symbol.children:

                visit(
                    child,
                )

        for symbol in self.cached(
            uri,
        ):

            visit(
                symbol,
            )

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
            "cached_documents": len(
                self._cache
            ),
            "cached_symbols": sum(
                len(
                    self.flatten(uri)
                )
                for uri
                in self._cache
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
                uri: len(
                    self.flatten(uri)
                )
                for uri
                in self._cache
            },
        }

###############################################################################
# Global Provider
###############################################################################

document_symbols_provider: (
    DocumentSymbolsProvider | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "DocumentSymbol",
    "DocumentSymbolsProvider",
    "document_symbols_provider",
]