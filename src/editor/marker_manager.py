"""
==============================================================================
GEETA AI Engine

File        : marker_manager.py
Package     : editor
Description : Editor Marker Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Marker Types
###############################################################################


class MarkerType(str, Enum):
    """
    Marker types.
    """

    ERROR = "error"

    WARNING = "warning"

    INFO = "info"

    HINT = "hint"

    BOOKMARK = "bookmark"

    BREAKPOINT = "breakpoint"

    GIT = "git"

    AI = "ai"

###############################################################################
# Marker
###############################################################################


@dataclass(slots=True)
class Marker:
    """
    Represents an editor marker.
    """

    line: int

    column: int

    marker_type: MarkerType

    message: str

###############################################################################
# Marker Manager
###############################################################################


class MarkerManager:
    """
    Marker management.

    Responsibilities

    - Diagnostics
    - Breakpoints
    - Bookmarks
    - Git markers
    - AI markers
    """

    def __init__(
        self,
    ) -> None:

        self._markers: list[
            Marker
        ] = []

        logger.info(
            "Marker Manager initialized."
        )

###############################################################################
# Add Marker
###############################################################################

    def add(
        self,
        marker: Marker,
    ) -> None:
        """
        Add a marker.
        """

        self._markers.append(
            marker,
        )

###############################################################################
# Remove Marker
###############################################################################

    def remove(
        self,
        marker: Marker,
    ) -> bool:
        """
        Remove a marker.
        """

        if marker not in self._markers:

            return False

        self._markers.remove(
            marker,
        )

        return True

###############################################################################
# Clear
###############################################################################

    def clear(
        self,
    ) -> None:
        """
        Remove all markers.
        """

        self._markers.clear()

###############################################################################
# Lookup
###############################################################################

    def markers(
        self,
    ) -> list[Marker]:
        """
        Return all markers.
        """

        return list(
            self._markers
        )
###############################################################################
# Filtering
###############################################################################

    def by_type(
        self,
        marker_type: MarkerType,
    ) -> list[Marker]:
        """
        Return markers of a specific type.
        """

        return [
            marker
            for marker in self._markers
            if marker.marker_type == marker_type
        ]

    ###########################################################################

    def by_line(
        self,
        line: int,
    ) -> list[Marker]:
        """
        Return markers for a line.
        """

        return [
            marker
            for marker in self._markers
            if marker.line == line
        ]

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return marker statistics.
        """

        return {
            "total": len(
                self._markers
            ),
            "errors": len(
                self.by_type(
                    MarkerType.ERROR
                )
            ),
            "warnings": len(
                self.by_type(
                    MarkerType.WARNING
                )
            ),
            "bookmarks": len(
                self.by_type(
                    MarkerType.BOOKMARK
                )
            ),
            "breakpoints": len(
                self.by_type(
                    MarkerType.BREAKPOINT
                )
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return marker report.
        """

        return {
            "statistics": self.statistics(),
            "markers": [
                {
                    "line": marker.line,
                    "column": marker.column,
                    "type": marker.marker_type.value,
                    "message": marker.message,
                }
                for marker
                in self._markers
            ],
        }

###############################################################################
# Global Marker Manager
###############################################################################

marker_manager = MarkerManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "MarkerType",
    "Marker",
    "MarkerManager",
    "marker_manager",
]