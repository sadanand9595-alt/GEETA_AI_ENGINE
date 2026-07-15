"""
GEETA AI ENGINE
Professional Menu Bar
"""

from __future__ import annotations

import logging

from PySide6.QtGui import (
    QAction,
    QKeySequence,
)

from PySide6.QtWidgets import (
    QMainWindow,
    QMenu,
)

logger = logging.getLogger(__name__)


class MenuBarManager:
    """
    Professional IDE Menu Bar.
    """

    ##################################################################

    def __init__(
        self,
        window: QMainWindow,
    ) -> None:

        self.window = window

        self.menu_bar = window.menuBar()

        self.build()

    ##################################################################

    def build(
        self,
    ) -> None:

        self.create_file_menu()

        self.create_edit_menu()
        ##################################################################
    # FILE MENU
    ##################################################################

    def create_file_menu(
        self,
    ) -> None:

        menu = self.menu_bar.addMenu("&File")

        self._action(
            menu,
            "New File",
            QKeySequence.New,
        )

        self._action(
            menu,
            "Open File",
            QKeySequence.Open,
        )

        self._action(
            menu,
            "Open Folder",
        )

        menu.addSeparator()

        self._action(
            menu,
            "Save",
            QKeySequence.Save,
        )

        self._action(
            menu,
            "Save As",
            QKeySequence.SaveAs,
        )

        self._action(
            menu,
            "Save All",
        )

        menu.addSeparator()

        exit_action = self._action(
            menu,
            "Exit",
        )

        exit_action.triggered.connect(
            self.window.close,
        )
        ##################################################################
    # EDIT MENU
    ##################################################################

    def create_edit_menu(
        self,
    ) -> None:

        menu = self.menu_bar.addMenu("&Edit")

        self._action(
            menu,
            "Undo",
            QKeySequence.Undo,
        )

        self._action(
            menu,
            "Redo",
            QKeySequence.Redo,
        )

        menu.addSeparator()

        self._action(
            menu,
            "Cut",
            QKeySequence.Cut,
        )

        self._action(
            menu,
            "Copy",
            QKeySequence.Copy,
        )

        self._action(
            menu,
            "Paste",
            QKeySequence.Paste,
        )

        menu.addSeparator()

        self._action(
            menu,
            "Find",
            QKeySequence.Find,
        )

        self._action(
            menu,
            "Replace",
        )
        ##################################################################
    # VIEW MENU
    ##################################################################

    def create_view_menu(
        self,
    ) -> None:

        menu = self.menu_bar.addMenu("&View")

        self._action(
            menu,
            "Explorer",
        )

        self._action(
            menu,
            "AI Chat",
        )

        self._action(
            menu,
            "Terminal",
        )

        menu.addSeparator()

        self._action(
            menu,
            "Zoom In",
        )

        self._action(
            menu,
            "Zoom Out",
        )
        ##################################################################
    # RUN MENU
    ##################################################################

    def create_run_menu(
        self,
    ) -> None:

        menu = self.menu_bar.addMenu("&Run")

        self._action(
            menu,
            "Run",
        )

        self._action(
            menu,
            "Debug",
        )

        self._action(
            menu,
            "Stop",
        )
        ##################################################################
    # AI MENU
    ##################################################################

    def create_ai_menu(
        self,
    ) -> None:

        menu = self.menu_bar.addMenu("&AI")

        self._action(
            menu,
            "Ask AI",
        )

        self._action(
            menu,
            "Explain Code",
        )

        self._action(
            menu,
            "Refactor Code",
        )

        self._action(
            menu,
            "Debug with AI",
        )
        ##################################################################
    # GIT MENU
    ##################################################################

    def create_git_menu(
        self,
    ) -> None:

        menu = self.menu_bar.addMenu("&Git")

        self._action(
            menu,
            "Commit",
        )

        self._action(
            menu,
            "Push",
        )

        self._action(
            menu,
            "Pull",
        )
        ##################################################################
    # HELP MENU
    ##################################################################

    def create_help_menu(
        self,
    ) -> None:

        menu = self.menu_bar.addMenu("&Help")

        self._action(
            menu,
            "Documentation",
        )

        self._action(
            menu,
            "About",
        )

    def build(
        self,
    ) -> None:

        self.create_file_menu()

        self.create_edit_menu()

        self.create_view_menu()

        self.create_run_menu()

        self.create_ai_menu()

        self.create_git_menu()

        self.create_help_menu()    

    ##################################################################
    # ACTION FACTORY
    ##################################################################

    def _action(
        self,
        menu: QMenu,
        text: str,
        shortcut: QKeySequence | None = None,
    ) -> QAction:
        """
        Create a QAction, optionally assign a shortcut,
        add it to the given menu, and return it.
        """

        action = QAction(
            text,
            self.window,
        )

        if shortcut is not None:
            action.setShortcut(
                shortcut,
            )

        menu.addAction(
            action,
        )

        logger.debug(
            "Menu Action Created: %s",
            text,
        )

        return action