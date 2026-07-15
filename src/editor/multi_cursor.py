"""
==============================================================================
GEETA AI Engine

File        : multi_cursor.py
Package     : editor
Description : Multi Cursor Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Caret
###############################################################################


@dataclass(slots=True)
class Caret:
    """
    Represents a single editor caret.
    """

    line: int

    column: int

###############################################################################
# Multi Cursor
###############################################################################


class MultiCursor:
    """
    Multi-cursor editing engine.

    Responsibilities

    - Multiple carets
    - Column editing
    - Caret synchronization
    - Bulk editing
    """

    def __init__(
        self,
    ) -> None:

        self._carets: list[
            Caret
        ] = [
            Caret(
                line=0,
                column=0,
            )
        ]

        logger.info(
            "Multi Cursor initialized."
        )

###############################################################################
# Carets
###############################################################################

    def add(
        self,
        line: int,
        column: int,
    ) -> None:
        """
        Add a caret.
        """

        self._carets.append(
            Caret(
                line=max(0, line),
                column=max(0, column),
            )
        )

    ###########################################################################

    def remove(
        self,
        index: int,
    ) -> bool:
        """
        Remove a caret.
        """

        if (
            index <= 0
            or index >= len(
                self._carets
            )
        ):

            return False

        del self._carets[index]

        return True

###############################################################################
# Lookup
###############################################################################

    def carets(
        self,
    ) -> list[Caret]:
        """
        Return all carets.
        """

        return list(
            self._carets
        )

###############################################################################
# Clear
###############################################################################

    def clear(
        self,
    ) -> None:
        """
        Reset to a single caret.
        """

        self._carets = [
            Caret(
                line=0,
                column=0,
            )
        ]
###############################################################################
# Primary Caret
###############################################################################

    @property
    def primary(
        self,
    ) -> Caret:
        """
        Return the primary caret.
        """

        return self._carets[0]

###############################################################################
# Move All Carets
###############################################################################

    def move(
        self,
        line_delta: int = 0,
        column_delta: int = 0,
    ) -> None:
        """
        Move all carets.
        """

        for caret in self._carets:

            caret.line = max(
                0,
                caret.line + line_delta,
            )

            caret.column = max(
                0,
                caret.column + column_delta,
            )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return multi-cursor statistics.
        """

        return {
            "caret_count": len(
                self._carets
            ),
            "primary_line": (
                self.primary.line
            ),
            "primary_column": (
                self.primary.column
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return multi-cursor report.
        """

        return {
            "statistics": self.statistics(),
            "carets": [
                {
                    "line": caret.line,
                    "column": caret.column,
                }
                for caret in self._carets
            ],
        }

###############################################################################
# Global Multi Cursor
###############################################################################

multi_cursor = MultiCursor()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "Caret",
    "MultiCursor",
    "multi_cursor",
]