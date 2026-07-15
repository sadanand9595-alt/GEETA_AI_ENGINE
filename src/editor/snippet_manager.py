"""
==============================================================================
GEETA AI Engine

File        : snippet_manager.py
Package     : editor
Description : Snippet Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Snippet
###############################################################################


@dataclass(slots=True)
class Snippet:
    """
    Represents a code snippet.
    """

    name: str

    prefix: str

    body: str

    description: str = ""

    language: str = "global"

###############################################################################
# Snippet Manager
###############################################################################


class SnippetManager:
    """
    Code snippet manager.

    Responsibilities

    - User snippets
    - Language snippets
    - Expansion
    - Import/Export
    - AI snippets
    """

    def __init__(
        self,
    ) -> None:

        self._snippets: dict[
            str,
            Snippet,
        ] = {}

        logger.info(
            "Snippet Manager initialized."
        )

###############################################################################
# Register
###############################################################################

    def register(
        self,
        snippet: Snippet,
    ) -> None:
        """
        Register a snippet.
        """

        self._snippets[
            snippet.name
        ] = snippet

###############################################################################
# Remove
###############################################################################

    def remove(
        self,
        name: str,
    ) -> bool:
        """
        Remove a snippet.
        """

        if name not in self._snippets:

            return False

        del self._snippets[name]

        return True

###############################################################################
# Lookup
###############################################################################

    def snippet(
        self,
        name: str,
    ) -> Snippet | None:
        """
        Return a snippet.
        """

        return self._snippets.get(
            name,
        )

###############################################################################
# Expand
###############################################################################

    def expand(
        self,
        name: str,
    ) -> str:
        """
        Expand a snippet.
        """

        snippet = self.snippet(
            name,
        )

        if snippet is None:

            return ""

        return snippet.body
###############################################################################
# Search
###############################################################################

    def search(
        self,
        prefix: str,
    ) -> list[Snippet]:
        """
        Search snippets by prefix.
        """

        return [
            snippet
            for snippet
            in self._snippets.values()
            if snippet.prefix.startswith(
                prefix,
            )
        ]

###############################################################################
# Language Filter
###############################################################################

    def language_snippets(
        self,
        language: str,
    ) -> list[Snippet]:
        """
        Return snippets for a language.
        """

        return [
            snippet
            for snippet
            in self._snippets.values()
            if snippet.language
            in (
                language,
                "global",
            )
        ]

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return snippet statistics.
        """

        languages = {
            snippet.language
            for snippet
            in self._snippets.values()
        }

        return {
            "snippet_count": len(
                self._snippets
            ),
            "language_count": len(
                languages
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return snippet manager report.
        """

        return {
            "statistics": self.statistics(),
            "snippets": [
                {
                    "name": snippet.name,
                    "prefix": snippet.prefix,
                    "language": snippet.language,
                }
                for snippet
                in self._snippets.values()
            ],
        }

###############################################################################
# Global Snippet Manager
###############################################################################

snippet_manager = SnippetManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "Snippet",
    "SnippetManager",
    "snippet_manager",
]