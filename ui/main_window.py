"""
GEETA AI ENGINE
Main Window
"""

from __future__ import annotations
from ui.editor_manager import EditorManager
from ui.menu_bar import MenuBarManager
from ui.tool_bar import ToolBarManager
from ui.terminal_panel import TerminalPanel
from ui.file_explorer import FileExplorer
import logging

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDockWidget,
    QLabel,
    QMainWindow,
    QStatusBar,
    QTextEdit,
)



logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Main Application Window
    """

    def __init__(
        self,
        database,
        providers,
        plugins,
        worker,
        vscode,
        command_palette,
        chat_panel,
        inline_ai,
    ) -> None:

        super().__init__()

        self.database = database
        self.providers = providers
        self.plugins = plugins
        self.worker = worker
        self.vscode = vscode

        self.command_palette = command_palette
        self.chat_panel = chat_panel
        self.inline_ai = inline_ai

        self.editor_manager: EditorManager | None = None
        self.file_explorer: FileExplorer | None = None

        self.status_label: QLabel | None = None

        self.initialize_ui()

    ####################################################################

    def initialize_ui(
        self,
    ) -> None:

        self.setWindowTitle(
            "GEETA AI ENGINE v3.0"
        )

        self.resize(
            1700,
            1000,
        )

        self.create_editor()

        self.create_file_explorer()

        self.create_ai_chat()

        self.create_terminal()

        self.create_statusbar()

        MenuBarManager(self)

        ToolBarManager(self)

        logger.info(
            "Main Window initialized."
        )
        ####################################################################
    # Editor
    ####################################################################

    def create_editor(
        self,
    ) -> None:

        self.editor_manager = EditorManager()

        self.setCentralWidget(
            self.editor_manager,
        )

    ####################################################################
    # File Explorer
    ####################################################################

    def create_file_explorer(
        self,
    ) -> None:

        self.file_explorer = FileExplorer(".")

        self.file_explorer.file_open_requested.connect(
            self.editor_manager.open_file,
        )

        dock = QDockWidget(
            "Explorer",
            self,
        )

        dock.setObjectName(
            "ExplorerDock",
        )

        dock.setWidget(
            self.file_explorer,
        )

        dock.setAllowedAreas(
            Qt.LeftDockWidgetArea,
        )

        self.addDockWidget(
            Qt.LeftDockWidgetArea,
            dock,
        )

    ####################################################################
    # AI Chat
    ####################################################################

    def create_ai_chat(
        self,
    ) -> None:

        dock = QDockWidget(
            "AI Chat",
            self,
        )

        dock.setObjectName(
            "AIChatDock",
        )

        chat = QTextEdit(self)

        chat.setReadOnly(True)

        chat.setPlaceholderText(
            "GEETA AI Assistant"
        )

        dock.setWidget(
            chat,
        )

        dock.setAllowedAreas(
            Qt.RightDockWidgetArea,
        )

        self.addDockWidget(
            Qt.RightDockWidgetArea,
            dock,
        )

   ####################################################################
    # Terminal
    ####################################################################

    def create_terminal(
        self,
    ) -> None:

        self.terminal = TerminalPanel()

        dock = QDockWidget(
            "Terminal",
            self,
        )

        dock.setObjectName(
            "TerminalDock",
        )

        dock.setWidget(
            self.terminal,
        )

        dock.setAllowedAreas(
            Qt.BottomDockWidgetArea,
        )

        self.addDockWidget(
            Qt.BottomDockWidgetArea,
            dock,
        )
    ####################################################################
    # Status Bar
    ####################################################################

    def create_statusbar(
        self,
    ) -> None:

        statusbar = QStatusBar(self)

        self.setStatusBar(
            statusbar,
        )

        self.status_label = QLabel(
            "GEETA AI ENGINE Ready",
            self,
        )

        statusbar.addPermanentWidget(
            self.status_label,
        )

        if self.editor_manager is not None:

            self.editor_manager.currentFileChanged.connect(
                self.on_current_file_changed,
            )

    ####################################################################
    # Status Updates
    ####################################################################

    def on_current_file_changed(
        self,
        filename: str,
    ) -> None:

        if self.status_label is not None:

            self.status_label.setText(
                filename,
            )

    ####################################################################
    # Close Event
    ####################################################################

    def closeEvent(
        self,
        event,
    ) -> None:

        logger.info(
            "Closing GEETA AI ENGINE...",
        )

        try:

            if self.editor_manager is not None:

                self.editor_manager.save_all()

        except Exception:

            logger.exception(
                "Error while saving editors.",
            )

        event.accept()