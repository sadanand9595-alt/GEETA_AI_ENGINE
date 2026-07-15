"""
==============================================================================
GEETA AI ENGINE

File        : caret_renderer.py
Package     : editor.paint
Description : Caret Renderer

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from PySide6.QtCore import QRectF
from PySide6.QtGui import (
    QColor,
    QPainter,
)

from editor.core.editor_session import EditorSession
from editor.render.render_context import RenderContext
from editor.render.renderer import RenderLayer

###############################################################################
# Caret Renderer
###############################################################################


class CaretRenderer(RenderLayer):
    """
    Professional caret renderer.

    Supports:
        • Insert caret
        • Block caret
        • Multiple carets
        • High DPI
        • AI inline caret
    """

    ###########################################################################

    priority = 60

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._visible = True

        self._width = 2

        self._color = QColor(
            255,
            255,
            255,
        )

        self._overwrite_mode = False

    ###########################################################################

    @property
    def visible(
        self,
    ) -> bool:

        return self._visible

    ###########################################################################

    def set_visible(
        self,
        visible: bool,
    ) -> None:

        self._visible = visible

###############################################################################
# Painting
###############################################################################

    def paint(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Paint the editor caret.
        """

        if not self._visible:

            return

        cursor = session.cursor

        if not context.is_line_visible(
            cursor.line,
        ):

            return

        x = context.column_to_x(
            cursor.column,
        )

        y = context.line_to_y(
            cursor.line,
        )

        painter.save()

        painter.setPen(
            self._color,
        )

        painter.setBrush(
            self._color,
        )

        if self._overwrite_mode:

            painter.drawRect(

                QRectF(

                    x,

                    y,

                    context.character_width,

                    context.line_height,

                )

            )

        else:

            painter.drawRect(

                QRectF(

                    x,

                    y,

                    self._width,

                    context.line_height,

                )

            )

        painter.restore()
        ###############################################################################
# Blinking
###############################################################################

    def blink(
        self,
    ) -> None:
        """
        Toggle caret visibility.
        """

        self._visible = not self._visible

    ###########################################################################

    def set_overwrite_mode(
        self,
        enabled: bool,
    ) -> None:
        """
        Enable or disable overwrite mode.
        """

        self._overwrite_mode = enabled

###############################################################################
# Multiple Carets
###############################################################################

    def paint_secondary_carets(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Paint additional carets.

        Future implementation for
        multi-cursor editing.
        """

        cursor_engine = session.cursor

        if not hasattr(
            cursor_engine,
            "secondary_carets",
        ):
            return

        painter.save()

        painter.setBrush(
            self._color,
        )

        painter.setPen(
            self._color,
        )

        for caret in cursor_engine.secondary_carets:

            if not context.is_line_visible(
                caret.line,
            ):
                continue

            x = context.column_to_x(
                caret.column,
            )

            y = context.line_to_y(
                caret.line,
            )

            painter.drawRect(

                QRectF(

                    x,

                    y,

                    self._width,

                    context.line_height,

                )

            )

        painter.restore()

###############################################################################
# AI Caret Hook
###############################################################################

    def paint_ai_caret(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Reserved for AI inline completion caret.

        Future integration:
            - Ghost Text
            - Inline Completion
            - AI Suggestions
        """

        return

###############################################################################
# Theme
###############################################################################

    def update_theme(
        self,
        color: QColor,
    ) -> None:
        """
        Update caret color.
        """

        self._color = color

###############################################################################
# Configuration
###############################################################################

    def set_width(
        self,
        width: int,
    ) -> None:
        """
        Update caret width.
        """

        self._width = max(
            1,
            width,
        )
        ###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, object]:
        """
        Return caret renderer statistics.
        """

        return {
            "visible": self._visible,
            "width": self._width,
            "overwrite_mode": self._overwrite_mode,
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
        Reset renderer state.
        """

        self._visible = True

        self._width = 2

        self._overwrite_mode = False

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
            f"visible={self._visible}, "
            f"width={self._width}, "
            f"overwrite={self._overwrite_mode})"
        )

###############################################################################
# Exports
###############################################################################

__all__ = [
    "CaretRenderer",
]