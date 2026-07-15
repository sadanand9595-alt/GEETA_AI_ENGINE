"""
==============================================================================
GEETA AI ENGINE

File        : gutter_renderer.py
Package     : editor.paint
Description : Professional Gutter Renderer

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

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
# Gutter Item
###############################################################################


@dataclass(slots=True)
class GutterItem:
    """
    Represents a single gutter decoration.
    """

    line: int
    icon: str
    color: QColor
    tooltip: str = ""

###############################################################################
# Gutter Renderer
###############################################################################


class GutterRenderer(RenderLayer):
    """
    Enterprise gutter renderer.

    Features
    --------
    • Breakpoints
    • Git decorations
    • Diagnostics
    • Bookmarks
    • Execution line
    • Fold indicators
    • AI actions
    """

    priority = 5

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._enabled = True

        self._width = 48

        self._background = QColor(
            30,
            30,
            30,
        )

        self._separator = QColor(
            60,
            60,
            60,
        )

        logger.info(
            "GutterRenderer initialized.",
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
        Paint gutter.
        """

        if not self._enabled:
            return

        painter.save()

        painter.fillRect(

            QRectF(

                0,

                0,

                self._width,

                context.viewport_height,

            ),

            self._background,

        )

        painter.setPen(
            QPen(
                self._separator,
            )
        )

        painter.drawLine(

            self._width - 1,

            0,

            self._width - 1,

            context.viewport_height,

        )

        self.paint_line_numbers(
            painter,
            context,
            session,
        )

        self.paint_breakpoints(
            painter,
            context,
            session,
        )

        self.paint_git_changes(
            painter,
            context,
            session,
        )

        self.paint_execution_line(
            painter,
            context,
            session,
        )

        painter.restore()
        ###############################################################################
