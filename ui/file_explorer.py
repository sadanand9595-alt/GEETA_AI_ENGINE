"""
GEETA AI ENGINE
File Explorer
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFileDialog,
    QFileSystemModel,
    QMenu,
    QTreeView,
    QVBoxLayout,
    QWidget,
)


class FileExplorer(QWidget):
    """
    Project File Explorer
    """

    file_open_requested = Signal(str)

    def __init__(
        self,
        root: str | None = None,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self.model = QFileSystemModel(self)
        self.model.setRootPath("")

        self.tree = QTreeView(self)
        self.tree.setModel(self.model)

        self.tree.setSortingEnabled(True)
        self.tree.setAnimated(True)
        self.tree.setHeaderHidden(False)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tree)

        self.tree.doubleClicked.connect(
            self._double_clicked
        )

        self.tree.setContextMenuPolicy(
            Qt.CustomContextMenu
        )

        self.tree.customContextMenuRequested.connect(
            self.show_context_menu
        )

        if root:
            self.set_root(root)

    ######################################################################

    def set_root(
        self,
        folder: str,
    ) -> None:

        folder = str(Path(folder).resolve())

        index = self.model.index(folder)

        self.tree.setRootIndex(index)

    ######################################################################

    def root_path(
        self,
    ) -> str:

        return self.model.rootPath()

    ######################################################################

    def open_folder(
        self,
    ) -> None:

        folder = QFileDialog.getExistingDirectory(
            self,
            "Open Folder",
            self.root_path(),
        )

        if folder:

            self.set_root(folder)

    ######################################################################

    def refresh(
        self,
    ) -> None:

        root = self.root_path()

        self.model.setRootPath("")

        self.set_root(root)

    ######################################################################

    def _double_clicked(
        self,
        index,
    ) -> None:

        path = self.model.filePath(index)

        if Path(path).is_file():

            self.file_open_requested.emit(path)

    ######################################################################

    def show_context_menu(
        self,
        position,
    ) -> None:

        menu = QMenu(self)

        refresh_action = QAction(
            "Refresh",
            self,
        )

        refresh_action.triggered.connect(
            self.refresh
        )

        open_folder_action = QAction(
            "Open Folder",
            self,
        )

        open_folder_action.triggered.connect(
            self.open_folder
        )

        menu.addAction(open_folder_action)
        menu.addSeparator()
        menu.addAction(refresh_action)

        menu.exec(
            self.tree.viewport().mapToGlobal(position)
        )

    ######################################################################

    def current_path(
        self,
    ) -> str | None:

        index = self.tree.currentIndex()

        if not index.isValid():

            return None

        return self.model.filePath(index)

    ######################################################################

    def selected_file(
        self,
    ) -> str | None:

        path = self.current_path()

        if path and Path(path).is_file():

            return path

        return None