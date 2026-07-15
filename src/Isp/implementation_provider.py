"""
==============================================================================
GEETA AI IDE

File        : implementation_provider.py
Package     : lsp
Description : LSP Implementation Provider

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
# Implementation Location
###############################################################################


@dataclass(slots=True)
class ImplementationLocation:
    """
    Represents an implementation location.
    """

    uri: str

    line: int

    character: int

    end_line: int

    end_character: int

###############################################################################
# Implementation Provider
###############################################################################


class ImplementationProvider:
    """
    LSP Implementation Provider.

    Responsibilities

    - Go To Implementation
    - Interface navigation
    - Abstract class navigation
    - Implementation cache
    - Multiple implementations
    """

    ###########################################################################

    def __init__(
        self,
        client: LSPClient,
    ) -> None:

        self._client = client

        self._cache: dict[
            tuple[str, int, int],
            list[ImplementationLocation],
        ] = {}

        logger.info(
            "Implementation Provider initialized."
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
        Request implementations.
        """

        return self._client.send_request(
            "textDocument/implementation",
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
        implementations: list[
            ImplementationLocation
        ],
    ) -> None:
        """
        Cache implementation results.
        """

        self._cache[
            (
                uri,
                line,
                character,
            )
        ] = implementations

###############################################################################
# Lookup
###############################################################################

    def cached(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> list[
        ImplementationLocation
    ] | None:
        """
        Return cached implementations.
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
        Clear implementation cache.
        """

        self._cache.clear()
###############################################################################
# Primary Implementation
###############################################################################

    def primary(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> ImplementationLocation | None:
        """
        Return the primary implementation.
        """

        implementations = self.cached(
            uri,
            line,
            character,
        )

        if not implementations:

            return None

        return implementations[0]

###############################################################################
# Peek Implementation
###############################################################################

    def peek(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> list[ImplementationLocation]:
        """
        Return implementations for Peek Implementation.
        """

        implementations = self.cached(
            uri,
            line,
            character,
        )

        if implementations is None:

            return []

        return list(
            implementations,
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return implementation provider statistics.
        """

        return {
            "cached_requests": len(
                self._cache
            ),
            "cached_implementations": sum(
                len(items)
                for items
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
        Return implementation provider report.
        """

        return {
            "statistics": self.statistics(),
            "cached": [
                {
                    "uri": key[0],
                    "line": key[1],
                    "character": key[2],
                    "implementations": len(value),
                }
                for key, value
                in self._cache.items()
            ],
        }

###############################################################################
# Global Provider
###############################################################################

implementation_provider: (
    ImplementationProvider | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "ImplementationLocation",
    "ImplementationProvider",
    "implementation_provider",
]