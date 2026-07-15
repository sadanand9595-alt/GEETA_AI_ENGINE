"""
==============================================================================
GEETA AI IDE

File        : moniker_provider.py
Package     : lsp
Description : LSP Moniker Provider

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
# Moniker
###############################################################################


@dataclass(slots=True)
class Moniker:
    """
    Represents an LSP Moniker.
    """

    scheme: str

    identifier: str

    unique: str

    kind: str

###############################################################################
# Moniker Provider
###############################################################################


class MonikerProvider:
    """
    Enterprise Moniker Provider.

    Responsibilities

    - Cross-project symbol identity
    - External library symbols
    - Package references
    - Symbol uniqueness
    - Repository navigation
    """

    ###########################################################################

    def __init__(
        self,
        client: LSPClient,
    ) -> None:

        self._client = client

        self._cache: dict[
            tuple[str, int, int],
            list[Moniker],
        ] = {}

        logger.info(
            "Moniker Provider initialized."
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
        Request monikers.
        """

        return self._client.send_request(
            "textDocument/moniker",
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
        monikers: list[
            Moniker
        ],
    ) -> None:
        """
        Cache monikers.
        """

        self._cache[
            (
                uri,
                line,
                character,
            )
        ] = monikers

###############################################################################
# Lookup
###############################################################################

    def cached(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> list[
        Moniker
    ]:
        """
        Return cached monikers.
        """

        return list(
            self._cache.get(
                (
                    uri,
                    line,
                    character,
                ),
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
        Clear moniker cache.
        """

        self._cache.clear()
###############################################################################
# Symbol Lookup
###############################################################################

    def moniker_at(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> Moniker | None:
        """
        Return the primary moniker at the specified position.
        """

        monikers = self.cached(
            uri,
            line,
            character,
        )

        if not monikers:

            return None

        return monikers[0]

###############################################################################
# Unique Validation
###############################################################################

    def has_unique_moniker(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> bool:
        """
        Return True if a unique moniker exists.
        """

        for moniker in self.cached(
            uri,
            line,
            character,
        ):

            if moniker.unique.lower() != "local":

                return True

        return False

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
            "cached_requests": len(
                self._cache
            ),
            "cached_monikers": sum(
                len(monikers)
                for monikers
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
            "cached": [
                {
                    "uri": key[0],
                    "line": key[1],
                    "character": key[2],
                    "monikers": len(value),
                }
                for key, value
                in self._cache.items()
            ],
        }

###############################################################################
# Global Provider
###############################################################################

moniker_provider: (
    MonikerProvider | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "Moniker",
    "MonikerProvider",
    "moniker_provider",
]