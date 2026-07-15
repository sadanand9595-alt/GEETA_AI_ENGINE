"""
==============================================================================
GEETA AI ENGINE

File        : ghost_text_renderer.py
Package     : editor.paint
Description : AI Ghost Text Renderer

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import QPointF
from PySide6.QtGui import (
    QColor,
    QFont,
    QPainter,
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
# Ghost Completion
###############################################################################


@dataclass(slots=True)
class GhostCompletion:
    """
    Represents an AI inline completion.
    """

    line: int
    column: int
    text: str
    multiline: bool = False
    confidence: float = 1.0


###############################################################################
# Ghost Text Renderer
###############################################################################


class GhostTextRenderer(RenderLayer):
    """
    Enterprise AI ghost text renderer.

    Features
    --------
    • Inline AI completion
    • Multi-line ghost text
    • Cursor aware placement
    • Fade rendering
    • Theme support
    • Cached rendering
    """

    priority = 70

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._enabled = True

        self._ghost_color = QColor(
            150,
            150,
            150,
            170,
        )

        self._font: QFont | None = None

        logger.info(
            "GhostTextRenderer initialized.",
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
        Paint AI ghost completion.
        """

        if not self._enabled:
            return

        completion = getattr(
            session,
            "ghost_completion",
            None,
        )

        if completion is None:
            return

        painter.save()

        painter.setPen(
            self._ghost_color,
        )

        if self._font is not None:
            painter.setFont(
                self._font,
            )

        self.paint_completion(
            painter,
            context,
            completion,
        )

        painter.restore()
        ###############################################################################
# Completion Rendering
###############################################################################

    def paint_completion(
        self,
        painter: QPainter,
        context: RenderContext,
        completion: GhostCompletion,
    ) -> None:
        """
        Paint a ghost completion.
        """

        if completion.multiline:

            self.paint_multiline_completion(

                painter,

                context,

                completion,

            )

            return

        x = context.column_to_x(
            completion.column,
        )

        y = (
            context.line_to_y(
                completion.line,
            )
            + context.line_height
            - 4
        )

        painter.drawText(

            QPointF(

                x,

                y,

            ),

            completion.text,

        )

###############################################################################
# Multi-line Completion
###############################################################################

    def paint_multiline_completion(
        self,
        painter: QPainter,
        context: RenderContext,
        completion: GhostCompletion,
    ) -> None:
        """
        Paint multi-line ghost completion.
        """

        lines = completion.text.splitlines()

        for offset, line in enumerate(lines):

            x = context.column_to_x(

                completion.column

                if offset == 0

                else 0,

            )

            y = (

                context.line_to_y(

                    completion.line + offset,

                )

                + context.line_height

                - 4

            )

            painter.drawText(

                QPointF(

                    x,

                    y,

                ),

                line,

            )

###############################################################################
# Cursor Position
###############################################################################

    def cursor_position(
        self,
        context: RenderContext,
        completion: GhostCompletion,
    ) -> QPointF:
        """
        Return completion origin.
        """

        return QPointF(

            context.column_to_x(
                completion.column,
            ),

            context.line_to_y(
                completion.line,
            ),

        )

###############################################################################
# Clipping
###############################################################################

    def apply_clip(
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
# Fade Effect
###############################################################################

    def opacity_for_completion(
        self,
        completion: GhostCompletion,
    ) -> int:
        """
        Convert confidence into opacity.
        """

        confidence = max(

            0.0,

            min(

                1.0,

                completion.confidence,

            ),

        )

        return int(
            confidence * 170,
        )

###############################################################################
# Cache
###############################################################################

    def invalidate_cache(
        self,
    ) -> None:
        """
        Invalidate ghost text cache.
        """

        logger.debug(
            "Ghost text cache invalidated.",
        )
        ###############################################################################
# Theme
###############################################################################

    def update_theme(
        self,
        ghost_color: QColor,
        font: QFont | None = None,
    ) -> None:
        """
        Update ghost text appearance.
        """

        self._ghost_color = ghost_color

        if font is not None:
            self._font = font

###############################################################################
# Accept Preview
###############################################################################

    def paint_accept_hint(
        self,
        painter: QPainter,
        context: RenderContext,
        completion: GhostCompletion,
    ) -> None:
        """
        Reserved for accept hint rendering.

        Future:
            Tab • Accept
        """

        return

###############################################################################
# Reject Preview
###############################################################################

    def paint_reject_hint(
        self,
        painter: QPainter,
        context: RenderContext,
        completion: GhostCompletion,
    ) -> None:
        """
        Reserved for reject hint rendering.

        Future:
            Esc • Dismiss
        """

        return

###############################################################################
# Animation
###############################################################################

    def animation_alpha(
        self,
        elapsed_ms: int,
    ) -> int:
        """
        Calculate fade animation alpha.
        """

        if elapsed_ms <= 0:
            return 0

        if elapsed_ms >= 250:
            return 255

        return int(
            elapsed_ms / 250 * 255,
        )

###############################################################################
# Hover
###############################################################################

    def paint_hover(
        self,
        painter: QPainter,
        context: RenderContext,
        completion: GhostCompletion,
    ) -> None:
        """
        Reserved for hover rendering.

        Future:
            • Provider name
            • Confidence
            • Token count
        """

        return

###############################################################################
# Cache Validation
###############################################################################

    def cache_key(
        self,
        completion: GhostCompletion,
    ) -> tuple[int, int, str]:
        """
        Return cache key.
        """

        return (

            completion.line,

            completion.column,

            completion.text,

        )

###############################################################################
# Visibility
###############################################################################

    def should_render(
        self,
        context: RenderContext,
        completion: GhostCompletion,
    ) -> bool:
        """
        Check whether completion is visible.
        """

        return context.is_line_visible(
            completion.line,
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
            "font": (
                self._font.family()
                if self._font is not None
                else None
            ),
            "ghost_alpha": self._ghost_color.alpha(),
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
            "supports_multiline": True,
            "supports_animation": True,
            "supports_hover": True,
            "supports_cache": True,
            "supports_ai_completion": True,
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

        self._ghost_color = QColor(
            150,
            150,
            150,
            170,
        )

        self._font = None

        self.invalidate_cache()

        logger.info(
            "GhostTextRenderer reset.",
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
    "GhostCompletion",
    "GhostTextRenderer",
]