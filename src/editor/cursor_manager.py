"""
==============================================================================
GEETA AI Engine

File        : cursor_manager.py
Package     : editor
Description : Cursor Manager

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
# Cursor
###############################################################################


@dataclass(slots=True)
class Cursor:
    """
    Represents a cursor position.
    """

    line: int = 0

    column: int = 0

###############################################################################
# Cursor Manager
###############################################################################


class CursorManager:
    """
    Cursor management.

    Responsibilities

    - Cursor movement
    - Multi-cursor
    - Navigation
    - View synchronization
    """

    def __init__(
        self,
    ) -> None:

        self._cursors: list[
            Cursor
        ] = [
            Cursor(),
        ]

        logger.info(
            "Cursor Manager initialized."
        )

###############################################################################
# Primary Cursor
###############################################################################

    @property
    def cursor(
        self,
    ) -> Cursor:
        """
        Return primary cursor.
        """

        return self._cursors[0]

###############################################################################
# Set Position
###############################################################################

    def set_position(
        self,
        line: int,
        column: int,
    ) -> None:
        """
        Set cursor position.
        """

        self.cursor.line = max(
            0,
            line,
        )

        self.cursor.column = max(
            0,
            column,
        )

###############################################################################
# Movement
###############################################################################

    def move_left(
        self,
    ) -> None:
        """
        Move cursor left.
        """

        self.cursor.column = max(
            0,
            self.cursor.column - 1,
        )

    ###########################################################################

    def move_right(
        self,
    ) -> None:
        """
        Move cursor right.
        """

        self.cursor.column += 1

    ###########################################################################

    def move_up(
        self,
    ) -> None:
        """
        Move cursor up.
        """

        self.cursor.line = max(
            0,
            self.cursor.line - 1,
        )

    ###########################################################################

    def move_down(
        self,
    ) -> None:
        """
        Move cursor down.
        """

        self.cursor.line += 1
###############################################################################
# Multi Cursor
###############################################################################

    def add_cursor(
        self,
        line: int,
        column: int,
    ) -> None:
        """
        Add a new cursor.
        """

        self._cursors.append(
            Cursor(
                line=max(0, line),
                column=max(0, column),
            )
        )

    ###########################################################################

    def remove_cursor(
        self,
        index: int,
    ) -> bool:
        """
        Remove a cursor.
        """

        if (
            index <= 0
            or index >= len(self._cursors)
        ):

            return False

        del self._cursors[index]

        return True

###############################################################################
# Navigation
###############################################################################

    def move_to_line(
        self,
        line: int,
    ) -> None:
        """
        Move cursor to a line.
        """

        self.cursor.line = max(
            0,
            line,
        )

    ###########################################################################

    def move_to_column(
        self,
        column: int,
    ) -> None:
        """
        Move cursor to a column.
        """

        self.cursor.column = max(
            0,
            column,
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return cursor statistics.
        """

        return {
            "cursor_count": len(
                self._cursors
            ),
            "primary_line": (
                self.cursor.line
            ),
            "primary_column": (
                self.cursor.column
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return cursor manager report.
        """

        return {
            "statistics": self.statistics(),
            "cursors": [
                {
                    "line": cursor.line,
                    "column": cursor.column,
                }
                for cursor in self._cursors
            ],
        }

###############################################################################
# Global Cursor Manager
###############################################################################

cursor_manager = CursorManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "Cursor",
    "CursorManager",
    "cursor_manager",
]