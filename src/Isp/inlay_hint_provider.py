"""
==============================================================================
GEETA AI IDE

File        : inlay_hint_provider.py
Package     : lsp
Description : LSP Inlay Hint Provider

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
# Inlay Hint
###############################################################################


@dataclass(slots=True)
class InlayHint:
    """
    Represents an LSP Inlay Hint.
    """

    line: int

    character: int

    label: str

    kind: str

    tooltip: str = ""

###############################################################################
# Inlay Hint Provider
###############################################################################


class InlayHintProvider:
    """
    LSP Inlay Hint Provider.

    Responsibilities

    - Parameter hints
    - Type hints
    - Return hints
    - Hint cache
    - AI hints
    """

    ###########################################################################

    def __init__(
        self,
        client: LSPClient,
    ) -> None:

        self._client = client

        self._cache: dict[
            str,
            list[InlayHint],
        ] = {}

        logger.info(
            "Inlay Hint Provider initialized."
        )

###############################################################################
# Request
###############################################################################

    def request(
        self,
        uri: str,
        start_line: int,
        end_line: int,
    ) -> int:
        """
        Request inlay hints.
        """

        return self._client.send_request(
            "textDocument/inlayHint",
            {
                "textDocument": {
                    "uri": uri,
                },
                "range": {
                    "start": {
                        "line": start_line,
                        "character": 0,
                    },
                    "end": {
                        "line": end_line,
                        "character": 0,
                    },
                },
            },
        )

###############################################################################
# Cache
###############################################################################

    def cache(
        self,
        uri: str,
        hints: list[
            InlayHint
        ],
    ) -> None:
        """
        Cache inlay hints.
        """

        self._cache[
            uri
        ] = hints

###############################################################################
# Lookup
###############################################################################

    def cached(
        self,
        uri: str,
    ) -> list[
        InlayHint
    ]:
        """
        Return cached hints.
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
        Clear inlay hint cache.
        """

        self._cache.clear()
###############################################################################
# Hint Lookup
###############################################################################

    def hint_at(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> InlayHint | None:
        """
        Return hint at the specified position.
        """

        for hint in self.cached(
            uri,
        ):

            if (
                hint.line == line
                and hint.character == character
            ):

                return hint

        return None

###############################################################################
# Filter
###############################################################################

    def by_kind(
        self,
        uri: str,
        kind: str,
    ) -> list[InlayHint]:
        """
        Return hints filtered by kind.
        """

        return [
            hint
            for hint
            in self.cached(
                uri,
            )
            if hint.kind == kind
        ]

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
            "cached_hints": sum(
                len(hints)
                for hints
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
                uri: len(
                    hints
                )
                for uri, hints
                in self._cache.items()
            },
        }

###############################################################################
# Global Provider
###############################################################################

inlay_hint_provider: (
    InlayHintProvider | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "InlayHint",
    "InlayHintProvider",
    "inlay_hint_provider",
]