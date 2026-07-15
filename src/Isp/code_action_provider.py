"""
==============================================================================
GEETA AI IDE

File        : code_action_provider.py
Package     : lsp
Description : LSP Code Action Provider

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
# Code Action
###############################################################################


@dataclass(slots=True)
class CodeAction:
    """
    Represents an LSP Code Action.
    """

    title: str

    kind: str

    command: str = ""

    diagnostics: list[str] = field(
        default_factory=list,
    )

    preferred: bool = False

###############################################################################
# Code Action Provider
###############################################################################


class CodeActionProvider:
    """
    LSP Code Action Provider.

    Responsibilities

    - Quick Fix
    - Refactor
    - Source Actions
    - Organize Imports
    - AI Fixes
    """

    ###########################################################################

    def __init__(
        self,
        client: LSPClient,
    ) -> None:

        self._client = client

        self._cache: dict[
            tuple[str, int, int],
            list[CodeAction],
        ] = {}

        logger.info(
            "Code Action Provider initialized."
        )

###############################################################################
# Request
###############################################################################

    def request(
        self,
        uri: str,
        line: int,
        character: int,
        diagnostics: list[dict[str, Any]],
    ) -> int:
        """
        Send code action request.
        """

        return self._client.send_request(
            "textDocument/codeAction",
            {
                "textDocument": {
                    "uri": uri,
                },
                "range": {
                    "start": {
                        "line": line,
                        "character": character,
                    },
                    "end": {
                        "line": line,
                        "character": character,
                    },
                },
                "context": {
                    "diagnostics": diagnostics,
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
        actions: list[
            CodeAction
        ],
    ) -> None:
        """
        Cache code actions.
        """

        self._cache[
            (
                uri,
                line,
                character,
            )
        ] = actions

###############################################################################
# Lookup
###############################################################################

    def cached(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> list[
        CodeAction
    ] | None:
        """
        Return cached actions.
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
        Clear action cache.
        """

        self._cache.clear()
###############################################################################
# Preferred Action
###############################################################################

    def preferred_action(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> CodeAction | None:
        """
        Return the preferred code action.
        """

        actions = self.cached(
            uri,
            line,
            character,
        )

        if not actions:

            return None

        for action in actions:

            if action.preferred:

                return action

        return actions[0]

###############################################################################
# Filter
###############################################################################

    def filter_by_kind(
        self,
        actions: list[
            CodeAction,
        ],
        kind: str,
    ) -> list[CodeAction]:
        """
        Filter actions by kind.
        """

        return [
            action
            for action
            in actions
            if action.kind.startswith(
                kind,
            )
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
            "cached_requests": len(
                self._cache
            ),
            "cached_actions": sum(
                len(actions)
                for actions
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
                    "actions": len(value),
                }
                for key, value
                in self._cache.items()
            ],
        }

###############################################################################
# Global Provider
###############################################################################

code_action_provider: CodeActionProvider | None = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "CodeAction",
    "CodeActionProvider",
    "code_action_provider",
]