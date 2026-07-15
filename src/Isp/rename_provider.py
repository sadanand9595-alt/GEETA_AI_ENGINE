"""
==============================================================================
GEETA AI IDE

File        : rename_provider.py
Package     : lsp
Description : Rename Symbol Provider

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
# Workspace Edit
###############################################################################


@dataclass(slots=True)
class TextEdit:
    """
    Represents a text edit.
    """

    uri: str

    start_line: int

    start_character: int

    end_line: int

    end_character: int

    new_text: str


###############################################################################
# Rename Result
###############################################################################


@dataclass(slots=True)
class RenameResult:
    """
    Rename operation result.
    """

    edits: list[TextEdit] = field(
        default_factory=list,
    )

###############################################################################
# Rename Provider
###############################################################################


class RenameProvider:
    """
    Workspace rename provider.

    Responsibilities

    - Symbol rename
    - Workspace edits
    - Rename preview
    - Conflict detection
    - Cross-file rename
    """

    ###########################################################################

    def __init__(
        self,
        client: LSPClient,
    ) -> None:

        self._client = client

        self._cache: dict[
            tuple[str, int, int, str],
            RenameResult,
        ] = {}

        logger.info(
            "Rename Provider initialized."
        )

###############################################################################
# Request
###############################################################################

    def request(
        self,
        uri: str,
        line: int,
        character: int,
        new_name: str,
    ) -> int:
        """
        Send rename request.
        """

        return self._client.send_request(
            "textDocument/rename",
            {
                "textDocument": {
                    "uri": uri,
                },
                "position": {
                    "line": line,
                    "character": character,
                },
                "newName": new_name,
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
        new_name: str,
        result: RenameResult,
    ) -> None:
        """
        Cache rename result.
        """

        self._cache[
            (
                uri,
                line,
                character,
                new_name,
            )
        ] = result

###############################################################################
# Lookup
###############################################################################

    def cached(
        self,
        uri: str,
        line: int,
        character: int,
        new_name: str,
    ) -> RenameResult | None:
        """
        Return cached rename result.
        """

        return self._cache.get(
            (
                uri,
                line,
                character,
                new_name,
            )
        )

###############################################################################
# Clear Cache
###############################################################################

    def clear_cache(
        self,
    ) -> None:
        """
        Clear rename cache.
        """

        self._cache.clear()
###############################################################################
# Preview
###############################################################################

    def preview(
        self,
        uri: str,
        line: int,
        character: int,
        new_name: str,
    ) -> list[TextEdit]:
        """
        Return workspace edits for preview.
        """

        result = self.cached(
            uri,
            line,
            character,
            new_name,
        )

        if result is None:

            return []

        return list(
            result.edits
        )

###############################################################################
# Conflict Detection
###############################################################################

    def has_conflicts(
        self,
        result: RenameResult,
    ) -> bool:
        """
        Detect duplicate edit locations.
        """

        seen: set[
            tuple[
                str,
                int,
                int,
            ]
        ] = set()

        for edit in result.edits:

            key = (
                edit.uri,
                edit.start_line,
                edit.start_character,
            )

            if key in seen:

                return True

            seen.add(
                key,
            )

        return False

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return rename provider statistics.
        """

        return {
            "cached_requests": len(
                self._cache
            ),
            "workspace_edits": sum(
                len(result.edits)
                for result
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
        Return rename provider report.
        """

        return {
            "statistics": self.statistics(),
            "cached_requests": [
                {
                    "uri": key[0],
                    "line": key[1],
                    "character": key[2],
                    "new_name": key[3],
                    "edits": len(value.edits),
                }
                for key, value
                in self._cache.items()
            ],
        }

###############################################################################
# Global Rename Provider
###############################################################################

rename_provider: RenameProvider | None = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "TextEdit",
    "RenameResult",
    "RenameProvider",
    "rename_provider",
]