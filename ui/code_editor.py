"""
GEETA AI ENGINE
Professional Code Editor
"""

from __future__ import annotations

import logging
from pathlib import Path

from PySide6.QtCore import QFileInfo, Signal
from PySide6.QtGui import (
    QAction,
    QFont,
    QKeySequence,
    QTextCursor,
)
from PySide6.QtWidgets import (
    QFileDialog,
    QPlainTextEdit,
    QWidget,
)

logger = logging.getLogger(__name__)


class CodeEditor(QPlainTextEdit):
    """
    Professional Code Editor
    """

    fileOpened = Signal(str)
    fileSaved = Signal(str)
    modificationStateChanged = Signal(bool)

    #######################################################################

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self._file_path: str | None = None

        self._modified = False

        self.setup_editor()

        self.document().modificationChanged.connect(
            self._document_modified,
        )

    #######################################################################

    def setup_editor(
        self,
    ) -> None:

        font = QFont(
            "Consolas",
            11,
        )

        font.setFixedPitch(True)

        self.setFont(font)

        self.setTabStopDistance(40)

        self.setLineWrapMode(
            QPlainTextEdit.NoWrap,
        )

        save_action = QAction(
            self,
        )

        save_action.setShortcut(
            QKeySequence.Save,
        )

        save_action.triggered.connect(
            self.save,
        )

        self.addAction(
            save_action,
        )

    #######################################################################

    @property
    def file_path(
        self,
    ) -> str | None:

        return self._file_path

    #######################################################################

    def load_file(
        self,
        path: str,
    ) -> bool:

        try:

            text = Path(path).read_text(
                encoding="utf-8",
            )

            self.setPlainText(
                text,
            )

            self.document().setModified(
                False,
            )

            self._file_path = path

            self.fileOpened.emit(
                path,
            )

            logger.info(
                "Opened %s",
                path,
            )

            return True

        except Exception:

            logger.exception(
                "Cannot open file.",
            )

            return False

    #######################################################################

    def save(
        self,
    ) -> bool:

        if not self._file_path:

            return self.save_as()

        try:

            Path(
                self._file_path,
            ).write_text(

                self.toPlainText(),

                encoding="utf-8",
            )

            self.document().setModified(
                False,
            )

            self.fileSaved.emit(
                self._file_path,
            )

            logger.info(
                "Saved %s",
                self._file_path,
            )

            return True

        except Exception:

            logger.exception(
                "Save failed.",
            )

            return False

    #######################################################################

    def save_as(
        self,
    ) -> bool:

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            self._file_path or "",
        )

        if not filename:

            return False

        self._file_path = filename

        return self.save()

    #######################################################################

    def goto_line(
        self,
        line: int,
    ) -> None:

        cursor = QTextCursor(
            self.document(),
        )

        cursor.movePosition(
            QTextCursor.Start,
        )

        cursor.movePosition(
            QTextCursor.Down,
            QTextCursor.MoveAnchor,
            max(0, line - 1),
        )

        self.setTextCursor(
            cursor,
        )

        self.centerCursor()

    #######################################################################

    def filename(
        self,
    ) -> str:

        if not self._file_path:

            return "Untitled"

        return QFileInfo(
            self._file_path,
        ).fileName()

    #######################################################################

    def is_modified(
        self,
    ) -> bool:

        return self.document().isModified()

    #######################################################################

    def zoom_in(
        self,
    ) -> None:

        self.zoomIn(1)

    #######################################################################

    def zoom_out(
        self,
    ) -> None:

        self.zoomOut(1)

    #######################################################################

    def _document_modified(
        self,
        modified: bool,
    ) -> None:

        self._modified = modified

        self.modificationStateChanged.emit(
            modified,
        )