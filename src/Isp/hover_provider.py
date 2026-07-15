"""
==============================================================================
GEETA AI IDE

File        : hover_provider.py
Package     : lsp
Description : LSP Hover Provider

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
# Hover Result
###############################################################################


@dataclass(slots=True)
class HoverResult:
    """
    Represents hover information.
    """

    contents: str

    language: str = "markdown"

    range: dict[str, Any] | None = None

###############################################################################
# Hover Provider
###############################################################################


class HoverProvider:
    """
    LSP Hover provider.

    Responsibilities

    - Hover requests
    - Documentation
    - Type information
    - AI explanation
    - Hover cache
    """

    ###########################################################################

    def __init__(
        self,
        client: LSPClient,
    ) -> None:

        self._client = client

        self._cache: dict[
            tuple[str, int, int],
            HoverResult,
        ] = {}

        logger.info(
            "Hover Provider initialized."
        )

###############################################################################
# Hover Request
###############################################################################

    def request(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> int:
        """
        Send hover request.
        """

        return self._client.send_request(
            "textDocument/hover",
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
        result: HoverResult,
    ) -> None:
        """
        Cache hover result.
        """

        self._cache[
            (
                uri,
                line,
                character,
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
    ) -> HoverResult | None:
        """
        Return cached hover.
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
        Clear hover cache.
        """

        self._cache.clear()
###############################################################################
# Markdown Rendering
###############################################################################

    def render(
        self,
        result: HoverResult,
    ) -> str:
        """
        Render hover contents.
        """

        if result.language == "markdown":

            return result.contents

        return f"```{result.language}\n{result.contents}\n```"

###############################################################################
# AI Explanation
###############################################################################

    def ai_explanation(
        self,
        result: HoverResult,
        explanation: str,
    ) -> HoverResult:
        """
        Attach AI explanation to hover result.
        """

        return HoverResult(
            contents=(
                result.contents
                + "\n\n---\n"
                + "### AI Explanation\n"
                + explanation
            ),
            language=result.language,
            range=result.range,
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return hover provider statistics.
        """

        return {
            "cached_entries": len(
                self._cache
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return hover provider report.
        """

        return {
            "statistics": self.statistics(),
            "cached": [
                {
                    "uri": key[0],
                    "line": key[1],
                    "character": key[2],
                }
                for key
                in self._cache.keys()
            ],
        }

###############################################################################
# Global Hover Provider
###############################################################################

hover_provider: HoverProvider | None = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "HoverResult",
    "HoverProvider",
    "hover_provider",
]