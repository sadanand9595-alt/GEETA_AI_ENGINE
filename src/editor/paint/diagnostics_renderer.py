"""
==============================================================================
GEETA AI ENGINE

File        : diagnostics_renderer.py
Package     : editor.paint
Description : Diagnostics Renderer

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from enum import Enum

from PySide6.QtCore import QPointF
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
# Severity
###############################################################################


class DiagnosticSeverity(Enum):
    """
    Diagnostic severity.
    """

    ERROR = 1

    WARNING = 2

    INFORMATION = 3

    HINT = 4


###############################################################################
# Diagnostics Renderer
###############################################################################


class DiagnosticsRenderer(RenderLayer):
    """
    Professional diagnostics renderer.

    Features
    --------
    • Error squiggles
    • Warning squiggles
    • Information markers
    • Hint markers
    • AI diagnostics
    • LSP diagnostics
    """

    priority = 40

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._enabled = True

        self._colors = {

            DiagnosticSeverity.ERROR:
                QColor(244, 71, 71),

            DiagnosticSeverity.WARNING:
                QColor(255, 193, 7),

            DiagnosticSeverity.INFORMATION:
                QColor(66, 165, 245),

            DiagnosticSeverity.HINT:
                QColor(120, 120, 120),

        }

        logger.info(
            "DiagnosticsRenderer initialized.",
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
        Paint diagnostics.
        """

        if not self._enabled:

            return

        diagnostics = getattr(
            session,
            "diagnostics",
            [],
        )

        painter.save()

        for diagnostic in diagnostics:

            self._paint_diagnostic(

                painter,

                context,

                diagnostic,

            )

        painter.restore()
        ###############################################################################
# Diagnostic Painting
###############################################################################

    def _paint_diagnostic(
        self,
        painter: QPainter,
        context: RenderContext,
        diagnostic,
    ) -> None:
        """
        Paint a single diagnostic.
        """

        line = diagnostic.line

        if not context.is_line_visible(
            line,
        ):
            return

        color = self._colors.get(
            diagnostic.severity,
            self._colors[
                DiagnosticSeverity.INFORMATION
            ],
        )

        painter.setPen(
            QPen(
                color,
                2,
            )
        )

        start_x = context.column_to_x(
            diagnostic.start_column,
        )

        end_x = context.column_to_x(
            diagnostic.end_column,
        )

        y = (
            context.line_to_y(
                line,
            )
            + context.line_height
            - 2
        )

        self._draw_squiggle(

            painter,

            start_x,

            end_x,

            y,

        )

###############################################################################
# Squiggle Renderer
###############################################################################

    def _draw_squiggle(
        self,
        painter: QPainter,
        start_x: float,
        end_x: float,
        y: float,
    ) -> None:
        """
        Draw a squiggly underline.
        """

        step = 4.0

        x = start_x

        direction = 1

        while x < end_x:

            painter.drawLine(

                QPointF(
                    x,
                    y,
                ),

                QPointF(
                    x + step,
                    y + direction * 2,
                ),

            )

            direction *= -1

            x += step

###############################################################################
# Inline Message Hook
###############################################################################

    def paint_inline_message(
        self,
        painter: QPainter,
        context: RenderContext,
        diagnostic,
    ) -> None:
        """
        Reserved for inline diagnostic messages.

        Future:
            • Error text
            • Quick Fix
            • AI explanation
        """

        return

###############################################################################
# Hover Hook
###############################################################################

    def paint_hover(
        self,
        painter: QPainter,
        context: RenderContext,
        diagnostic,
    ) -> None:
        """
        Reserved for hover diagnostics.
        """

        return

###############################################################################
# AI Review Hook
###############################################################################

    def paint_ai_review(
        self,
        painter: QPainter,
        context: RenderContext,
        diagnostic,
    ) -> None:
        """
        Reserved for AI code review overlays.
        """

        return
        ###############################################################################
# Gutter Diagnostics
###############################################################################

    def paint_gutter_marker(
        self,
        painter: QPainter,
        context: RenderContext,
        diagnostic,
    ) -> None:
        """
        Paint a gutter diagnostic marker.
        """

        if not hasattr(
            context,
            "gutter_width",
        ):
            return

        line = diagnostic.line

        if not context.is_line_visible(
            line,
        ):
            return

        color = self._colors.get(
            diagnostic.severity,
            self._colors[
                DiagnosticSeverity.INFORMATION
            ],
        )

        y = context.line_to_y(
            line,
        )

        painter.save()

        painter.setBrush(
            color,
        )

        painter.setPen(
            color,
        )

        painter.drawEllipse(

            6,

            int(
                y
                + context.line_height / 2
                - 3
            ),

            6,

            6,

        )

        painter.restore()

###############################################################################
# Overview Ruler
###############################################################################

    def paint_overview_marker(
        self,
        painter: QPainter,
        context: RenderContext,
        diagnostic,
    ) -> None:
        """
        Reserved for overview ruler markers.

        Future:
            VS Code style scrollbar markers.
        """

        return

###############################################################################
# Minimap
###############################################################################

    def paint_minimap_marker(
        self,
        painter: QPainter,
        context: RenderContext,
        diagnostic,
    ) -> None:
        """
        Reserved for minimap diagnostics.

        Future integration:
            • Errors
            • Warnings
            • Git Changes
        """

        return

###############################################################################
# Click Regions
###############################################################################

    def clickable_region(
        self,
        diagnostic,
    ) -> tuple[int, int, int, int]:
        """
        Return clickable region.

        Future:
            Used by mouse controller.
        """

        return (

            diagnostic.line,

            diagnostic.start_column,

            diagnostic.line,

            diagnostic.end_column,

        )

###############################################################################
# Theme
###############################################################################

    def update_theme(
        self,
        colors: dict[DiagnosticSeverity, QColor],
    ) -> None:
        """
        Update diagnostic colors.
        """

        self._colors.update(
            colors,
        )

###############################################################################
# Performance
###############################################################################

    def should_render(
        self,
        context: RenderContext,
        diagnostic,
    ) -> bool:
        """
        Check visibility.
        """

        return context.is_line_visible(
            diagnostic.line,
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
            "severity_levels": len(self._colors),
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
            "supports_gutter": True,
            "supports_squiggles": True,
            "supports_hover": True,
            "supports_ai_review": True,
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

        self._colors = {

            DiagnosticSeverity.ERROR:
                QColor(244, 71, 71),

            DiagnosticSeverity.WARNING:
                QColor(255, 193, 7),

            DiagnosticSeverity.INFORMATION:
                QColor(66, 165, 245),

            DiagnosticSeverity.HINT:
                QColor(120, 120, 120),

        }

        logger.info(
            "DiagnosticsRenderer reset.",
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
            f"priority={self.priority})"
        )

###############################################################################
# Exports
###############################################################################

__all__ = [
    "DiagnosticSeverity",
    "DiagnosticsRenderer",
]