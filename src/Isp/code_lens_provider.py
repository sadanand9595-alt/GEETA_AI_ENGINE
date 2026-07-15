"""
==============================================================================
GEETA AI IDE

File        : code_lens_provider.py
Package     : lsp
Description : LSP Code Lens Provider

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
# Code Lens
###############################################################################


@dataclass(slots=True)
class LSPCodeLens:
    """
    Represents an LSP CodeLens.
    """

    line: int

    character: int

    title: str

    command: str

    resolved: bool = False

###############################################################################
# Code Lens Provider
###############################################################################


class CodeLensProvider:
    """
    Enterprise LSP Code Lens Provider.

    Responsibilities

    - Reference Count
    - Run Test
    - Debug Test
    - Git Blame
    - AI Actions
    - Resolve CodeLens
    """

    ###########################################################################

    def __init__(
        self,
        client: LSPClient,
    ) -> None:

        self._client = client

        self._cache: dict[
            str,
            list[LSPCodeLens],
        ] = {}

        logger.info(
            "Code Lens Provider initialized."
        )

###############################################################################
# Request
###############################################################################

    def request(
        self,
        uri: str,
    ) -> int:
        """
        Request CodeLens.
        """

        return self._client.send_request(
            "textDocument/codeLens",
            {
                "textDocument": {
                    "uri": uri,
                }
            },
        )

###############################################################################
# Resolve
###############################################################################

    def resolve(
        self,
        lens: dict[str, Any],
    ) -> int:
        """
        Resolve CodeLens.
        """

        return self._client.send_request(
            "codeLens/resolve",
            lens,
        )

###############################################################################
# Cache
###############################################################################

    def cache(
        self,
        uri: str,
        lenses: list[
            LSPCodeLens
        ],
    ) -> None:
        """
        Cache CodeLens entries.
        """

        self._cache[
            uri
        ] = lenses

###############################################################################
# Lookup
###############################################################################

    def cached(
        self,
        uri: str,
    ) -> list[
        LSPCodeLens
    ]:
        """
        Return cached CodeLens entries.
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
        Clear CodeLens cache.
        """

        self._cache.clear()
###############################################################################
# Lookup
###############################################################################

    def lens_at(
        self,
        uri: str,
        line: int,
    ) -> LSPCodeLens | None:
        """
        Return CodeLens at the specified line.
        """

        for lens in self.cached(
            uri,
        ):

            if lens.line == line:

                return lens

        return None

###############################################################################
# Filter
###############################################################################

    def by_command(
        self,
        uri: str,
        command: str,
    ) -> list[LSPCodeLens]:
        """
        Return CodeLens entries filtered by command.
        """

        return [
            lens
            for lens
            in self.cached(
                uri,
            )
            if lens.command == command
        ]

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return CodeLens statistics.
        """

        return {
            "cached_documents": len(
                self._cache
            ),
            "cached_lenses": sum(
                len(lenses)
                for lenses
                in self._cache.values()
            ),
            "resolved_lenses": sum(
                sum(
                    1
                    for lens in lenses
                    if lens.resolved
                )
                for lenses
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
        Return CodeLens report.
        """

        return {
            "statistics": self.statistics(),
            "documents": {
                uri: len(lenses)
                for uri, lenses
                in self._cache.items()
            },
        }

###############################################################################
# Global Provider
###############################################################################

code_lens_provider: (
    CodeLensProvider | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "LSPCodeLens",
    "CodeLensProvider",
    "code_lens_provider",
]