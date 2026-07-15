"""
==============================================================================
GEETA AI Engine

File        : line_numbers.py
Package     : editor
Description : Line Numbers & Editor Gutter

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Literal

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Line Numbers
###############################################################################


class LineNumbers:
    """
    Editor gutter manager.

    Responsibilities

    - Absolute line numbers
    - Relative line numbers
    - Active line
    - Gutter rendering
    - Width calculation
    """

    def __init__(
        self,
    ) -> None:

        self._mode: Literal[
            "absolute",
            "relative",
        ] = "absolute"

        self._active_line = 1

        logger.info(
            "Line Numbers initialized."
        )

###############################################################################
# Mode
###############################################################################

    def set_mode(
        self,
        mode: Literal[
            "absolute",
            "relative",
        ],
    ) -> None:
        """
        Set numbering mode.
        """

        self._mode = mode

###############################################################################
# Active Line
###############################################################################

    def set_active_line(
        self,
        line: int,
    ) -> None:
        """
        Set active editor line.
        """

        self._active_line = max(
            1,
            line,
        )

###############################################################################
# Display Number
###############################################################################

    def display_number(
        self,
        line: int,
    ) -> int:
        """
        Return displayed line number.
        """

        if self._mode == "absolute":

            return line

        return abs(
            line - self._active_line
        )

###############################################################################
# Width
###############################################################################

    def gutter_width(
        self,
        total_lines: int,
    ) -> int:
        """
        Return gutter width.
        """

        return len(
            str(
                max(
                    1,
                    total_lines,
                )
            )
        )
###############################################################################
# Gutter Rendering
###############################################################################

    def render(
        self,
        total_lines: int,
    ) -> list[str]:
        """
        Render line numbers for the gutter.
        """

        width = self.gutter_width(
            total_lines,
        )

        return [
            str(
                self.display_number(
                    line,
                )
            ).rjust(
                width,
            )
            for line
            in range(
                1,
                total_lines + 1,
            )
        ]

###############################################################################
# Active Line
###############################################################################

    def is_active(
        self,
        line: int,
    ) -> bool:
        """
        Return whether the line is active.
        """

        return (
            line
            == self._active_line
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
        total_lines: int,
    ) -> dict[str, object]:
        """
        Return gutter statistics.
        """

        return {
            "mode": self._mode,
            "active_line": (
                self._active_line
            ),
            "total_lines": (
                total_lines
            ),
            "gutter_width": (
                self.gutter_width(
                    total_lines,
                )
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
        total_lines: int,
    ) -> dict[str, object]:
        """
        Return gutter report.
        """

        return {
            "statistics": self.statistics(
                total_lines,
            ),
            "preview": self.render(
                min(
                    total_lines,
                    20,
                )
            ),
        }

###############################################################################
# Global Line Numbers
###############################################################################

line_numbers = LineNumbers()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "LineNumbers",
    "line_numbers",
]