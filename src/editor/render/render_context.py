"""
==============================================================================
GEETA AI ENGINE

File        : render_context.py
Package     : editor.render
Description : Render Context

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from PySide6.QtCore import QRect

if TYPE_CHECKING:
    from PySide6.QtGui import (
        QColor,
        QFontMetricsF,
    )

###############################################################################
# Render Context
###############################################################################


@dataclass(slots=True, frozen=True)
class RenderContext:
    """
    Immutable rendering context shared by all
    render layers.

    Every paint pass receives exactly one
    RenderContext instance.
    """

    ###########################################################################
    # Viewport
    ###########################################################################

    viewport: QRect

    scroll_x: int

    scroll_y: int

    ###########################################################################
    # Visible Region
    ###########################################################################

    first_visible_line: int

    last_visible_line: int

    ###########################################################################
    # Character Metrics
    ###########################################################################

    line_height: float

    character_width: float

    font_metrics: QFontMetricsF

    ###########################################################################
    # Theme
    ###########################################################################

    background_color: QColor

    foreground_color: QColor

    selection_color: QColor

    caret_color: QColor

    current_line_color: QColor

    ###########################################################################
    # Rendering Flags
    ###########################################################################

    show_line_numbers: bool

    show_whitespace: bool

    show_current_line: bool

    show_diagnostics: bool

    show_minimap: bool

    dpi_scale: float = 1.0

###############################################################################
# Helper Methods
###############################################################################

    @property
    def visible_line_count(
        self,
    ) -> int:
        """
        Number of visible lines.
        """

        return max(
            0,
            self.last_visible_line
            - self.first_visible_line
            + 1,
        )

    ###########################################################################

    @property
    def viewport_height(
        self,
    ) -> int:
        """
        Viewport height.
        """

        return self.viewport.height()

    ###########################################################################

    @property
    def viewport_width(
        self,
    ) -> int:
        """
        Viewport width.
        """

        return self.viewport.width()
        ###############################################################################
# Geometry Helpers
###############################################################################

    def line_to_y(
        self,
        line: int,
    ) -> float:
        """
        Convert a document line number to a viewport Y coordinate.
        """

        return (
            (line - self.first_visible_line)
            * self.line_height
            - self.scroll_y
        )

    ###########################################################################

    def column_to_x(
        self,
        column: int,
    ) -> float:
        """
        Convert a document column to a viewport X coordinate.
        """

        return (
            column * self.character_width
            - self.scroll_x
        )

###############################################################################
# Visibility
###############################################################################

    def is_line_visible(
        self,
        line: int,
    ) -> bool:
        """
        Return True if the line is inside the visible viewport.
        """

        return (
            self.first_visible_line
            <= line
            <= self.last_visible_line
        )

    ###########################################################################

    def is_point_visible(
        self,
        x: float,
        y: float,
    ) -> bool:
        """
        Return True if the viewport contains the point.
        """

        return (
            0 <= x <= self.viewport_width
            and
            0 <= y <= self.viewport_height
        )

###############################################################################
# Coordinate Conversion
###############################################################################

    def viewport_to_line(
        self,
        y: float,
    ) -> int:
        """
        Convert viewport Y coordinate to document line.
        """

        return (
            self.first_visible_line
            + int(
                (y + self.scroll_y)
                / self.line_height
            )
        )

    ###########################################################################

    def viewport_to_column(
        self,
        x: float,
    ) -> int:
        """
        Convert viewport X coordinate to document column.
        """

        return int(
            (x + self.scroll_x)
            / self.character_width
        )

###############################################################################
# Render Flags
###############################################################################

    def is_feature_enabled(
        self,
        feature: str,
    ) -> bool:
        """
        Return True if a rendering feature is enabled.
        """

        features = {
            "line_numbers": self.show_line_numbers,
            "whitespace": self.show_whitespace,
            "current_line": self.show_current_line,
            "diagnostics": self.show_diagnostics,
            "minimap": self.show_minimap,
        }

        return features.get(
            feature,
            False,
        )
        ###############################################################################
# Geometry Helpers
###############################################################################

    def line_to_y(
        self,
        line: int,
    ) -> float:
        """
        Convert a document line number to a viewport Y coordinate.
        """

        return (
            (line - self.first_visible_line)
            * self.line_height
            - self.scroll_y
        )

    ###########################################################################

    def column_to_x(
        self,
        column: int,
    ) -> float:
        """
        Convert a document column to a viewport X coordinate.
        """

        return (
            column * self.character_width
            - self.scroll_x
        )

###############################################################################
# Visibility
###############################################################################

    def is_line_visible(
        self,
        line: int,
    ) -> bool:
        """
        Return True if the line is inside the visible viewport.
        """

        return (
            self.first_visible_line
            <= line
            <= self.last_visible_line
        )

    ###########################################################################

    def is_point_visible(
        self,
        x: float,
        y: float,
    ) -> bool:
        """
        Return True if the viewport contains the point.
        """

        return (
            0 <= x <= self.viewport_width
            and
            0 <= y <= self.viewport_height
        )

###############################################################################
# Coordinate Conversion
###############################################################################

    def viewport_to_line(
        self,
        y: float,
    ) -> int:
        """
        Convert viewport Y coordinate to document line.
        """

        return (
            self.first_visible_line
            + int(
                (y + self.scroll_y)
                / self.line_height
            )
        )

    ###########################################################################

    def viewport_to_column(
        self,
        x: float,
    ) -> int:
        """
        Convert viewport X coordinate to document column.
        """

        return int(
            (x + self.scroll_x)
            / self.character_width
        )

###############################################################################
# Render Flags
###############################################################################

    def is_feature_enabled(
        self,
        feature: str,
    ) -> bool:
        """
        Return True if a rendering feature is enabled.
        """

        features = {
            "line_numbers": self.show_line_numbers,
            "whitespace": self.show_whitespace,
            "current_line": self.show_current_line,
            "diagnostics": self.show_diagnostics,
            "minimap": self.show_minimap,
        }

        return features.get(
            feature,
            False,
        )