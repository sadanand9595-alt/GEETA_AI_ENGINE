"""
==============================================================================
GEETA AI Engine

File        : minimap.py
Package     : editor
Description : Editor Minimap

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
# Minimap
###############################################################################


class Minimap:
    """
    Editor minimap.

    Responsibilities

    - Document overview
    - Viewport synchronization
    - Scroll synchronization
    - Navigation
    - Rendering support
    """

    def __init__(
        self,
    ) -> None:

        self._lines: list[str] = []

        self._viewport_start = 0

        self._viewport_end = 0

        logger.info(
            "Minimap initialized."
        )

###############################################################################
# Load Document
###############################################################################

    def load(
        self,
        text: str,
    ) -> None:
        """
        Load document into minimap.
        """

        self._lines = text.splitlines()

###############################################################################
# Viewport
###############################################################################

    def set_viewport(
        self,
        start: int,
        end: int,
    ) -> None:
        """
        Update viewport.
        """

        self._viewport_start = max(
            0,
            start,
        )

        self._viewport_end = max(
            self._viewport_start,
            end,
        )

###############################################################################
# Visible Lines
###############################################################################

    def visible_lines(
        self,
    ) -> list[str]:
        """
        Return viewport lines.
        """

        return self._lines[
            self._viewport_start:
            self._viewport_end
        ]

###############################################################################
# Navigate
###############################################################################

    def goto(
        self,
        line: int,
    ) -> int:
        """###############################################################################
# Scroll Information
###############################################################################

    def scroll_percentage(
        self,
    ) -> float:
        """
        Return viewport scroll percentage.
        """

        if not self._lines:

            return 0.0

        return (
            self._viewport_start
            / max(
                1,
                len(self._lines) - 1,
            )
        ) * 100.0

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return minimap statistics.
        """

        return {
            "total_lines": len(
                self._lines
            ),
            "viewport_start": (
                self._viewport_start
            ),
            "viewport_end": (
                self._viewport_end
            ),
            "visible_lines": len(
                self.visible_lines()
            ),
            "scroll_percentage": round(
                self.scroll_percentage(),
                2,
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return minimap report.
        """

        return {
            "statistics": self.statistics(),
            "visible_preview": (
                self.visible_lines()
            ),
        }

###############################################################################
# Global Minimap
###############################################################################

minimap = Minimap()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "Minimap",
    "minimap",
]
        Navigate to a line.
        """

        if not self._lines:

            return 0

        return min(
            max(0, line),
            len(self._lines) - 1,
        )
###############################################################################
# Scroll Information
###############################################################################

    def scroll_percentage(
        self,
    ) -> float:
        """
        Return viewport scroll percentage.
        """

        if not self._lines:

            return 0.0

        return (
            self._viewport_start
            / max(
                1,
                len(self._lines) - 1,
            )
        ) * 100.0

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return minimap statistics.
        """

        return {
            "total_lines": len(
                self._lines
            ),
            "viewport_start": (
                self._viewport_start
            ),
            "viewport_end": (
                self._viewport_end
            ),
            "visible_lines": len(
                self.visible_lines()
            ),
            "scroll_percentage": round(
                self.scroll_percentage(),
                2,
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return minimap report.
        """

        return {
            "statistics": self.statistics(),
            "visible_preview": (
                self.visible_lines()
            ),
        }

###############################################################################
# Global Minimap
###############################################################################

minimap = Minimap()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "Minimap",
    "minimap",
]