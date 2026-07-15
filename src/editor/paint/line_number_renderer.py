"""
==============================================================================
GEETA AI ENGINE

File        : line_number_renderer.py
Package     : editor.paint
Description : Line Number Renderer

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QColor,
    QFont,
    QPainter,
)

from editor.render.renderer import RenderLayer
from editor.render.render_context import RenderContext
from editor.core.editor_session import EditorSession

###############################################################################
# Line Number Renderer
###############################################################################


class LineNumberRenderer(RenderLayer):
    """
    Paints editor line numbers.
    """

    ###########################################################################

    priority = 5

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._width = 60

        self._background = QColor(
            37,
            37,
            38,
        )

        self._foreground = QColor(
            133,
            133,
            133,
        )

        self._font = QFont(
            "JetBrains Mono",
            10,
        )

    ###########################################################################

    @property
    def width(
        self,
    ) -> int:
        """
        Width of the line number area.
        """

        return self._width

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
        Paint visible line numbers.
        """

        if not context.show_line_numbers:

            return

        painter.save()

        painter.setFont(
            self._font,
        )

        painter.fillRect(

            0,

            0,

            self._width,

            context.viewport_height,

            self._background,

        )

        painter.setPen(
            self._foreground,
        )

        for line in range(

            context.first_visible_line,

            context.last_visible_line + 1,

        ):

            y = context.line_to_y(
                line,
            )

            painter.drawText(

                0,

                int(y),

                self._width - 8,

                int(context.line_height),

                Qt.AlignRight
                | Qt.AlignVCenter,

                str(line + 1),

            )

        painter.restore()
        ###############################################################################
# Configuration
###############################################################################

    def set_width(
        self,
        width: int,
    ) -> None:
        """
        Update gutter width.
        """

        self._width = max(
            40,
            width,
        )

    ###########################################################################

    def gutter_width(
        self,
        total_lines: int,
    ) -> int:
        """
        Calculate dynamic gutter width.
        """

        digits = max(
            2,
            len(str(max(1, total_lines))),
        )

        return max(
            40,
            20 + digits * 10,
        )

###############################################################################
# Current Line
###############################################################################

    def draw_current_line(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Highlight the current line number.
        """

        current_line = (
            session.cursor.line
        )

        if not context.is_line_visible(
            current_line,
        ):

            return

        painter.setPen(
            QColor(
                255,
                255,
                255,
            ),
        )

        y = context.line_to_y(
            current_line,
        )

        painter.drawText(

            0,

            int(y),

            self._width - 8,

            int(context.line_height),

            Qt.AlignRight
            | Qt.AlignVCenter,

            str(current_line + 1),

        )

###############################################################################
# Future Hooks
###############################################################################

    def draw_breakpoints(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Reserved for breakpoint rendering.
        """

        return

    ###########################################################################

    def draw_git_decorations(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Reserved for Git decorations.
        """

        return

    ###########################################################################

    def draw_folding_markers(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Reserved for code folding markers.
        """

        return
        ###############################################################################
# Theme
###############################################################################

    def update_theme(
        self,
        background: QColor,
        foreground: QColor,
    ) -> None:
        """
        Update renderer colors.
        """

        self._background = background

        self._foreground = foreground

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return renderer statistics.
        """

        return {
            "gutter_width": self._width,
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
            "font_family": self._font.family(),
            "font_size": self._font.pointSize(),
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

        self._width = 60

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
            f"width={self._width})"
        )

###############################################################################
# Exports
###############################################################################

__all__ = [
    "LineNumberRenderer",
]