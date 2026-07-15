"""
==============================================================================
GEETA AI ENGINE

File        : selection_renderer.py
Package     : editor.paint
Description : Selection Renderer

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
# Selection Renderer
###############################################################################


class SelectionRenderer(RenderLayer):
    """
    Professional selection renderer.

    Supports
    --------
    • Single selection
    • Multi selection
    • Rectangular selection
    • Search highlight
    • AI highlight
    """

    ###########################################################################

    priority = 20

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._color = QColor(
            38,
            79,
            120,
            180,
        )

        self._border = QColor(
            70,
            120,
            180,
        )

        self._radius = 2.0

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
        Paint text selections.
        """

        selection = session.selection.primary

        if selection.empty:

            return

        painter.save()

        painter.setBrush(
            self._color,
        )

        painter.setPen(
            self._border,
        )

        start_line = session.document.offset_to_line(
            selection.normalized[0],
        )

        end_line = session.document.offset_to_line(
            selection.normalized[1],
        )

        for line in range(
            start_line,
            end_line + 1,
        ):

            if not context.is_line_visible(
                line,
            ):
                continue

            y = context.line_to_y(
                line,
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
# Multi Selection
###############################################################################

    def paint_multi_selection(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Paint all secondary selections.
        """

        selections = session.selection.selections

        if len(selections) <= 1:

            return

        painter.save()

        painter.setBrush(
            self._color,
        )

        painter.setPen(
            self._border,
        )

        for selection in selections[1:]:

            if selection.empty:

                continue

            start, end = selection.normalized

            start_line = session.document.offset_to_line(
                start,
            )

            end_line = session.document.offset_to_line(
                end,
            )

            for line in range(
                start_line,
                end_line + 1,
            ):

                if not context.is_line_visible(
                    line,
                ):

                    continue

                y = context.line_to_y(
                    line,
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
# Rectangular Selection
###############################################################################

    def paint_rectangular_selection(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Reserved for column selection rendering.
        """

        return

###############################################################################
# Search Highlight
###############################################################################

    def paint_search_highlight(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Reserved for search result highlighting.
        """

        return

###############################################################################
# AI Highlight
###############################################################################

    def paint_ai_highlight(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Reserved for AI-generated highlights.

        Future:
            • Explain Code
            • AI Refactor
            • AI Review
            • AI Error Fix
        """

        return

###############################################################################
# Matching Words
###############################################################################

    def paint_matching_words(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Reserved for matching word highlights.
        """

        return
        ###############################################################################
# Theme
###############################################################################

    def update_theme(
        self,
        fill_color: QColor,
        border_color: QColor,
    ) -> None:
        """
        Update selection colors.
        """

        self._color = fill_color

        self._border = border_color

###############################################################################
# Configuration
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
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, object]:
        """
        Return renderer statistics.
        """

        return {
            "corner_radius": self._radius,
            "alpha": self._color.alpha(),
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
            "fill_color": (
                self._color.red(),
                self._color.green(),
                self._color.blue(),
                self._color.alpha(),
            ),
            "border_color": (
                self._border.red(),
                self._border.green(),
                self._border.blue(),
                self._border.alpha(),
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

        self._radius = 2.0

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
            f"radius={self._radius})"
        )

###############################################################################
# Exports
###############################################################################

__all__ = [
    "SelectionRenderer",
]