# Line Numbers
###############################################################################

    def paint_line_numbers(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Paint visible line numbers.
        """

        painter.save()

        painter.setPen(
            QColor(
                140,
                140,
                140,
            )
        )

        for line in range(

            context.first_visible_line,

            context.last_visible_line + 1,

        ):

            y = (
                context.line_to_y(
                    line,
                )
                + context.line_height
                - 4
            )

            painter.drawText(

                4,

                int(y),

                str(line + 1),

            )

        painter.restore()

###############################################################################
# Breakpoints
###############################################################################

    def paint_breakpoints(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Paint debugger breakpoints.
        """

        breakpoints = getattr(
            session,
            "breakpoints",
            [],
        )

        painter.save()

        for breakpoint in breakpoints:

            if not context.is_line_visible(
                breakpoint.line,
            ):
                continue

            y = context.line_to_y(
                breakpoint.line,
            )

            painter.setBrush(
                QColor(
                    220,
                    50,
                    47,
                )
            )

            painter.setPen(
                QColor(
                    220,
                    50,
                    47,
                )
            )

            painter.drawEllipse(

                18,

                int(
                    y
                    + context.line_height / 2
                    - 5
                ),

                10,

                10,

            )

        painter.restore()

###############################################################################
# Git Decorations
###############################################################################

    def paint_git_changes(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Paint Git change indicators.

        States:
            • Added
            • Modified
            • Deleted
        """

        git_changes = getattr(
            session,
            "git_changes",
            [],
        )

        painter.save()

        for change in git_changes:

            if not context.is_line_visible(
                change.line,
            ):
                continue

            color = {

                "added": QColor(
                    46,
                    204,
                    113,
                ),

                "modified": QColor(
                    241,
                    196,
                    15,
                ),

                "deleted": QColor(
                    231,
                    76,
                    60,
                ),

            }.get(

                change.kind,

                QColor(
                    150,
                    150,
                    150,
                ),

            )

            y = context.line_to_y(
                change.line,
            )

            painter.fillRect(

                QRectF(

                    self._width - 3,

                    y,

                    3,

                    context.line_height,

                ),

                color,

            )

        painter.restore()

###############################################################################
# Execution Line
###############################################################################

    def paint_execution_line(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Paint debugger execution line.
        """

        execution_line = getattr(
            session,
            "execution_line",
            None,
        )

        if execution_line is None:
            return

        if not context.is_line_visible(
            execution_line,
        ):
            return

        y = context.line_to_y(
            execution_line,
        )

        painter.save()

        painter.setBrush(
            QColor(
                39,
                174,
                96,
            )
        )

        painter.setPen(
            QColor(
                39,
                174,
                96,
            )
        )

        painter.drawPolygon(

            [

                (30, int(y + 4)),
                (40, int(y + context.line_height / 2)),
                (30, int(y + context.line_height - 4)),

            ]

        )

        painter.restore()
        ###############################################################################
# Bookmarks
###############################################################################

    def paint_bookmarks(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Paint bookmark markers.
        """

        bookmarks = getattr(
            session,
            "bookmarks",
            [],
        )

        painter.save()

        bookmark_color = QColor(
            52,
            152,
            219,
        )

        painter.setBrush(
            bookmark_color,
        )

        painter.setPen(
            bookmark_color,
        )

        for bookmark in bookmarks:

            if not context.is_line_visible(
                bookmark.line,
            ):
                continue

            y = context.line_to_y(
                bookmark.line,
            )

            painter.drawRect(

                QRectF(

                    4,

                    y + 3,

                    8,

                    context.line_height - 6,

                )

            )

        painter.restore()

###############################################################################
# Diagnostics
###############################################################################

    def paint_diagnostics(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Paint gutter diagnostic icons.
        """

        diagnostics = getattr(
            session,
            "diagnostics",
            [],
        )

        painter.save()

        for diagnostic in diagnostics:

            if not context.is_line_visible(
                diagnostic.line,
            ):
                continue

            color = {

                "error": QColor(
                    231,
                    76,
                    60,
                ),

                "warning": QColor(
                    241,
                    196,
                    15,
                ),

                "info": QColor(
                    52,
                    152,
                    219,
                ),

                "hint": QColor(
                    149,
                    165,
                    166,
                ),

            }.get(

                diagnostic.kind,

                QColor(
                    180,
                    180,
                    180,
                ),

            )

            y = context.line_to_y(
                diagnostic.line,
            )

            painter.setBrush(
                color,
            )

            painter.setPen(
                color,
            )

            painter.drawEllipse(

                32,

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
# Fold Integration
###############################################################################

    def paint_fold_controls(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Reserved for fold indicator integration.
        """

        return

###############################################################################
# AI Actions
###############################################################################

    def paint_ai_actions(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Reserved for AI gutter actions.

        Future:
            • AI Fix
            • AI Explain
            • AI Refactor
            • AI Generate Tests
        """

        return

###############################################################################
# Mouse Interaction
###############################################################################

    def hit_test(
        self,
        x: float,
        y: float,
    ) -> bool:
        """
        Check whether a click belongs
        to the gutter.
        """

        return (

            0
            <= x
            <= self._width

        )
        ###############################################################################
# Theme
###############################################################################

    def update_theme(
        self,
        background: QColor,
        separator: QColor,
    ) -> None:
        """
        Update gutter colors.
        """

        self._background = background

        self._separator = separator

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
            "width": self._width,
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
            "supports_breakpoints": True,
            "supports_git": True,
            "supports_bookmarks": True,
            "supports_execution_line": True,
            "supports_diagnostics": True,
            "supports_ai_actions": True,
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

        self._width = 48

        self._background = QColor(
            30,
            30,
            30,
        )

        self._separator = QColor(
            60,
            60,
            60,
        )

        logger.info(
            "GutterRenderer reset.",
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
            f"width={self._width}, "
            f"priority={self.priority})"
        )

###############################################################################
# Exports
###############################################################################

__all__ = [
    "GutterItem",
    "GutterRenderer",
]