"""
==============================================================================
GEETA AI Engine

File        : editor_history.py
Package     : editor
Description : Editor History Manager

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
# History Entry
###############################################################################


@dataclass(slots=True)
class HistoryEntry:
    """
    Represents a navigation history entry.
    """

    file_path: str

    line: int

    column: int

###############################################################################
# Editor History
###############################################################################


class EditorHistory:
    """
    Editor navigation history.

    Responsibilities

    - Navigation history
    - Jump Back
    - Jump Forward
    - Recently visited locations
    - History management
    """

    def __init__(
        self,
    ) -> None:

        self._back_stack: list[
            HistoryEntry
        ] = []

        self._forward_stack: list[
            HistoryEntry
        ] = []

        logger.info(
            "Editor History initialized."
        )

###############################################################################
# Push
###############################################################################

    def push(
        self,
        file_path: str,
        line: int,
        column: int,
    ) -> None:
        """
        Push a navigation location.
        """

        self._back_stack.append(
            HistoryEntry(
                file_path=file_path,
                line=line,
                column=column,
            )
        )

        self._forward_stack.clear()

###############################################################################
# Back
###############################################################################

    def back(
        self,
    ) -> HistoryEntry | None:
        """
        Navigate backward.
        """

        if len(self._back_stack) <= 1:

            return None

        current = self._back_stack.pop()

        self._forward_stack.append(
            current,
        )

        return self._back_stack[-1]

###############################################################################
# Forward
###############################################################################

    def forward(
        self,
    ) -> HistoryEntry | None:
        """
        Navigate forward.
        """

        if not self._forward_stack:

            return None

        entry = self._forward_stack.pop()

        self._back_stack.append(
            entry,
        )

        return entry

###############################################################################
# Current
###############################################################################

    @property
    def current(
        self,
    ) -> HistoryEntry | None:
        """
        Return current location.
        """

        if not self._back_stack:

            return None

        return self._back_stack[-1]
###############################################################################
# Clear
###############################################################################

    def clear(
        self,
    ) -> None:
        """
        Clear navigation history.
        """

        self._back_stack.clear()

        self._forward_stack.clear()

###############################################################################
# Recent Locations
###############################################################################

    def recent(
        self,
        limit: int = 20,
    ) -> list[HistoryEntry]:
        """
        Return recently visited locations.
        """

        return list(
            reversed(
                self._back_stack[-limit:]
            )
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return navigation history statistics.
        """

        return {
            "back_entries": len(
                self._back_stack
            ),
            "forward_entries": len(
                self._forward_stack
            ),
            "current_location": (
                self.current.file_path
                if self.current
                else None
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return navigation history report.
        """

        return {
            "statistics": self.statistics(),
            "history": [
                {
                    "file": entry.file_path,
                    "line": entry.line,
                    "column": entry.column,
                }
                for entry
                in self._back_stack
            ],
            "forward_history": [
                {
                    "file": entry.file_path,
                    "line": entry.line,
                    "column": entry.column,
                }
                for entry
                in self._forward_stack
            ],
        }

###############################################################################
# Global Editor History
###############################################################################

editor_history = EditorHistory()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "HistoryEntry",
    "EditorHistory",
    "editor_history",
]