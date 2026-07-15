"""
==============================================================================
GEETA AI ENGINE

File        : text_renderer.py
Package     : editor.paint
Description : Professional Text Renderer

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from PySide6.QtCore import QPointF
from PySide6.QtGui import (
    QColor,
    QPainter,
    QTextLayout,
)

from config.logger import get_logger

from editor.core.editor_session import EditorSession
from editor.render.layout_engine import LayoutEngine
from editor.render.render_context import RenderContext
from editor.render.renderer import RenderLayer

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Text Renderer
###############################################################################


class TextRenderer(RenderLayer):
    """
    Professional text renderer.

    Responsibilities
    ----------------
    • Render visible source code
    • Unicode-safe drawing
    • High-DPI rendering
    • LayoutEngine integration
    • Future syntax highlighting
    """

    ###########################################################################

    priority = 30

    ###########################################################################

    def __init__(
        self,
        layout_engine: LayoutEngine,
    ) -> None:

        self._layout_engine = layout_engine

        self._foreground = QColor(
            220,
            220,
            220,
        )

        logger.info(
            "TextRenderer initialized.",
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
        Paint all visible document lines.
        """

        painter.save()

        painter.setPen(
            self._foreground,
        )

        document = session.document

        for line_number in range(

            context.first_visible_line,

            context.last_visible_line + 1,

        ):

            text = document.line_text(
                line_number,
            )

            layout: QTextLayout = (
                self._layout_engine.create_layout(
                    text,
                )
            )

            layout.draw(

                painter,

                QPointF(

                    0.0,

                    context.line_to_y(
                        line_number,
                    ),

                ),

            )

        painter.restore()
        ###############################################################################
# Cached Layout
###############################################################################

    def _create_layout(
        self,
        text: str,
    ) -> QTextLayout:
        """
        Create a layout for a single line.

        Future:
            RenderCache integration.
        """

        return self._layout_engine.create_layout(
            text,
        )

###############################################################################
# Visible Line
###############################################################################

    def paint_line(
        self,
        painter: QPainter,
        context: RenderContext,
        line_number: int,
        text: str,
    ) -> None:
        """
        Paint a single visible line.
        """

        layout = self._create_layout(
            text,
        )

        layout.draw(

            painter,

            QPointF(

                0.0,

                context.line_to_y(
                    line_number,
                ),

            ),

        )

###############################################################################
# Syntax Highlight Hook
###############################################################################

    def apply_syntax_highlighting(
        self,
        layout: QTextLayout,
        line_number: int,
        session: EditorSession,
    ) -> None:
        """
        Reserved for syntax highlighting.

        Future integration:
            • Python
            • C++
            • JavaScript
            • HTML
            • CSS
            • Markdown
            • JSON
        """

        return

###############################################################################
# Performance
###############################################################################

    def should_render_line(
        self,
        context: RenderContext,
        line_number: int,
    ) -> bool:
        """
        Check whether a line should be rendered.
        """

        return (
            context.first_visible_line
            <= line_number
            <= context.last_visible_line
        )

###############################################################################
# Clipping
###############################################################################

    def clip_line(
        self,
        painter: QPainter,
        context: RenderContext,
    ) -> None:
        """
        Apply viewport clipping.
        """

        painter.setClipRect(
            context.viewport,
        )
        ###############################################################################
# Cached Rendering
###############################################################################

    def paint_visible_lines(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Paint all visible lines.
        """

        document = session.document

        for line_number in range(
            context.first_visible_line,
            context.last_visible_line + 1,
        ):

            if not self.should_render_line(
                context,
                line_number,
            ):
                continue

            text = document.line_text(
                line_number,
            )

            self.paint_line(
                painter,
                context,
                line_number,
                text,
            )

###############################################################################
# Selection Awareness
###############################################################################

    def paint_selection_overlay(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Reserved for selection-aware glyph rendering.

        Future:
            • Transparent selections
            • Block selections
            • Multiple selections
        """

        return

###############################################################################
# Long Line Optimization
###############################################################################

    def trim_long_line(
        self,
        text: str,
        maximum_length: int = 50000,
    ) -> str:
        """
        Protect the renderer from pathological line lengths.
        """

        if len(text) <= maximum_length:
            return text

        logger.warning(
            "Long line truncated for rendering (%d chars).",
            len(text),
        )

        return text[:maximum_length]

###############################################################################
# Theme
###############################################################################

    def update_theme(
        self,
        foreground: QColor,
    ) -> None:
        """
        Update renderer foreground color.
        """

        self._foreground = foreground

###############################################################################
# High DPI
###############################################################################

    def device_pixel_ratio(
        self,
        painter: QPainter,
    ) -> float:
        """
        Return current device pixel ratio.
        """

        device = painter.device()

        if device is None:
            return 1.0

        return device.devicePixelRatioF()
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
            "priority": self.priority,
            "foreground": (
                self._foreground.red(),
                self._foreground.green(),
                self._foreground.blue(),
                self._foreground.alpha(),
            ),
            "font_family": (
                self._layout_engine.font.family()
            ),
            "line_height": (
                self._layout_engine.line_height()
            ),
            "character_width": (
                self._layout_engine.character_width()
            ),
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
            "unicode": True,
            "high_dpi": True,
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

        self._foreground = QColor(
            220,
            220,
            220,
        )

        logger.info(
            "TextRenderer reset.",
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
            f"font='{self._layout_engine.font.family()}', "
            f"priority={self.priority})"
        )

###############################################################################
# Exports
###############################################################################

__all__ = [
    "TextRenderer",
]