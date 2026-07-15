"""
==============================================================================
GEETA AI IDE

File        : definition_provider.py
Package     : lsp
Description : Go To Definition Provider

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
# Definition Location
###############################################################################


@dataclass(slots=True)
class DefinitionLocation:
    """
    Represents a symbol definition.
    """

    uri: str

    line: int

    character: int

    end_line: int

    end_character: int

###############################################################################
# Definition Provider
###############################################################################


class DefinitionProvider:
    """
    Go To Definition provider.

    Responsibilities

    - Symbol definition lookup
    - Cross-file navigation
    - Workspace navigation
    - Definition cache
    - Peek Definition
    """

    ###########################################################################

    def __init__(
        self,
        client: LSPClient,
    ) -> None:

        self._client = client

        self._cache: dict[
            tuple[str, int, int],
            list[DefinitionLocation],
        ] = {}

        logger.info(
            "Definition Provider initialized."
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
        Send definition request.
        """

        return self._client.send_request(
            "textDocument/definition",
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
        definitions: list[
            DefinitionLocation
        ],
    ) -> None:
        """
        Cache definition results.
        """

        self._cache[
            (
                uri,
                line,
                character,
            )
        ] = definitions

###############################################################################
# Lookup
###############################################################################

    def cached(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> list[
        DefinitionLocation
    ] | None:
        """
        Return cached definitions.
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
        Clear definition cache.
        """

        self._cache.clear()
###############################################################################
# Primary Definition
###############################################################################

    def primary(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> DefinitionLocation | None:
        """
        Return the primary definition.
        """

        definitions = self.cached(
            uri,
            line,
            character,
        )

        if not definitions:

            return None

        return definitions[0]

###############################################################################
# Peek Definition
###############################################################################

    def peek(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> list[DefinitionLocation]:
        """
        Return definitions for Peek Definition.
        """

        definitions = self.cached(
            uri,
            line,
            character,
        )

        if definitions is None:

            return []

        return list(
            definitions
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return definition provider statistics.
        """

        return {
            "cached_requests": len(
                self._cache
            ),
            "cached_definitions": sum(
                len(definitions)
                for definitions
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
        Return definition provider report.
        """

        return {
            "statistics": self.statistics(),
            "cached": [
                {
                    "uri": key[0],
                    "line": key[1],
                    "character": key[2],
                    "definitions": len(value),
                }
                for key, value
                in self._cache.items()
            ],
        }

###############################################################################
# Global Definition Provider
###############################################################################

definition_provider: DefinitionProvider | None = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "DefinitionLocation",
    "DefinitionProvider",
    "definition_provider",
]