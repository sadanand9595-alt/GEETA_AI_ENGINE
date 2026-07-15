"""
==============================================================================
GEETA AI ENGINE

File        : whitespace_renderer.py
Package     : editor.paint
Description : Whitespace Renderer

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

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
# Whitespace Renderer
###############################################################################


class WhitespaceRenderer(RenderLayer):
    """
    Professional whitespace renderer.

    Features
    --------
    • Space markers
    • Tab markers
    • End-of-line markers
    • Indentation guides
    • Trailing whitespace indicators
    """

    priority = 35

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._enabled = True

        self._show_spaces = False

        self._show_tabs = True

        self._show_eol = False

        self._show_indent_guides = True

        self._color = QColor(
            110,
            110,
            110,
            140,
        )

        logger.info(
            "WhitespaceRenderer initialized.",
        )

###############################################################################
# Configuration
###############################################################################

    def set_enabled(
        self,
        enabled: bool,
    ) -> None:

        self._enabled = enabled

    ###########################################################################

    def update_theme(
        self,
        color: QColor,
    ) -> None:

        self._color = color

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
        Paint invisible characters.
        """

        if not self._enabled:

            return

        painter.save()

        painter.setPen(
            QPen(
                self._color,
            )
        )

        document = session.document

        for line_number in range(

            context.first_visible_line,

            context.last_visible_line + 1,

        ):

            text = document.line_text(
                line_number,
            )

            self._paint_line(

                painter,

                context,

                line_number,

                text,

            )

        painter.restore()
        ###############################################################################
# Line Rendering
###############################################################################

    def _paint_line(
        self,
        painter: QPainter,
        context: RenderContext,
        line_number: int,
        text: str,
    ) -> None:
        """
        Paint whitespace for a single line.
        """

        y = context.line_to_y(
            line_number,
        )

        x = 0.0

        for character in text:

            if (
                character == " "
                and self._show_spaces
            ):

                self._draw_space(
                    painter,
                    x,
                    y,
                    context,
                )

            elif (
                character == "\t"
                and self._show_tabs
            ):

                self._draw_tab(
                    painter,
                    x,
                    y,
                    context,
                )

            x += context.character_width

        if self._show_eol:

            self._draw_eol(
                painter,
                x,
                y,
                context,
            )

        if self._show_indent_guides:

            self._draw_indent_guides(
                painter,
                text,
                y,
                context,
            )

###############################################################################
# Character Rendering
###############################################################################

    def _draw_space(
        self,
        painter: QPainter,
        x: float,
        y: float,
        context: RenderContext,
    ) -> None:
        """
        Draw a visible space marker.
        """

        painter.drawText(
            QPointF(
                x,
                y + context.line_height - 4,
            ),
            "·",
        )

    ###########################################################################

    def _draw_tab(
        self,
        painter: QPainter,
        x: float,
        y: float,
        context: RenderContext,
    ) -> None:
        """
        Draw a visible tab marker.
        """

        painter.drawText(
            QPointF(
                x,
                y + context.line_height - 4,
            ),
            "→",
        )

    ###########################################################################

    def _draw_eol(
        self,
        painter: QPainter,
        x: float,
        y: float,
        context: RenderContext,
    ) -> None:
        """
        Draw end-of-line marker.
        """

        painter.drawText(
            QPointF(
                x + 2,
                y + context.line_height - 4,
            ),
            "↵",
        )

###############################################################################
# Indentation Guides
###############################################################################

    def _draw_indent_guides(
        self,
        painter: QPainter,
        text: str,
        y: float,
        context: RenderContext,
    ) -> None:
        """
        Draw indentation guide lines.
        """

        indentation = 0

        for character in text:

            if character == " ":

                indentation += 1

            elif character == "\t":

                indentation += 4

            else:

                break

        level = indentation // 4

        for index in range(level):

            x = (
                (index + 1)
                * context.character_width
                * 4
            )

            painter.drawLine(

                int(x),

                int(y),

                int(x),

                int(
                    y + context.line_height
                ),

            )
            ###############################################################################
# Trailing Whitespace
###############################################################################

    def _draw_trailing_whitespace(
        self,
        painter: QPainter,
        text: str,
        y: float,
        context: RenderContext,
    ) -> None:
        """
        Highlight trailing whitespace.
        """

        stripped = text.rstrip(" \t")

        if len(stripped) == len(text):
            return

        start = len(stripped)

        x = start * context.character_width

        width = (
            len(text) - start
        ) * context.character_width

        painter.fillRect(

            x,

            y,

            width,

            context.line_height,

            QColor(
                255,
                80,
                80,
                80,
            ),

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
            "spaces": self._show_spaces,
            "tabs": self._show_tabs,
            "eol": self._show_eol,
            "indent_guides": self._show_indent_guides,
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
            "priority": self.priority,
            "color": (
                self._color.red(),
                self._color.green(),
                self._color.blue(),
                self._color.alpha(),
            ),
        }

###############################################################################
# Lifecycle
###############################################################################

    def reset(
        self,
    ) -> None:
        """
        Reset renderer configuration.
        """

        self._enabled = True

        self._show_spaces = False

        self._show_tabs = True

        self._show_eol = False

        self._show_indent_guides = True

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
    "WhitespaceRenderer",
]