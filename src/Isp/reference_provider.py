"""
==============================================================================
GEETA AI IDE

File        : reference_provider.py
Package     : lsp
Description : Find References Provider

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
# Reference Location
###############################################################################


@dataclass(slots=True)
class ReferenceLocation:
    """
    Represents a symbol reference.
    """

    uri: str

    line: int

    character: int

    end_line: int

    end_character: int

###############################################################################
# Reference Provider
###############################################################################


class ReferenceProvider:
    """
    Find References provider.

    Responsibilities

    - Find All References
    - Workspace references
    - Cross-file references
    - Reference cache
    - Peek References
    """

    ###########################################################################

    def __init__(
        self,
        client: LSPClient,
    ) -> None:

        self._client = client

        self._cache: dict[
            tuple[str, int, int],
            list[ReferenceLocation],
        ] = {}

        logger.info(
            "Reference Provider initialized."
        )

###############################################################################
# Request
###############################################################################

    def request(
        self,
        uri: str,
        line: int,
        character: int,
        include_declaration: bool = True,
    ) -> int:
        """
        Send references request.
        """

        return self._client.send_request(
            "textDocument/references",
            {
                "textDocument": {
                    "uri": uri,
                },
                "position": {
                    "line": line,
                    "character": character,
                },
                "context": {
                    "includeDeclaration": (
                        include_declaration
                    ),
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
        references: list[
            ReferenceLocation
        ],
    ) -> None:
        """
        Cache references.
        """

        self._cache[
            (
                uri,
                line,
                character,
            )
        ] = references

###############################################################################
# Lookup
###############################################################################

    def cached(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> list[
        ReferenceLocation
    ] | None:
        """
        Return cached references.
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
        Clear reference cache.
        """

        self._cache.clear()
###############################################################################
# Peek References
###############################################################################

    def peek(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> list[ReferenceLocation]:
        """
        Return cached references for Peek References.
        """

        references = self.cached(
            uri,
            line,
            character,
        )

        if references is None:

            return []

        return list(
            references
        )

###############################################################################
# Group By File
###############################################################################

    def group_by_file(
        self,
        references: list[
            ReferenceLocation
        ],
    ) -> dict[
        str,
        list[ReferenceLocation],
    ]:
        """
        Group references by file.
        """

        grouped: dict[
            str,
            list[ReferenceLocation],
        ] = {}

        for reference in references:

            grouped.setdefault(
                reference.uri,
                [],
            ).append(
                reference,
            )

        return grouped

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
            "cached_references": sum(
                len(reference_list)
                for reference_list
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
                    "references": len(value),
                }
                for key, value
                in self._cache.items()
            ],
        }

###############################################################################
# Global Provider
###############################################################################

reference_provider: ReferenceProvider | None = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "ReferenceLocation",
    "ReferenceProvider",
    "reference_provider",
]