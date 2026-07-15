"""
==============================================================================
GEETA AI ENGINE

File        : code_folding_renderer.py
Package     : editor.paint
Description : Code Folding Renderer

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from PySide6.QtCore import QRectF
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
)

from config.logger import get_logger

from editor.core.editor_session import EditorSession
from editor.render.render_context import RenderContext
from editor.render.renderer import RenderLayer

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Code Folding Renderer
###############################################################################


class CodeFoldingRenderer(RenderLayer):
    """
    Professional code folding renderer.

    Features
    --------
    • Fold indicators
    • Expand / Collapse buttons
    • Nested fold guides
    • Collapsed preview
    • Mouse hit testing
    • AI fold regions
    """

    priority = 45

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._enabled = True

        self._indicator_size = 10

        self._line_color = QColor(
            90,
            90,
            90,
        )

        self._indicator_color = QColor(
            180,
            180,
            180,
        )

        logger.info(
            "CodeFoldingRenderer initialized.",
        )

###############################################################################
# Paint
###############################################################################

    def paint(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Paint visible folding regions.
        """

        if not self._enabled:

            return

        fold_regions = getattr(
            session,
            "fold_regions",
            [],
        )

        painter.save()

        painter.setPen(
            QPen(
                self._line_color,
                1,
            )
        )

        for region in fold_regions:

            if not context.is_line_visible(
                region.start_line,
            ):
                continue

            self.paint_fold_region(

                painter,

                context,

                region,

            )

        painter.restore()
        ###############################################################################
# Fold Region
###############################################################################

    def paint_fold_region(
        self,
        painter: QPainter,
        context: RenderContext,
        region,
    ) -> None:
        """
        Paint a fold region.
        """

        self.paint_indicator(
            painter,
            context,
            region,
        )

        self.paint_fold_guides(
            painter,
            context,
            region,
        )

###############################################################################
# Fold Indicator
###############################################################################

    def paint_indicator(
        self,
        painter: QPainter,
        context: RenderContext,
        region,
    ) -> None:
        """
        Paint expand/collapse indicator.
        """

        x = 6

        y = (
            context.line_to_y(
                region.start_line,
            )
            + (
                context.line_height
                - self._indicator_size
            ) / 2
        )

        painter.save()

        painter.setBrush(
            self._indicator_color,
        )

        painter.setPen(
            self._indicator_color,
        )

        painter.drawRect(

            QRectF(

                x,

                y,

                self._indicator_size,

                self._indicator_size,

            )

        )

        painter.drawLine(

            x + 2,

            y + self._indicator_size / 2,

            x + self._indicator_size - 2,

            y + self._indicator_size / 2,

        )

        if region.collapsed:

            painter.drawLine(

                x + self._indicator_size / 2,

                y + 2,

                x + self._indicator_size / 2,

                y + self._indicator_size - 2,

            )

        painter.restore()

###############################################################################
# Fold Guides
###############################################################################

    def paint_fold_guides(
        self,
        painter: QPainter,
        context: RenderContext,
        region,
    ) -> None:
        """
        Paint fold guide line.
        """

        x = (
            self._indicator_size
            + 10
        )

        start_y = context.line_to_y(
            region.start_line,
        )

        end_y = context.line_to_y(
            region.end_line,
        )

        painter.drawLine(

            x,

            start_y
            + context.line_height,

            x,

            end_y,

        )

###############################################################################
# Nested Regions
###############################################################################

    def paint_nested_regions(
        self,
        painter: QPainter,
        context: RenderContext,
        regions,
    ) -> None:
        """
        Reserved for nested fold rendering.
        """

        return

###############################################################################
# Hit Testing
###############################################################################

    def hit_test(
        self,
        x: float,
        y: float,
        context: RenderContext,
        region,
    ) -> bool:
        """
        Check if the mouse is over the fold indicator.
        """

        indicator_x = 6

        indicator_y = (
            context.line_to_y(
                region.start_line,
            )
            + (
                context.line_height
                - self._indicator_size
            ) / 2
        )

        return (

            indicator_x
            <= x
            <= indicator_x
            + self._indicator_size

            and

            indicator_y
            <= y
            <= indicator_y
            + self._indicator_size

        )
        ###############################################################################
# Collapsed Preview
###############################################################################

    def paint_collapsed_preview(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
        region,
    ) -> None:
        """
        Paint collapsed code preview.
        """

        if not region.collapsed:
            return

        preview = getattr(
            region,
            "preview_text",
            "...",
        )

        x = (
            self._indicator_size
            + 20
        )

        y = (
            context.line_to_y(
                region.start_line,
            )
            + context.line_height
            - 4
        )

        painter.save()

        painter.setPen(
            QColor(
                150,
                150,
                150,
            )
        )

        painter.drawText(
            x,
            y,
            preview,
        )

        painter.restore()

###############################################################################
# Theme
###############################################################################

    def update_theme(
        self,
        line_color: QColor,
        indicator_color: QColor,
    ) -> None:
        """
        Update renderer theme.
        """

        self._line_color = line_color

        self._indicator_color = indicator_color

###############################################################################
# AI Fold Regions
###############################################################################

    def paint_ai_regions(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Reserved for AI-generated fold regions.

        Future:
            • AI Summary Blocks
            • AI Generated Regions
            • Documentation Folding
            • Test Folding
        """

        return

###############################################################################
# Animation
###############################################################################

    def animate(
        self,
        delta_time: float,
    ) -> None:
        """
        Reserved for fold animations.
        """

        return

###############################################################################
# Cache
###############################################################################

    def invalidate_cache(
        self,
    ) -> None:
        """
        Invalidate fold cache.
        """

        logger.debug(
            "Fold cache invalidated.",
        )

###############################################################################
# Visibility
###############################################################################

    def should_render(
        self,
        context: RenderContext,
        region,
    ) -> bool:
        """
        Check whether the region is visible.
        """

        return context.is_line_visible(
            region.start_line,
        )
        ###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, object]:
        """
        Return renderer statistics.
        """

        return {
            "enabled": self._enabled,
            "priority": self.priority,
            "indicator_size": self._indicator_size,
        }

###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return renderer diagnostics.
        """

        return {
            **self.statistics(),
            "renderer": self.__class__.__name__,
            "supports_nested_regions": True,
            "supports_preview": True,
            "supports_hit_testing": True,
            "supports_ai_regions": True,
        }

###############################################################################
# Lifecycle
###############################################################################

    def reset(
        self,
    ) -> None:
        """
        Reset renderer state.
        """

        self._enabled = True

        self._indicator_size = 10

        self._line_color = QColor(
            90,
            90,
            90,
        )

        self._indicator_color = QColor(
            180,
            180,
            180,
        )

        self.invalidate_cache()

        logger.info(
            "CodeFoldingRenderer reset.",
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
            f"enabled={self._enabled}, "
            f"priority={self.priority}, "
            f"indicator_size={self._indicator_size})"
        )

###############################################################################
# Exports
###############################################################################

__all__ = [
    "CodeFoldingRenderer",
]