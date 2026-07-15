"""
==============================================================================
GEETA AI IDE

File        : type_definition_provider.py
Package     : lsp
Description : LSP Type Definition Provider

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
# Type Definition
###############################################################################


@dataclass(slots=True)
class TypeDefinition:
    """
    Represents a type definition.
    """

    uri: str

    line: int

    character: int

    end_line: int

    end_character: int

###############################################################################
# Type Definition Provider
###############################################################################


class TypeDefinitionProvider:
    """
    LSP Type Definition Provider.

    Responsibilities

    - Go To Type Definition
    - Generic type lookup
    - Type alias lookup
    - Type hierarchy
    - Type cache
    """

    ###########################################################################

    def __init__(
        self,
        client: LSPClient,
    ) -> None:

        self._client = client

        self._cache: dict[
            tuple[str, int, int],
            list[TypeDefinition],
        ] = {}

        logger.info(
            "Type Definition Provider initialized."
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
        Request type definition.
        """

        return self._client.send_request(
            "textDocument/typeDefinition",
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
            TypeDefinition
        ],
    ) -> None:
        """
        Cache type definitions.
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
        TypeDefinition
    ] | None:
        """
        Return cached type definitions.
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
        Clear type definition cache.
        """

        self._cache.clear()
###############################################################################
# Primary Type Definition
###############################################################################

    def primary(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> TypeDefinition | None:
        """
        Return the primary type definition.
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
# Peek Type Definition
###############################################################################

    def peek(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> list[TypeDefinition]:
        """
        Return all cached type definitions.
        """

        definitions = self.cached(
            uri,
            line,
            character,
        )

        if definitions is None:

            return []

        return list(
            definitions,
        )

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
            "cached_type_definitions": sum(
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
        Return provider report.
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
# Global Provider
###############################################################################

type_definition_provider: (
    TypeDefinitionProvider | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "TypeDefinition",
    "TypeDefinitionProvider",
    "type_definition_provider",
]