"""
==============================================================================
GEETA AI ENGINE

File        : current_line_renderer.py
Package     : editor.paint
Description : Current Line Renderer

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
# Current Line Renderer
###############################################################################


class CurrentLineRenderer(RenderLayer):
    """
    Paints the active editor line.

    Features
    --------
    • Active line highlight
    • Rounded background
    • Focus aware
    • Theme aware
    """

    ###########################################################################

    priority = 10

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._enabled = True

        self._radius = 2.0

        self._color = QColor(
            45,
            45,
            48,
            180,
        )

###############################################################################
# Configuration
###############################################################################

    def set_enabled(
        self,
        enabled: bool,
    ) -> None:
        """
        Enable or disable current line highlighting.
        """

        self._enabled = enabled

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
        Paint the active line background.
        """

        if not self._enabled:

            return

        if not context.show_current_line:

            return

        cursor = session.cursor

        if not context.is_line_visible(
            cursor.line,
        ):

            return

        y = context.line_to_y(
            cursor.line,
        )

        painter.save()

        painter.setPen(
            QColor(0, 0, 0, 0),
        )

        painter.setBrush(
            self._color,
        )

        painter.drawRoundedRect(

            QRectF(

                0,

                y,

                context.viewport_width,

                context.line_height,

            ),

            self._radius,

            self._radius,

        )

        painter.restore()
        ###############################################################################
# Theme
###############################################################################

    def update_theme(
        self,
        color: QColor,
    ) -> None:
        """
        Update highlight color.
        """

        self._color = color

###############################################################################
# Highlight Mode
###############################################################################

    def set_corner_radius(
        self,
        radius: float,
    ) -> None:
        """
        Update rounded corner radius.
        """

        self._radius = max(
            0.0,
            radius,
        )

###############################################################################
# Focus
###############################################################################

    def paint_inactive(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Reserved for inactive editor highlighting.

        Future:
            - Split Editors
            - Diff Editors
            - Preview Editors
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
        Reserved for future highlight animations.
        """

        return

###############################################################################
# Render Modes
###############################################################################

    def paint_text_width(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Reserved for text-width highlighting.

        Future:
            Highlight only behind visible text instead
            of the entire viewport width.
        """

        return

###############################################################################
# Future Hooks
###############################################################################

    def paint_ai_focus(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Reserved for AI editing focus.

        Future:
            • AI Refactor
            • AI Review
            • AI Edit Mode
        """

        return
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
            "corner_radius": self._radius,
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

        self._enabled = True

        self._radius = 2.0

        self._color = QColor(
            45,
            45,
            48,
            180,
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
            f"radius={self._radius})"
        )

###############################################################################
# Exports
###############################################################################

__all__ = [
    "CurrentLineRenderer",
]