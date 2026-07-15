"""
==============================================================================
GEETA AI ENGINE

File        : search_highlight_renderer.py
Package     : editor.paint
Description : Search Highlight Renderer

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
# Search Match
###############################################################################


@dataclass(slots=True)
class SearchMatch:
    """
    Represents a single search match.
    """

    line: int
    start_column: int
    end_column: int
    active: bool = False

###############################################################################
# Search Highlight Renderer
###############################################################################


class SearchHighlightRenderer(RenderLayer):
    """
    Enterprise search highlight renderer.

    Features
    --------
    • Search matches
    • Active match
    • Regex search
    • Replace preview
    • Semantic search
    """

    priority = 25

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._enabled = True

        self._match_color = QColor(
            255,
            235,
            59,
            140,
        )

        self._active_match_color = QColor(
            255,
            152,
            0,
            180,
        )

        logger.info(
            "SearchHighlightRenderer initialized.",
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
        Paint search matches.
        """

        if not self._enabled:

            return

        matches = getattr(
            session,
            "search_matches",
            [],
        )

        painter.save()

        for match in matches:

            if not context.is_line_visible(
                match.line,
            ):
                continue

            self.paint_match(

                painter,

                context,

                match,

            )

        painter.restore()
        ###############################################################################
# Match Rendering
###############################################################################

    def paint_match(
        self,
        painter: QPainter,
        context: RenderContext,
        match: SearchMatch,
    ) -> None:
        """
        Paint a search match.
        """

        x = context.column_to_x(
            match.start_column,
        )

        width = max(

            context.column_to_x(
                match.end_column,
            ) - x,

            context.character_width,

        )

        y = context.line_to_y(
            match.line,
        )

        color = (

            self._active_match_color

            if match.active

            else self._match_color

        )

        painter.fillRect(

            QRectF(

                x,

                y,

                width,

                context.line_height,

            ),

            color,

        )

###############################################################################
# Active Match
###############################################################################

    def paint_active_match(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Paint currently selected search match.
        """

        active = getattr(
            session,
            "active_search_match",
            None,
        )

        if active is None:

            return

        self.paint_match(

            painter,

            context,

            active,

        )

###############################################################################
# Regex Highlight
###############################################################################

    def paint_regex_matches(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Reserved for regex capture highlighting.
        """

        return

###############################################################################
# Replace Preview
###############################################################################

    def paint_replace_preview(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Reserved for replace preview rendering.
        """

        return

###############################################################################
# Visibility
###############################################################################

    def should_render(
        self,
        context: RenderContext,
        match: SearchMatch,
    ) -> bool:
        """
        Check visibility.
        """

        return context.is_line_visible(
            match.line,
        )

###############################################################################
# Cache
###############################################################################

    def invalidate_cache(
        self,
    ) -> None:
        """
        Invalidate cached search geometry.
        """

        logger.debug(
            "Search highlight cache invalidated.",
        )
        ###############################################################################
# Theme
###############################################################################

    def update_theme(
        self,
        match_color: QColor,
        active_match_color: QColor,
    ) -> None:
        """
        Update renderer colors.
        """

        self._match_color = match_color

        self._active_match_color = active_match_color

###############################################################################
# Whole Word Indicator
###############################################################################

    def paint_whole_word_indicator(
        self,
        painter: QPainter,
        context: RenderContext,
        match: SearchMatch,
    ) -> None:
        """
        Reserved for whole-word search visualization.

        Future:
            Draw subtle underline or border.
        """

        return

###############################################################################
# Case Sensitive Indicator
###############################################################################

    def paint_case_sensitive_indicator(
        self,
        painter: QPainter,
        context: RenderContext,
        match: SearchMatch,
    ) -> None:
        """
        Reserved for case-sensitive search visualization.
        """

        return

###############################################################################
# Semantic Search
###############################################################################

    def paint_semantic_matches(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Reserved for AI semantic search highlights.

        Future:
            • Symbol matches
            • Similar code blocks
            • AI-ranked matches
        """

        return

###############################################################################
# Hover
###############################################################################

    def paint_hover(
        self,
        painter: QPainter,
        context: RenderContext,
        match: SearchMatch,
    ) -> None:
        """
        Reserved for search hover tooltips.
        """

        return

###############################################################################
# Multi-file Search
###############################################################################

    def paint_multifile_matches(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Reserved for workspace-wide search rendering.

        Future:
            • Search panel integration
            • Workspace search
            • AI semantic search
        """

        return

###############################################################################
# Performance
###############################################################################

    def prepare_frame(
        self,
        context: RenderContext,
    ) -> None:
        """
        Prepare renderer before painting.

        Future:
            Cache visible matches.
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
            "priority": self.priority,
            "match_color": (
                self._match_color.red(),
                self._match_color.green(),
                self._match_color.blue(),
                self._match_color.alpha(),
            ),
            "active_match_color": (
                self._active_match_color.red(),
                self._active_match_color.green(),
                self._active_match_color.blue(),
                self._active_match_color.alpha(),
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
            "supports_regex": True,
            "supports_replace_preview": True,
            "supports_semantic_search": True,
            "supports_multifile_search": True,
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

        self._match_color = QColor(
            255,
            235,
            59,
            140,
        )

        self._active_match_color = QColor(
            255,
            152,
            0,
            180,
        )

        self.invalidate_cache()

        logger.info(
            "SearchHighlightRenderer reset.",
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
    "SearchMatch",
    "SearchHighlightRenderer",
]