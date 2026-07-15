"""
==============================================================================
GEETA AI IDE

File        : semantic_tokens_provider.py
Package     : lsp
Description : LSP Semantic Tokens Provider

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
# Semantic Token
###############################################################################


@dataclass(slots=True)
class SemanticToken:
    """
    Represents a semantic token.
    """

    line: int

    start: int

    length: int

    token_type: str

    modifiers: list[str]

###############################################################################
# Semantic Tokens Provider
###############################################################################


class SemanticTokensProvider:
    """
    LSP Semantic Tokens Provider.

    Responsibilities

    - Semantic highlighting
    - Token decoding
    - Token cache
    - Delta updates
    - Theme integration
    """

    ###########################################################################

    def __init__(
        self,
        client: LSPClient,
    ) -> None:

        self._client = client

        self._cache: dict[
            str,
            list[SemanticToken],
        ] = {}

        logger.info(
            "Semantic Tokens Provider initialized."
        )

###############################################################################
# Full Tokens
###############################################################################

    def request_full(
        self,
        uri: str,
    ) -> int:
        """
        Request semantic tokens for a document.
        """

        return self._client.send_request(
            "textDocument/semanticTokens/full",
            {
                "textDocument": {
                    "uri": uri,
                }
            },
        )

###############################################################################
# Range Tokens
###############################################################################

    def request_range(
        self,
        uri: str,
        start_line: int,
        end_line: int,
    ) -> int:
        """
        Request semantic tokens for a range.
        """

        return self._client.send_request(
            "textDocument/semanticTokens/range",
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
        tokens: list[
            SemanticToken
        ],
    ) -> None:
        """
        Cache semantic tokens.
        """

        self._cache[
            uri
        ] = tokens

###############################################################################
# Lookup
###############################################################################

    def cached(
        self,
        uri: str,
    ) -> list[
        SemanticToken
    ]:
        """
        Return cached tokens.
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
        Clear semantic token cache.
        """

        self._cache.clear()
###############################################################################
# Token Lookup
###############################################################################

    def token_at(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> SemanticToken | None:
        """
        Return the semantic token at the given position.
        """

        for token in self.cached(
            uri,
        ):

            if token.line != line:

                continue

            if (
                token.start
                <= character
                < token.start + token.length
            ):

                return token

        return None

###############################################################################
# Filter
###############################################################################

    def by_type(
        self,
        uri: str,
        token_type: str,
    ) -> list[SemanticToken]:
        """
        Return semantic tokens of a specific type.
        """

        return [
            token
            for token
            in self.cached(uri)
            if token.token_type == token_type
        ]

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return semantic token statistics.
        """

        return {
            "cached_documents": len(
                self._cache
            ),
            "cached_tokens": sum(
                len(tokens)
                for tokens
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
        Return semantic token report.
        """

        return {
            "statistics": self.statistics(),
            "documents": {
                uri: len(tokens)
                for uri, tokens
                in self._cache.items()
            },
        }

###############################################################################
# Global Provider
###############################################################################

semantic_tokens_provider: (
    SemanticTokensProvider | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "SemanticToken",
    "SemanticTokensProvider",
    "semantic_tokens_provider",
]