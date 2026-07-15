"""
==============================================================================
GEETA AI ENGINE

File        : editor_manager.py
Package     : ui
Description : Enterprise Editor Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QTabWidget

from config.logger import get_logger

from src.editor.code_editor import CodeEditor

logger = get_logger(__name__)


class EditorManager(QTabWidget):
    """
    Enterprise editor manager.

    Responsibilities
    ----------------
    • Multi-tab editor
    • Current editor management
    • File open/save
    • Tab lifecycle
    • Editor commands
    """

    currentEditorChanged = Signal(object)
    currentFileChanged = Signal(str)
    fileOpened = Signal(str)
    fileClosed = Signal(str)
    fileSaved = Signal(str)

    ###########################################################################

    def __init__(
        self,
        parent=None,
    ) -> None:

        super().__init__(parent)

        self.setTabsClosable(True)
        self.setMovable(True)
        self.setDocumentMode(True)

        self.tabCloseRequested.connect(
            self.close_tab,
        )

        self.currentChanged.connect(
            self._on_current_changed,
        )

        logger.info(
            "EditorManager initialized.",
        )

    ###########################################################################

    def current_editor(
        self,
    ) -> CodeEditor | None:
        """
        Return current editor.
        """

        widget = self.currentWidget()

        if isinstance(
            widget,
            CodeEditor,
        ):
            return widget

        return None

    ###########################################################################

    def new_file(
        self,
    ) -> CodeEditor:
        """
        Create a new file.
        """

        editor = CodeEditor()

        index = self.addTab(
            editor,
            "Untitled",
        )

        self.setCurrentIndex(index)

        return editor

    def _on_current_changed(
        self,
        index: int,
    ) -> None:
        editor = self.current_editor()

        self.currentEditorChanged.emit(editor)

        path = self.current_file_path()

        if path is None:
            path = ""

        self.currentFileChanged.emit(path)        
###############################################################################
# Open File
###############################################################################

    def open_file(
        self,
        file_path: str,
    ) -> CodeEditor:
        """
        Open a file in a new editor tab.
        """

        path = Path(file_path)

        editor = CodeEditor()

        if path.exists():

            editor.setPlainText(

                path.read_text(
                    encoding="utf-8",
                )

            )

        editor.file_path = str(path)

        index = self.addTab(

            editor,

            path.name,

        )

        self.setCurrentIndex(index)

        self.fileOpened.emit(
            str(path),
        )

        logger.info(
            "Opened file: %s",
            path,
        )

        return editor

###############################################################################
# Save File
###############################################################################

    def save_file(
        self,
    ) -> bool:
        """
        Save current editor.
        """

        editor = self.current_editor()

        if editor is None:

            return False

        file_path = getattr(
            editor,
            "file_path",
            None,
        )

        if not file_path:

            return False

        Path(file_path).write_text(

            editor.toPlainText(),

            encoding="utf-8",

        )

        self.fileSaved.emit(
            file_path,
        )

        logger.info(
            "Saved: %s",
            file_path,
        )

        return True

###############################################################################
# Save As
###############################################################################

    def save_file_as(
        self,
        file_path: str,
    ) -> bool:
        """
        Save current editor using a new filename.
        """

        editor = self.current_editor()

        if editor is None:

            return False

        Path(file_path).write_text(

            editor.toPlainText(),

            encoding="utf-8",

        )

        editor.file_path = file_path

        self.setTabText(

            self.currentIndex(),

            Path(file_path).name,

        )

        self.fileSaved.emit(
            file_path,
        )

        logger.info(
            "Saved As: %s",
            file_path,
        )

        return True

###############################################################################
# Reload File
###############################################################################

    def reload_file(
        self,
    ) -> bool:
        """
        Reload current file from disk.
        """

        editor = self.current_editor()

        if editor is None:

            return False

        file_path = getattr(
            editor,
            "file_path",
            None,
        )

        if not file_path:

            return False

        editor.setPlainText(

            Path(file_path).read_text(

                encoding="utf-8",

            )

        )

        logger.info(
            "Reloaded: %s",
            file_path,
        )

        return True

###############################################################################
# Close Tab
###############################################################################

    def close_tab(
        self,
        index: int,
    ) -> None:
        """
        Close a tab.
        """

        widget = self.widget(index)

        if widget is None:

            return

        file_path = getattr(
            widget,
            "file_path",
            "",
        )

        self.removeTab(index)

        widget.deleteLater()

        if file_path:

            self.fileClosed.emit(
                file_path,
            )

        logger.info(
            "Closed tab: %s",
            file_path,
        )

###############################################################################
# Close All Tabs
###############################################################################

    def close_all_tabs(
        self,
    ) -> None:
        """
        Close all editor tabs.
        """

        while self.count():

            self.close_tab(0)

        logger.info(
            "All tabs closed.",
        )
        ###############################################################################
# Undo
###############################################################################

    def undo(
        self,
    ) -> None:
        """
        Undo current editor.
        """

        editor = self.current_editor()

        if editor is not None:

            editor.undo()

###############################################################################
# Redo
###############################################################################

    def redo(
        self,
    ) -> None:
        """
        Redo current editor.
        """

        editor = self.current_editor()

        if editor is not None:

            editor.redo()

###############################################################################
# Cut
###############################################################################

    def cut(
        self,
    ) -> None:
        """
        Cut selected text.
        """

        editor = self.current_editor()

        if editor is not None:

            editor.cut()

###############################################################################
# Copy
###############################################################################

    def copy(
        self,
    ) -> None:
        """
        Copy selected text.
        """

        editor = self.current_editor()

        if editor is not None:

            editor.copy()

###############################################################################
# Paste
###############################################################################

    def paste(
        self,
    ) -> None:
        """
        Paste clipboard contents.
        """

        editor = self.current_editor()

        if editor is not None:

            editor.paste()

###############################################################################
# Select All
###############################################################################

    def select_all(
        self,
    ) -> None:
        """
        Select all text.
        """

        editor = self.current_editor()

        if editor is not None:

            editor.selectAll()

###############################################################################
# Find
###############################################################################

    def find(
        self,
    ) -> None:
        """
        Open Find dialog.

        Placeholder for Search Panel integration.
        """

        logger.info(
            "Find requested.",
        )

###############################################################################
# Replace
###############################################################################

    def replace(
        self,
    ) -> None:
        """
        Open Replace dialog.

        Placeholder for Replace Panel integration.
        """

        logger.info(
            "Replace requested.",
        )

###############################################################################
# Go To Line
###############################################################################

    def goto_line(
        self,
        line: int,
    ) -> None:
        """
        Move caret to specified line.
        """

        editor = self.current_editor()

        if editor is None:

            return

        if hasattr(
            editor,
            "goto_line",
        ):

            editor.goto_line(
                line,
            )

        logger.info(
            "Goto line: %d",
            line,
        )
        ###############################################################################
# Current File
###############################################################################

    def current_file_path(
        self,
    ) -> str | None:
        """
        Return current file path.
        """

        editor = self.current_editor()

        if editor is None:

            return None

        return getattr(
            editor,
            "file_path",
            None,
        )

###############################################################################
# Current File Name
###############################################################################

    def current_file_name(
        self,
    ) -> str:
        """
        Return current file name.
        """

        path = self.current_file_path()

        if not path:

            return "Untitled"

        return Path(path).name

###############################################################################
# Rename Tab
###############################################################################

    def rename_current_tab(
        self,
        title: str,
    ) -> None:
        """
        Rename current tab.
        """

        index = self.currentIndex()

        if index >= 0:

            self.setTabText(

                index,

                title,

            )

###############################################################################
# Dirty State
###############################################################################

    def set_modified(
        self,
        modified: bool,
    ) -> None:
        """
        Mark current tab modified.
        """

        index = self.currentIndex()

        if index < 0:

            return

        title = self.tabText(index)

        if modified:

            if not title.endswith("*"):

                self.setTabText(

                    index,

                    title + "*",

                )

        else:

            self.setTabText(

                index,

                title.rstrip("*"),

            )

###############################################################################
# Tab Navigation
###############################################################################

    def next_tab(
        self,
    ) -> None:
        """
        Switch to next tab.
        """

        if self.count() == 0:

            return

        self.setCurrentIndex(

            (self.currentIndex() + 1)

            % self.count()

        )

###############################################################################
# Previous Tab
###############################################################################

    def previous_tab(
        self,
    ) -> None:
        """
        Switch to previous tab.
        """

        if self.count() == 0:

            return

        self.setCurrentIndex(

            (self.currentIndex() - 1)

            % self.count()

        )

###############################################################################
# Activate Tab
###############################################################################

    def activate_tab(
        self,
        index: int,
    ) -> bool:
        """
        Activate a specific tab.
        """

        if 0 <= index < self.count():

            self.setCurrentIndex(index)

            return True

        return False

###############################################################################
# Find Editor
###############################################################################

    def editor_at(
        self,
        index: int,
    ) -> CodeEditor | None:
        """
        Return editor at index.
        """

        widget = self.widget(index)

        if isinstance(
            widget,
            CodeEditor,
        ):

            return widget

        return None

###############################################################################
# Editor Count
###############################################################################

    def editor_count(
        self,
    ) -> int:
        """
        Return number of open editors.
        """

        return self.count()
        ###############################################################################
# Save All
###############################################################################

    def save_all(
        self,
    ) -> None:
        """
        Save all open editors.
        """

        for index in range(self.count()):

            editor = self.editor_at(index)

            if editor is None:

                continue

            file_path = getattr(
                editor,
                "file_path",
                None,
            )

            if not file_path:

                continue

            Path(file_path).write_text(

                editor.toPlainText(),

                encoding="utf-8",

            )

            self.fileSaved.emit(
                file_path,
            )

        logger.info(
            "All editors saved.",
        )

###############################################################################
# Reload All
###############################################################################

    def reload_all(
        self,
    ) -> None:
        """
        Reload all editors from disk.
        """

        for index in range(self.count()):

            editor = self.editor_at(index)

            if editor is None:

                continue

            file_path = getattr(
                editor,
                "file_path",
                None,
            )

            if not file_path:

                continue

            editor.setPlainText(

                Path(file_path).read_text(

                    encoding="utf-8",

                )

            )

        logger.info(
            "All editors reloaded.",
        )

###############################################################################
# Close Others
###############################################################################

    def close_other_tabs(
        self,
    ) -> None:
        """
        Close every tab except current.
        """

        current = self.currentIndex()

        for index in reversed(range(self.count())):

            if index != current:

                self.close_tab(index)

###############################################################################
# Close Left
###############################################################################

    def close_tabs_left(
        self,
    ) -> None:
        """
        Close tabs on the left.
        """

        current = self.currentIndex()

        for index in reversed(range(current)):

            self.close_tab(index)

###############################################################################
# Close Right
###############################################################################

    def close_tabs_right(
        self,
    ) -> None:
        """
        Close tabs on the right.
        """

        current = self.currentIndex()

        for index in reversed(
            range(
                current + 1,
                self.count(),
            )
        ):

            self.close_tab(index)

###############################################################################
# Duplicate Prevention
###############################################################################

    def find_editor(
        self,
        file_path: str,
    ) -> CodeEditor | None:
        """
        Find already-open editor.
        """

        for index in range(self.count()):

            editor = self.editor_at(index)

            if editor is None:

                continue

            if getattr(
                editor,
                "file_path",
                "",
            ) == file_path:

                return editor

        return None

###############################################################################
# Iterate Editors
###############################################################################

    def editors(
        self,
    ):
        """
        Iterate over editors.
        """

        for index in range(self.count()):

            editor = self.editor_at(index)

            if editor is not None:

                yield editor

###############################################################################
# Workspace Sync
###############################################################################

    def synchronize_workspace(
        self,
    ) -> None:
        """
        Synchronize editor state with workspace.

        Placeholder for WorkspaceManager integration.
        """

        logger.info(
            "Workspace synchronized.",
        )
        ###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, object]:
        """
        Return editor manager statistics.
        """

        return {
            "open_editors": self.count(),
            "current_index": self.currentIndex(),
            "current_file": self.current_file_name(),
        }

###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return diagnostic information.
        """

        return {
            **self.statistics(),
            "tabs_closable": self.tabsClosable(),
            "tabs_movable": self.isMovable(),
            "document_mode": self.documentMode(),
        }

###############################################################################
# Reset
###############################################################################

    def reset(
        self,
    ) -> None:
        """
        Reset editor manager.
        """

        self.close_all_tabs()

        logger.info(
            "EditorManager reset.",
        )

###############################################################################
# File Exists
###############################################################################

    def is_file_open(
        self,
        file_path: str,
    ) -> bool:
        """
        Check whether a file is already open.
        """

        return self.find_editor(
            file_path,
        ) is not None

###############################################################################
# Open Or Activate
###############################################################################

    def open_or_activate(
        self,
        file_path: str,
    ) -> CodeEditor:
        """
        Open a file or activate its existing tab.
        """

        editor = self.find_editor(
            file_path,
        )

        if editor is not None:

            index = self.indexOf(
                editor,
            )

            if index >= 0:

                self.setCurrentIndex(
                    index,
                )

            return editor

        return self.open_file(
            file_path,
        )

###############################################################################
# Active Editors
###############################################################################

    @property
    def active_editors(
        self,
    ) -> list[CodeEditor]:
        """
        Return all active editors.
        """

        return list(
            self.editors(),
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
            f"editors={self.count()}, "
            f"current={self.currentIndex()})"
        )

###############################################################################
# Exports
###############################################################################

__all__ = [
    "EditorManager",
]