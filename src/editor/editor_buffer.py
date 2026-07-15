"""
==============================================================================
GEETA AI Engine

File        : editor_buffer.py
Package     : editor
Description : Editor Buffer

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Editor Buffer
###############################################################################


class EditorBuffer:
    """
    In-memory text buffer.

    Responsibilities

    - Text storage
    - Insert/Delete/Replace
    - Line access
    - Offset mapping
    - Incremental editing
    """

    def __init__(
        self,
        text: str = "",
    ) -> None:

        self._text = text

        logger.info(
            "Editor Buffer initialized."
        )

###############################################################################
# Text
###############################################################################

    @property
    def text(
        self,
    ) -> str:
        """
        Return buffer text.
        """

        return self._text

    ###########################################################################

    @text.setter
    def text(
        self,
        value: str,
    ) -> None:
        """
        Replace entire buffer.
        """

        self._text = value

###############################################################################
# Insert
###############################################################################

    def insert(
        self,
        offset: int,
        value: str,
    ) -> None:
        """
        Insert text.
        """

        self._text = (
            self._text[:offset]
            + value
            + self._text[offset:]
        )

###############################################################################
# Delete
###############################################################################

    def delete(
        self,
        start: int,
        end: int,
    ) -> None:
        """
        Delete text range.
        """

        self._text = (
            self._text[:start]
            + self._text[end:]
        )

###############################################################################
# Replace
###############################################################################

    def replace(
        self,
        start: int,
        end: int,
        value: str,
    ) -> None:
        """
        Replace text range.
        """

        self.delete(
            start,
            end,
        )

        self.insert(
            start,
            value,
        )

###############################################################################
# Lines
###############################################################################

    def lines(
        self,
    ) -> list[str]:
        """
        Return all lines.
        """

        return self._text.splitlines()
###############################################################################
# Line Access
###############################################################################

    def line(
        self,
        index: int,
    ) -> str:
        """
        Return a single line.
        """

        lines = self.lines()

        if index < 0 or index >= len(lines):

            raise IndexError(
                "Line index out of range."
            )

        return lines[index]

###############################################################################
# Offset Mapping
###############################################################################

    def offset_to_line_column(
        self,
        offset: int,
    ) -> tuple[int, int]:
        """
        Convert offset to line/column.
        """

        before = self._text[:offset]

        line = before.count("\n")

        column = len(
            before.split("\n")[-1]
        )

        return (
            line,
            column,
        )

    ###########################################################################

    def line_column_to_offset(
        self,
        line: int,
        column: int,
    ) -> int:
        """
        Convert line/column to offset.
        """

        lines = self.lines()

        if line >= len(lines):

            raise IndexError(
                "Line index out of range."
            )

        return (
            sum(
                len(item) + 1
                for item in lines[:line]
            )
            + column
        )

###############################################################################
# Snapshot
###############################################################################

    def snapshot(
        self,
    ) -> str:
        """
        Return an immutable snapshot.
        """

        return str(
            self._text
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return buffer statistics.
        """

        return {
            "characters": len(
                self._text
            ),
            "lines": len(
                self.lines()
            ),
            "words": len(
                self._text.split()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return buffer report.
        """

        return {
            "statistics": self.statistics(),
        }

###############################################################################
# Exports
###############################################################################

__all__ = [
    "EditorBuffer",
]