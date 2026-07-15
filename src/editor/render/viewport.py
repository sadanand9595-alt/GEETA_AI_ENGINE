"""
==============================================================================
GEETA AI ENGINE

File        : viewport.py
Package     : editor.render
Description : Viewport Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from threading import RLock

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Viewport
###############################################################################


class Viewport:
    """
    Viewport manager.

    Responsibilities
    ----------------
    • Horizontal scrolling
    • Vertical scrolling
    • Visible line calculation
    • Coordinate mapping
    • Scroll boundaries
    """

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._lock = RLock()

        self._width = 0

        self._height = 0

        self._scroll_x = 0

        self._scroll_y = 0

        self._line_height = 20.0

        self._character_width = 8.0

        self._document_lines = 1

        logger.info(
            "Viewport initialized.",
        )

###############################################################################
# Size
###############################################################################

    def resize(
        self,
        width: int,
        height: int,
    ) -> None:
        """
        Update viewport size.
        """

        with self._lock:

            self._width = max(0, width)

            self._height = max(0, height)

###############################################################################
# Metrics
###############################################################################

    def set_metrics(
        self,
        line_height: float,
        character_width: float,
    ) -> None:
        """
        Update font metrics.
        """

        with self._lock:

            self._line_height = max(1.0, line_height)

            self._character_width = max(
                1.0,
                character_width,
            )

###############################################################################
# Document
###############################################################################

    def set_document_lines(
        self,
        lines: int,
    ) -> None:
        """
        Update total document line count.
        """

        with self._lock:

            self._document_lines = max(
                1,
                lines,
            )
            ###############################################################################
# Scrolling
###############################################################################

    def set_scroll(
        self,
        x: int,
        y: int,
    ) -> None:
        """
        Set viewport scroll position.
        """

        with self._lock:

            self._scroll_x = max(
                0,
                x,
            )

            self._scroll_y = max(
                0,
                y,
            )

    ###########################################################################

    def scroll_by(
        self,
        dx: int,
        dy: int,
    ) -> None:
        """
        Scroll relative to the current position.
        """

        self.set_scroll(

            self._scroll_x + dx,

            self._scroll_y + dy,

        )

###############################################################################
# Scroll Queries
###############################################################################

    @property
    def scroll_x(
        self,
    ) -> int:
        """
        Current horizontal scroll position.
        """

        return self._scroll_x

    ###########################################################################

    @property
    def scroll_y(
        self,
    ) -> int:
        """
        Current vertical scroll position.
        """

        return self._scroll_y

###############################################################################
# Visible Lines
###############################################################################

    @property
    def first_visible_line(
        self,
    ) -> int:
        """
        Return the first visible line.
        """

        return int(
            self._scroll_y
            / self._line_height
        )

    ###########################################################################

    @property
    def visible_line_count(
        self,
    ) -> int:
        """
        Number of visible lines.
        """

        return max(

            1,

            int(
                self._height
                / self._line_height
            ) + 1,

        )

    ###########################################################################

    @property
    def last_visible_line(
        self,
    ) -> int:
        """
        Return the last visible line.
        """

        return min(

            self._document_lines - 1,

            self.first_visible_line
            + self.visible_line_count,

        )
        ###############################################################################
# Coordinate Mapping
###############################################################################

    def line_to_y(
        self,
        line: int,
    ) -> float:
        """
        Convert document line to viewport Y coordinate.
        """

        return (
            line * self._line_height
            - self._scroll_y
        )

    ###########################################################################

    def y_to_line(
        self,
        y: float,
    ) -> int:
        """
        Convert viewport Y coordinate to document line.
        """

        return max(
            0,
            int(
                (y + self._scroll_y)
                / self._line_height
            ),
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int | float]:
        """
        Return viewport statistics.
        """

        return {
            "width": self._width,
            "height": self._height,
            "scroll_x": self._scroll_x,
            "scroll_y": self._scroll_y,
            "first_visible_line": self.first_visible_line,
            "last_visible_line": self.last_visible_line,
            "visible_lines": self.visible_line_count,
            "document_lines": self._document_lines,
            "line_height": self._line_height,
            "character_width": self._character_width,
        }

###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return viewport diagnostics.
        """

        return {
            **self.statistics(),
            "valid": (
                self._width >= 0
                and self._height >= 0
            ),
        }

###############################################################################
# Lifecycle
###############################################################################

    def reset(
        self,
    ) -> None:
        """
        Reset the viewport.
        """

        with self._lock:

            self._scroll_x = 0
            self._scroll_y = 0

            self._width = 0
            self._height = 0

            self._document_lines = 1

        logger.info(
            "Viewport reset.",
        )

###############################################################################
# Representation
###############################################################################

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}("
            f"size={self._width}x{self._height}, "
            f"scroll=({self._scroll_x}, {self._scroll_y}), "
            f"visible={self.first_visible_line}-"
            f"{self.last_visible_line})"
        )

###############################################################################
# Exports
###############################################################################

__all__ = [
    "Viewport",
]