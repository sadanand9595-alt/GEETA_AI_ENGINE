"""
==============================================================================
GEETA AI ENGINE

File        : editor_widget.py
Package     : editor.widget
Description : Professional Editor Widget

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QColor,
    QFont,
    QFontMetricsF,
    QPainter,
    QPaintEvent,
)
from PySide6.QtWidgets import (
    QAbstractScrollArea,
    QWidget,
)

from editor.core.editor_session import EditorSession
from editor.render.layout_engine import LayoutEngine
from editor.render.render_cache import RenderCache
from editor.render.render_context import RenderContext
from editor.render.renderer import Renderer
from editor.render.viewport import Viewport

logger = logging.getLogger(__name__)


class EditorWidget(QAbstractScrollArea):
    """
    Professional custom editor widget.

    Features
    --------
    • Custom rendering
    • Custom scrolling
    • AI ready
    • Large file support
    • VS Code style architecture
    """

    #######################################################################

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        ###################################################################
        # Editor Core
        ###################################################################

        self.session = EditorSession()

        self.viewport_manager = Viewport()

        self.renderer = Renderer()

        self.layout_engine = LayoutEngine(
            QFont(
                "JetBrains Mono",
                11,
            )
        )

        self.render_cache = RenderCache()

        ###################################################################
        # Font
        ###################################################################

        self.setFont(
            self.layout_engine.font,
        )

        self._metrics = QFontMetricsF(
            self.font(),
        )

        ###################################################################
        # Scrollbars
        ###################################################################

        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded,
        )

        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAsNeeded,
        )

        ###################################################################
        # Widget
        ###################################################################

        self.setFocusPolicy(
            Qt.StrongFocus,
        )

        self.setMouseTracking(
            True,
        )

        logger.info(
            "Editor Widget initialized.",
        )
        ###############################################################################
# Paint Event
###############################################################################

    def paintEvent(
        self,
        event: QPaintEvent,
    ) -> None:
        """
        Paint the editor.
        """

        painter = QPainter(
            self.viewport(),
        )

        painter.fillRect(
            event.rect(),
            QColor(30, 30, 30),
        )

        context = self._create_render_context()

        self.renderer.paint(
            painter,
            context,
            self.session,
        )

###############################################################################
# Render Context
###############################################################################

    def _create_render_context(
        self,
    ) -> RenderContext:
        """
        Build the RenderContext for the current paint pass.
        """

        rect = self.viewport().rect()

        return RenderContext(

            viewport=rect,

            scroll_x=self.viewport_manager.scroll_x,

            scroll_y=self.viewport_manager.scroll_y,

            first_visible_line=(
                self.viewport_manager.first_visible_line
            ),

            last_visible_line=(
                self.viewport_manager.last_visible_line
            ),

            line_height=self.layout_engine.line_height(),

            character_width=(
                self.layout_engine.character_width()
            ),

            font_metrics=self.layout_engine.metrics,

            background_color=QColor(
                30,
                30,
                30,
            ),

            foreground_color=QColor(
                220,
                220,
                220,
            ),

            selection_color=QColor(
                38,
                79,
                120,
            ),

            caret_color=QColor(
                255,
                255,
                255,
            ),

            current_line_color=QColor(
                45,
                45,
                45,
            ),

            show_line_numbers=True,

            show_whitespace=False,

            show_current_line=True,

            show_diagnostics=True,

            show_minimap=False,
        )

###############################################################################
# Resize
###############################################################################

    def resizeEvent(
        self,
        event,
    ) -> None:
        """
        Handle viewport resize.
        """

        super().resizeEvent(
            event,
        )

        self.viewport_manager.resize(

            self.viewport().width(),

            self.viewport().height(),

        )

        self.viewport_manager.set_metrics(

            self.layout_engine.line_height(),

            self.layout_engine.character_width(),

        )
        ###############################################################################
# Keyboard Events
###############################################################################

    def keyPressEvent(
        self,
        event,
    ) -> None:
        """
        Handle keyboard input.
        """

        key = event.key()

        modifiers = event.modifiers()

        ###############################################################
        # Cursor Movement
        ###############################################################

        if key == Qt.Key_Left:

            self.session.cursor.move_left()

            self.viewport().update()

            return

        if key == Qt.Key_Right:

            self.session.cursor.move_right()

            self.viewport().update()

            return

        if key == Qt.Key_Up:

            self.session.cursor.move_up()

            self.viewport().update()

            return

        if key == Qt.Key_Down:

            self.session.cursor.move_down()

            self.viewport().update()

            return

        ###############################################################
        # Save
        ###############################################################

        if (
            modifiers & Qt.ControlModifier
            and key == Qt.Key_S
        ):

            self.session.save()

            return

        ###############################################################
        # Undo
        ###############################################################

        if (
            modifiers & Qt.ControlModifier
            and key == Qt.Key_Z
        ):

            self.session.undo_engine.undo()

            self.viewport().update()

            return

        ###############################################################
        # Redo
        ###############################################################

        if (
            modifiers & Qt.ControlModifier
            and key == Qt.Key_Y
        ):

            self.session.undo_engine.redo()

            self.viewport().update()

            return

        ###############################################################
        # Default
        ###############################################################

        super().keyPressEvent(
            event,
        )

###############################################################################
# Mouse Events
###############################################################################

    def mousePressEvent(
        self,
        event,
    ) -> None:
        """
        Handle mouse press.
        """

        self.setFocus()

        line = self.viewport_manager.y_to_line(
            event.position().y(),
        )

        logger.debug(
            "Mouse clicked on line %d",
            line,
        )

        super().mousePressEvent(
            event,
        )

###############################################################################
# Mouse Move
###############################################################################

    def mouseMoveEvent(
        self,
        event,
    ) -> None:
        """
        Handle mouse movement.
        """

        super().mouseMoveEvent(
            event,
        )

###############################################################################
# Wheel
###############################################################################

    def wheelEvent(
        self,
        event,
    ) -> None:
        """
        Handle mouse wheel scrolling.
        """

        delta = event.angleDelta().y()

        self.viewport_manager.scroll_by(
            0,
            -delta,
        )

        self.viewport().update()

###############################################################################
# Focus
###############################################################################

    def focusInEvent(
        self,
        event,
    ) -> None:
        """
        Handle focus gained.
        """

        logger.debug(
            "Editor focused.",
        )

        super().focusInEvent(
            event,
        )

    ###########################################################################

    def focusOutEvent(
        self,
        event,
    ) -> None:
        """
        Handle focus lost.
        """

        logger.debug(
            "Editor lost focus.",
        )

        super().focusOutEvent(
            event,
        )
        ###############################################################################
# File Operations
###############################################################################

    def open_file(
        self,
        filename: str,
    ) -> None:
        """
        Open a file into the current editor session.
        """

        self.session.open(
            filename,
        )

        self.viewport_manager.set_document_lines(
            self.session.text_buffer.line_count(),
        )

        self.update_scrollbars()

        self.viewport().update()

    ###########################################################################

    def save_file(
        self,
    ) -> None:
        """
        Save the current document.
        """

        self.session.save()

###############################################################################
# Scrollbars
###############################################################################

    def update_scrollbars(
        self,
    ) -> None:
        """
        Synchronize Qt scrollbars with the viewport state.
        """

        vertical = self.verticalScrollBar()

        vertical.setMinimum(0)

        maximum = max(
            0,
            int(
                self.session.text_buffer.line_count()
                * self.layout_engine.line_height()
                - self.viewport().height()
            ),
        )

        vertical.setMaximum(
            maximum,
        )

        vertical.setPageStep(
            self.viewport().height(),
        )

        vertical.setValue(
            self.viewport_manager.scroll_y,
        )

###############################################################################
# Refresh
###############################################################################

    def refresh(
        self,
    ) -> None:
        """
        Refresh the editor.
        """

        self.viewport_manager.set_document_lines(
            self.session.text_buffer.line_count(),
        )

        self.update_scrollbars()

        self.viewport().update()

###############################################################################
# Scrollbar Events
###############################################################################

    def scrollContentsBy(
        self,
        dx: int,
        dy: int,
    ) -> None:
        """
        Handle scrollbar movement.
        """

        super().scrollContentsBy(
            dx,
            dy,
        )

        self.viewport_manager.set_scroll(

            self.horizontalScrollBar().value(),

            self.verticalScrollBar().value(),

        )

        self.viewport().update()

###############################################################################
# Session
###############################################################################

    def session_statistics(
        self,
    ) -> dict[str, object]:
        """
        Return session statistics.
        """

        return self.session.statistics()

    ###########################################################################

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return editor diagnostics.
        """

        return {
            "session": self.session.diagnostics(),
            "viewport": self.viewport_manager.diagnostics(),
            "renderer": self.renderer.diagnostics(),
            "layout": self.layout_engine.diagnostics(),
            "cache": self.render_cache.diagnostics(),
        }
        ###############################################################################
