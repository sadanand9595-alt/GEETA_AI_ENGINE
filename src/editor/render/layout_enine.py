"""
==============================================================================
GEETA AI ENGINE

File        : layout_engine.py
Package     : editor.render
Description : Text Layout Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from threading import RLock

from PySide6.QtGui import (
    QFont,
    QFontMetricsF,
    QTextLayout,
)

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Layout Engine
###############################################################################


class LayoutEngine:
    """
    Professional text layout engine.

    Responsibilities
    ----------------
    • Line layout
    • Glyph positioning
    • Tab expansion
    • Soft wrapping
    • Coordinate mapping

    Uses Qt QTextLayout for Unicode-safe rendering.
    """

    ###########################################################################

    def __init__(
        self,
        font: QFont,
    ) -> None:

        self._lock = RLock()

        self._font = font

        self._metrics = QFontMetricsF(
            font,
        )

        logger.info(
            "Layout Engine initialized.",
        )

###############################################################################
# Font
###############################################################################

    @property
    def font(
        self,
    ) -> QFont:

        return self._font

    ###########################################################################

    @property
    def metrics(
        self,
    ) -> QFontMetricsF:

        return self._metrics

###############################################################################
# Layout Creation
###############################################################################

    def create_layout(
        self,
        text: str,
    ) -> QTextLayout:
        """
        Create a QTextLayout for a single line.
        """

        layout = QTextLayout(
            text,
            self._font,
        )

        layout.beginLayout()

        line = layout.createLine()

        if line.isValid():

            line.setPosition(
                (0.0, 0.0),
            )

        layout.endLayout()

        return layout

###############################################################################
# Metrics
###############################################################################

    def line_height(
        self,
    ) -> float:
        """
        Return line height.
        """

        return self._metrics.height()

    ###########################################################################

    def character_width(
        self,
    ) -> float:
        """
        Return average character width.
        """

        return self._metrics.averageCharWidth()
        ###############################################################################
# Coordinate Mapping
###############################################################################

    def x_to_column(
        self,
        layout: QTextLayout,
        x: float,
    ) -> int:
        """
        Convert an X coordinate to a text column.
        """

        line = layout.lineAt(0)

        if not line.isValid():

            return 0

        return line.xToCursor(
            x,
        )

    ###########################################################################

    def column_to_x(
        self,
        layout: QTextLayout,
        column: int,
    ) -> float:
        """
        Convert a text column to an X coordinate.
        """

        line = layout.lineAt(0)

        if not line.isValid():

            return 0.0

        return line.cursorToX(
            max(0, column),
        )

###############################################################################
# Cursor Position
###############################################################################

    def cursor_position(
        self,
        layout: QTextLayout,
        column: int,
    ) -> tuple[float, float]:
        """
        Return cursor X/Y position.
        """

        line = layout.lineAt(0)

        if not line.isValid():

            return (
                0.0,
                0.0,
            )

        return (
            line.cursorToX(column),
            line.y(),
        )

###############################################################################
# Tabs
###############################################################################

    def tab_width(
        self,
        tab_size: int = 4,
    ) -> float:
        """
        Return the visual width of a tab.
        """

        return (
            self.character_width()
            * tab_size
        )

###############################################################################
# Wrapping
###############################################################################

    def wrap_layout(
        self,
        layout: QTextLayout,
        width: float,
    ) -> None:
        """
        Apply soft wrapping to a layout.
        """

        layout.beginLayout()

        while True:

            line = layout.createLine()

            if not line.isValid():

                break

            line.setLineWidth(
                width,
            )

        layout.endLayout()

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, float]:
        """
        Return layout statistics.
        """

        return {
            "line_height": self.line_height(),
            "character_width": self.character_width(),
            "tab_width": self.tab_width(),
        }
        ###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return layout engine diagnostics.
        """

        return {
            **self.statistics(),
            "font_family": self._font.family(),
            "font_size": self._font.pointSizeF(),
            "fixed_pitch": self._font.fixedPitch(),
        }

###############################################################################
# Lifecycle
###############################################################################

    def reset(
        self,
    ) -> None:
        """
        Reset layout engine.

        Reserved for future cache cleanup.
        """

        logger.info(
            "Layout Engine reset.",
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

        return (
            f"{self.__class__.__name__}("
            f"font='{self._font.family()}', "
            f"size={self._font.pointSizeF():.1f})"
        )

###############################################################################
# Future Extension Hooks
###############################################################################

    def invalidate_cache(
        self,
    ) -> None:
        """
        Invalidate cached layouts.

        Future integration point for RenderCache.
        """

        logger.debug(
            "Layout cache invalidated.",
        )

###############################################################################
# Exports
###############################################################################

__all__ = [
    "LayoutEngine",
]