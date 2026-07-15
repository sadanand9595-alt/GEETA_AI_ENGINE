"""
==============================================================================
GEETA AI ENGINE

File        : inline_completion_renderer.py
Package     : editor.paint
Description : Enterprise Inline Completion Renderer

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

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
# Provider
###############################################################################


class CompletionProvider(Enum):
    """
    AI completion provider.
    """

    OPENAI = "OpenAI"

    CLAUDE = "Claude"

    GEMINI = "Gemini"

    OLLAMA = "Ollama"

    CUSTOM = "Custom"

###############################################################################
# Completion Candidate
###############################################################################


@dataclass(slots=True)
class CompletionCandidate:
    """
    Represents one inline completion candidate.
    """

    provider: CompletionProvider

    text: str

    confidence: float

    multiline: bool = False

###############################################################################
# Renderer
###############################################################################


class InlineCompletionRenderer(RenderLayer):
    """
    Professional inline completion renderer.

    Features
    --------
    • Multiple candidates
    • Provider badges
    • Streaming
    • Navigation
    • Preview rendering
    """

    priority = 75

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._enabled = True

        self._font: QFont | None = None

        self._text_color = QColor(
            180,
            180,
            180,
        )

        self._badge_color = QColor(
            55,
            120,
            240,
        )

        logger.info(
            "InlineCompletionRenderer initialized.",
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
        Paint inline completion.
        """

        if not self._enabled:

            return

        completion = getattr(
            session,
            "inline_completion",
            None,
        )

        if completion is None:

            return

        painter.save()

        painter.setPen(
            self._text_color,
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
        completion: CompletionCandidate,
    ) -> None:
        """
        Paint inline completion.
        """

        cursor = context.cursor_position

        x = context.column_to_x(
            cursor.column,
        )

        y = (
            context.line_to_y(
                cursor.line,
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

        self.paint_provider_badge(

            painter,

            x,

            y,

            completion.provider,

        )

###############################################################################
# Provider Badge
###############################################################################

    def paint_provider_badge(
        self,
        painter: QPainter,
        x: float,
        y: float,
        provider: CompletionProvider,
    ) -> None:
        """
        Paint AI provider badge.
        """

        badge = provider.value

        width = max(
            42,
            len(badge) * 7,
        )

        painter.save()

        painter.setBrush(
            self._badge_color,
        )

        painter.setPen(
            self._badge_color,
        )

        painter.drawRoundedRect(

            x,

            y - 22,

            width,

            18,

            4,

            4,

        )

        painter.setPen(
            QColor(
                255,
                255,
                255,
            )
        )

        painter.drawText(

            x + 6,

            y - 8,

            badge,

        )

        painter.restore()

###############################################################################
# Candidate Navigation
###############################################################################

    def next_candidate(
        self,
        session: EditorSession,
    ) -> None:
        """
        Select next completion candidate.
        """

        manager = getattr(
            session,
            "completion_manager",
            None,
        )

        if manager is None:

            return

        manager.next_candidate()

    ###########################################################################

    def previous_candidate(
        self,
        session: EditorSession,
    ) -> None:
        """
        Select previous completion candidate.
        """

        manager = getattr(
            session,
            "completion_manager",
            None,
        )

        if manager is None:

            return

        manager.previous_candidate()

###############################################################################
# Streaming
###############################################################################

    def update_stream(
        self,
        session: EditorSession,
        chunk: str,
    ) -> None:
        """
        Append streamed completion text.
        """

        completion = getattr(
            session,
            "inline_completion",
            None,
        )

        if completion is None:

            return

        completion.text += chunk

###############################################################################
# Accept Preview
###############################################################################

    def accept_preview(
        self,
        session: EditorSession,
    ) -> None:
        """
        Reserved for preview acceptance.

        Future:
            Accept without document mutation.
        """

        return
        ###############################################################################
# Completion Toolbar
###############################################################################

    def paint_toolbar(
        self,
        painter: QPainter,
        context: RenderContext,
        completion: CompletionCandidate,
    ) -> None:
        """
        Paint inline completion toolbar.

        Example:
            [Tab Accept] [Alt+] Next [Alt+[ Previous]
        """

        cursor = context.cursor_position

        x = context.column_to_x(
            cursor.column,
        )

        y = (
            context.line_to_y(
                cursor.line,
            )
            - 26
        )

        toolbar_width = 180
        toolbar_height = 20

        painter.save()

        painter.setBrush(
            QColor(
                45,
                45,
                48,
            )
        )

        painter.setPen(
            QColor(
                90,
                90,
                90,
            )
        )

        painter.drawRoundedRect(

            x,

            y,

            toolbar_width,

            toolbar_height,

            4,

            4,

        )

        painter.setPen(
            QColor(
                220,
                220,
                220,
            )
        )

        painter.drawText(

            x + 8,

            y + 14,

            "Tab Accept   Alt+] Next   Alt+[ Prev",

        )

        painter.restore()

###############################################################################
# Acceptance
###############################################################################

    def accept_character(
        self,
        session: EditorSession,
    ) -> None:
        """
        Reserved for character acceptance.
        """

        manager = getattr(
            session,
            "completion_manager",
            None,
        )

        if manager is not None:

            manager.accept_character()

    ###########################################################################

    def accept_word(
        self,
        session: EditorSession,
    ) -> None:
        """
        Reserved for word acceptance.
        """

        manager = getattr(
            session,
            "completion_manager",
            None,
        )

        if manager is not None:

            manager.accept_word()

    ###########################################################################

    def accept_line(
        self,
        session: EditorSession,
    ) -> None:
        """
        Reserved for line acceptance.
        """

        manager = getattr(
            session,
            "completion_manager",
            None,
        )

        if manager is not None:

            manager.accept_line()

    ###########################################################################

    def accept_completion(
        self,
        session: EditorSession,
    ) -> None:
        """
        Accept the full completion.
        """

        manager = getattr(
            session,
            "completion_manager",
            None,
        )

        if manager is not None:

            manager.accept()

###############################################################################
# Theme
###############################################################################

    def update_theme(
        self,
        text_color: QColor,
        badge_color: QColor,
        font: QFont | None = None,
    ) -> None:
        """
        Update renderer theme.
        """

        self._text_color = text_color

        self._badge_color = badge_color

        if font is not None:

            self._font = font

###############################################################################
# Hover
###############################################################################

    def paint_hover(
        self,
        painter: QPainter,
        context: RenderContext,
        completion: CompletionCandidate,
    ) -> None:
        """
        Reserved for completion hover.

        Future:
            • Provider
            • Confidence
            • Latency
            • Token count
        """

        return

###############################################################################
# Cache
###############################################################################

    def invalidate_cache(
        self,
    ) -> None:
        """
        Invalidate inline completion cache.
        """

        logger.debug(
            "Inline completion cache invalidated.",
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
            "text_color": (
                self._text_color.red(),
                self._text_color.green(),
                self._text_color.blue(),
                self._text_color.alpha(),
            ),
            "badge_color": (
                self._badge_color.red(),
                self._badge_color.green(),
                self._badge_color.blue(),
                self._badge_color.alpha(),
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
            "supports_streaming": True,
            "supports_navigation": True,
            "supports_provider_badges": True,
            "supports_toolbar": True,
            "supports_acceptance": True,
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

        self._font = None

        self._text_color = QColor(
            180,
            180,
            180,
        )

        self._badge_color = QColor(
            55,
            120,
            240,
        )

        self.invalidate_cache()

        logger.info(
            "InlineCompletionRenderer reset.",
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
    "CompletionProvider",
    "CompletionCandidate",
    "InlineCompletionRenderer",
]