# Widget Lifecycle
###############################################################################

    def clear(
        self,
    ) -> None:
        """
        Clear the current editor session.
        """

        self.session.reset()

        self.viewport_manager.reset()

        self.render_cache.reset()

        self.refresh()

        logger.info(
            "Editor cleared.",
        )

###############################################################################

    def closeEvent(
        self,
        event,
    ) -> None:
        """
        Handle widget close.
        """

        try:

            self.session.close()

            self.session.dispose()

            self.render_cache.reset()

            self.viewport_manager.reset()

            self.layout_engine.reset()

            logger.info(
                "Editor widget closed.",
            )

        except Exception:

            logger.exception(
                "Error while closing editor widget.",
            )

        event.accept()

###############################################################################
# Utility
###############################################################################

    def update_theme(
        self,
        font: QFont,
    ) -> None:
        """
        Update editor font/theme.
        """

        self.setFont(
            font,
        )

        self.layout_engine = LayoutEngine(
            font,
        )

        self._metrics = QFontMetricsF(
            font,
        )

        self.refresh()

###############################################################################

    def repaint_editor(
        self,
    ) -> None:
        """
        Force a complete repaint.
        """

        self.viewport().update()

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
            f"lines={self.session.text_buffer.line_count()}, "
            f"scroll={self.viewport_manager.scroll_y})"
        )

###############################################################################
# Exports
###############################################################################

__all__ = [
    "EditorWidget",
]