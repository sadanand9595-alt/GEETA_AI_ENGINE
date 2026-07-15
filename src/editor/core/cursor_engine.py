"""
==============================================================================
GEETA AI ENGINE

File        : cursor_engine.py
Package     : editor.core
Description : Cursor Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from threading import RLock

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

    preferred_column: int = 0

###############################################################################
# Cursor Engine
###############################################################################


class CursorEngine:
    """
    Enterprise Cursor Engine.

    Features
    --------
    • Multi Cursor Ready
    • Thread Safe
    • Word Navigation
    • Line Navigation
    • Selection Anchor Support
    """

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._lock = RLock()

        self._cursors: list[Cursor] = [
            Cursor(),
        ]

        logger.info(
            "Cursor Engine initialized."
        )

###############################################################################
# Cursor Queries
###############################################################################

    @property
    def primary(
        self,
    ) -> Cursor:
        """
        Return primary cursor.
        """

        return self._cursors[0]

    ###########################################################################

    @property
    def cursors(
        self,
    ) -> list[Cursor]:
        """
        Return all cursors.
        """

        return self._cursors.copy()

###############################################################################
# Cursor Management
###############################################################################

    def clear(
        self,
    ) -> None:
        """
        Reset to a single cursor.
        """

        with self._lock:

            self._cursors = [
                Cursor(),
            ]

    ###########################################################################

    def add_cursor(
        self,
        line: int,
        column: int,
    ) -> None:
        """
        Add a new cursor.
        """

        with self._lock:

            self._cursors.append(
                Cursor(
                    line=line,
                    column=column,
                    preferred_column=column,
                )
            )
            ###############################################################################
# Cursor Movement
###############################################################################

    def move_to(
        self,
        line: int,
        column: int,
    ) -> None:
        """
        Move the primary cursor.
        """

        with self._lock:

            cursor = self.primary

            cursor.line = max(0, line)

            cursor.column = max(0, column)

            cursor.preferred_column = (
                cursor.column
            )

    ###########################################################################

    def move_left(
        self,
        count: int = 1,
    ) -> None:
        """
        Move cursor left.
        """

        cursor = self.primary

        cursor.column = max(
            0,
            cursor.column - count,
        )

        cursor.preferred_column = (
            cursor.column
        )

    ###########################################################################

    def move_right(
        self,
        count: int = 1,
    ) -> None:
        """
        Move cursor right.
        """

        cursor = self.primary

        cursor.column += count

        cursor.preferred_column = (
            cursor.column
        )

    ###########################################################################

    def move_up(
        self,
        count: int = 1,
    ) -> None:
        """
        Move cursor up.
        """

        cursor = self.primary

        cursor.line = max(
            0,
            cursor.line - count,
        )

    ###########################################################################

    def move_down(
        self,
        count: int = 1,
    ) -> None:
        """
        Move cursor down.
        """

        cursor = self.primary

        cursor.line += count

###############################################################################
# Line Navigation
###############################################################################

    def move_home(
        self,
    ) -> None:
        """
        Move cursor to beginning of line.
        """

        cursor = self.primary

        cursor.column = 0

        cursor.preferred_column = 0

    ###########################################################################

    def move_end(
        self,
        line_length: int,
    ) -> None:
        """
        Move cursor to end of line.
        """

        cursor = self.primary

        cursor.column = max(
            0,
            line_length,
        )

        cursor.preferred_column = (
            cursor.column
        )

###############################################################################
# Validation
###############################################################################

    def validate(
        self,
        total_lines: int,
        line_length: int,
    ) -> None:
        """
        Clamp the primary cursor inside
        document bounds.
        """

        cursor = self.primary

        cursor.line = min(
            max(cursor.line, 0),
            max(total_lines - 1, 0),
        )

        cursor.column = min(
            max(cursor.column, 0),
            max(line_length, 0),
        )
        ###############################################################################
# Cursor Removal
###############################################################################

    def remove_cursor(
        self,
        index: int,
    ) -> bool:
        """
        Remove a secondary cursor.

        The primary cursor (index 0) cannot be removed.
        """

        with self._lock:

            if index <= 0:

                return False

            if index >= len(self._cursors):

                return False

            self._cursors.pop(index)

            return True

###############################################################################
# Queries
###############################################################################

    def cursor_count(
        self,
    ) -> int:
        """
        Return total cursor count.
        """

        return len(
            self._cursors,
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

        cursor = self.primary

        return {
            "cursor_count": len(
                self._cursors,
            ),
            "line": cursor.line,
            "column": cursor.column,
        }

###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return engine diagnostics.
        """

        stats = self.statistics()

        return {
            **stats,
            "multi_cursor": (
                len(self._cursors) > 1
            ),
        }

###############################################################################
# Reset
###############################################################################

    def reset(
        self,
    ) -> None:
        """
        Reset Cursor Engine.
        """

        self.clear()

        logger.info(
            "Cursor Engine reset."
        )

###############################################################################
# Representation
###############################################################################

    def __repr__(
        self,
    ) -> str:
        """
        Developer-friendly representation.
        """

        cursor = self.primary

        return (
            f"{self.__class__.__name__}"
            f"(line={cursor.line}, "
            f"column={cursor.column}, "
            f"cursors={len(self._cursors)})"
        )

###############################################################################
# Global Instance
###############################################################################

cursor_engine = CursorEngine()

###############################################################################
# Helper Functions
###############################################################################

def current_cursor() -> Cursor:
    """
    Return the primary cursor.
    """

    return cursor_engine.primary


def move_cursor(
    line: int,
    column: int,
) -> None:
    """
    Move the primary cursor.
    """

    cursor_engine.move_to(
        line,
        column,
    )


###############################################################################
# Exports
###############################################################################

__all__ = [
    "Cursor",
    "CursorEngine",
    "cursor_engine",
    "current_cursor",
    "move_cursor",
]