"""
GEETA AI Engine

VS Code-style editor widget.
"""

from __future__ import annotations

import codecs
from pathlib import Path

from PySide6.QtCore import QSignalBlocker, Signal
from PySide6.QtGui import QColor, QFont, QPalette, QTextFormat
from PySide6.QtWidgets import QFileDialog, QPlainTextEdit, QTextEdit, QWidget

from config.logger import get_logger

logger = get_logger(__name__)


class CodeEditor(QPlainTextEdit):
    """A file-backed, extensible text editor for the GEETA desktop IDE.

    The widget intentionally owns only document editing responsibilities. Visual
    collaborators such as line numbers, syntax highlighting, diagnostics,
    minimaps, AI completion, and LSP integrations can attach to its Qt document
    and signals without coupling this class to those services.
    """

    fileOpened = Signal(str)
    fileSaved = Signal(str)
    filePathChanged = Signal(str)
    modificationStateChanged = Signal(bool)
    zoomChanged = Signal(int)

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        encoding: str = "utf-8",
    ) -> None:
        super().__init__(parent)

        codecs.lookup(encoding)
        self._encoding = encoding
        self._file_path: Path | None = None
        self._dirty = False
        self._zoom_level = 0
        self._base_font = QFont("Consolas", 11)
        self._highlight_current_line = True

        self._configure_editor()
        self.document().modificationChanged.connect(self._on_document_modified)
        self.cursorPositionChanged.connect(self._update_current_line_highlight)
        self._update_current_line_highlight()

    @property
    def file_path(self) -> str | None:
        """Return the absolute path of the open file, if one exists."""
        return str(self._file_path) if self._file_path is not None else None

    @property
    def encoding(self) -> str:
        """Return the encoding used for file input and output."""
        return self._encoding

    @property
    def zoom_level(self) -> int:
        """Return the current zoom offset from the configured base font."""
        return self._zoom_level

    def filename(self) -> str:
        """Return a user-facing name for the current document."""
        return self._file_path.name if self._file_path is not None else "Untitled"

    def is_modified(self) -> bool:
        """Return whether the editor contains unsaved changes."""
        return self._dirty

    def open_file(self, file_path: str | Path) -> bool:
        """Open a UTF-8 text file without altering the editor on failure."""
        path = Path(file_path).expanduser().resolve()

        if not path.is_file():
            logger.warning("Unable to open non-file path: %s", path)
            return False

        try:
            content = path.read_text(encoding=self._encoding)
        except (OSError, UnicodeError):
            logger.exception("Unable to open file: %s", path)
            return False

        with QSignalBlocker(self.document()):
            self.setPlainText(content)
            self.document().setModified(False)

        self._file_path = path
        self._set_dirty_state(False)
        self.filePathChanged.emit(str(path))
        self.fileOpened.emit(str(path))
        self._update_current_line_highlight()
        logger.info("Opened editor document: %s", path)
        return True

    def load_file(self, file_path: str | Path) -> bool:
        """Compatibility alias for :meth:`open_file`."""
        return self.open_file(file_path)

    def save_file(self) -> bool:
        """Save the document to its current path.

        Untitled documents invoke the Save As workflow. Read-only documents are
        never written in place.
        """
        if self.isReadOnly():
            logger.warning("Refused to save read-only document: %s", self.file_path)
            return False

        if self._file_path is None:
            return self.save_as()

        return self._write_file(self._file_path)

    def save(self) -> bool:
        """Compatibility alias for :meth:`save_file`."""
        return self.save_file()

    def save_as(self, file_path: str | Path | None = None) -> bool:
        """Save the document under a new path, prompting when no path is given."""
        target = self._select_save_path() if file_path is None else Path(file_path)
        if target is None:
            return False

        target = target.expanduser().resolve()
        if not self._write_file(target):
            return False

        path_changed = target != self._file_path
        self._file_path = target
        if path_changed:
            self.filePathChanged.emit(str(target))
        return True

    def set_read_only(self, enabled: bool) -> None:
        """Set whether the document may be edited or saved in place."""
        self.setReadOnly(enabled)
        logger.info("Editor read-only mode set to %s for %s", enabled, self.filename())

    def set_line_wrap_enabled(self, enabled: bool) -> None:
        """Enable or disable visual line wrapping."""
        mode = (
            QPlainTextEdit.LineWrapMode.WidgetWidth
            if enabled
            else QPlainTextEdit.LineWrapMode.NoWrap
        )
        self.setLineWrapMode(mode)

    def is_line_wrap_enabled(self) -> bool:
        """Return whether visual line wrapping is enabled."""
        return self.lineWrapMode() != QPlainTextEdit.LineWrapMode.NoWrap

    def toggle_line_wrap(self) -> bool:
        """Toggle visual line wrapping and return its resulting state."""
        enabled = not self.is_line_wrap_enabled()
        self.set_line_wrap_enabled(enabled)
        return enabled

    def zoom_in(self) -> None:
        """Increase the editor font size by one zoom step."""
        self.zoomIn(1)
        self._set_zoom_level(self._zoom_level + 1)

    def zoom_out(self) -> None:
        """Decrease the editor font size by one zoom step."""
        self.zoomOut(1)
        self._set_zoom_level(self._zoom_level - 1)

    def reset_zoom(self) -> None:
        """Restore the configured editor font and zero zoom offset."""
        self.setFont(QFont(self._base_font))
        self._set_zoom_level(0)

    def set_current_line_highlight_enabled(self, enabled: bool) -> None:
        """Enable or disable the current-line visual indicator."""
        self._highlight_current_line = enabled
        self._update_current_line_highlight()

    def _configure_editor(self) -> None:
        self._base_font.setFixedPitch(True)
        self.setFont(QFont(self._base_font))
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(" ") * 4)
        self.setUndoRedoEnabled(True)

    def _write_file(self, path: Path) -> bool:
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(self.toPlainText(), encoding=self._encoding)
        except (OSError, UnicodeError):
            logger.exception("Unable to save file: %s", path)
            return False

        self.document().setModified(False)
        self._set_dirty_state(False)
        self.fileSaved.emit(str(path))
        logger.info("Saved editor document: %s", path)
        return True

    def _select_save_path(self) -> Path | None:
        initial_path = str(self._file_path) if self._file_path is not None else ""
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", initial_path)
        return Path(filename) if filename else None

    def _on_document_modified(self, modified: bool) -> None:
        self._set_dirty_state(modified)

    def _set_dirty_state(self, dirty: bool) -> None:
        if self._dirty == dirty:
            return
        self._dirty = dirty
        self.modificationStateChanged.emit(dirty)

    def _set_zoom_level(self, zoom_level: int) -> None:
        if self._zoom_level == zoom_level:
            return
        self._zoom_level = zoom_level
        self.zoomChanged.emit(zoom_level)

    def _update_current_line_highlight(self) -> None:
        if not self._highlight_current_line:
            self.setExtraSelections([])
            return

        selection = QTextEdit.ExtraSelection()
        color = self.palette().color(QPalette.ColorRole.AlternateBase)
        selection.format.setBackground(QColor(color).lighter(108))
        selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()
        self.setExtraSelections([selection])

__all__ = ["CodeEditor"]
