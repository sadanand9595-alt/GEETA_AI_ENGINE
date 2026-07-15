"""
GEETA AI ENGINE
Professional Toolbar
"""

from __future__ import annotations

import logging

from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QMainWindow,
    QToolBar,
)

logger = logging.getLogger(__name__)


class ToolBarManager:
    """
    Professional IDE Toolbar
    """

    def __init__(
        self,
        window: QMainWindow,
    ) -> None:

        self.window = window

        self.toolbar = QToolBar(
            "Main Toolbar",
            window,
        )

        self.toolbar.setMovable(False)

        self.toolbar.setFloatable(False)

        self.window.addToolBar(
            self.toolbar,
        )

        self.build()

    ##################################################################

    def build(
        self,
    ) -> None:

        
        self.toolbar.addSeparator()

        self.undo_action()

        self.redo_action()

        self.toolbar.addSeparator()

        self.run_action()

        self.debug_action()

        self.toolbar.addSeparator()

        self.ai_action()

        self.search_action()

        self.settings_action()

    ##################################################################

    def add_action(
        self,
        text: str,
        slot=None,
        icon: str = "",
    ) -> QAction:

        action = QAction(
            QIcon(icon),
            text,
            self.window,
        )

        if slot:

            action.triggered.connect(
                slot,
            )

        self.toolbar.addAction(
            action,
        )

        return action

    ##################################################################

    
    ##################################################################
    # File Actions
    ##################################################################

    def new_action(
        self,
    ) -> None:

        self.add_action(
            "Open",
        )

    ##################################################################

    def save_action(
        self,
    ) -> None:

        self.add_action(
            "Save",
        )

        self.toolbar.addSeparator()

    ##################################################################
    # Edit Actions
    ##################################################################

    def undo_action(
        self,
    ) -> None:

        self.add_action(
            "Undo",
        )

    ##################################################################

    def redo_action(
        self,
    ) -> None:

        self.add_action(
            "Redo",
        )

        self.toolbar.addSeparator()

    ##################################################################
    # Run Actions
    ##################################################################

    def run_action(
        self,
    ) -> None:

        self.add_action(
            "Run",
        )

    ##################################################################

    def debug_action(
        self,
    ) -> None:

        self.add_action(
            "Debug",
        )

        self.toolbar.addSeparator()

    ##################################################################
    # AI Actions
    ##################################################################

    def ai_action(
        self,
    ) -> None:

        self.add_action(
            "AI",
        )
##################################################################
    # Search Action
    ##################################################################

    def search_action(
        self,
    ) -> None:

        self.add_action(
            "Search",
        )

    ##################################################################
    # Settings Action
    ##################################################################

    def settings_action(
        self,
    ) -> None:

        self.add_action(
            "Settings",
        )
    ##################################################################
    # Action Factory
    ##################################################################

    def _add_action(
        self,
        text: str,
        callback=None,
    ) -> QAction:
        
        action = QAction(
            text,
            self.window,
        )

        if callback is not None:
            action.triggered.connect(
                callback,
            )

        self.toolbar.addAction(
            action,
        )

        logger.debug(
            "Toolbar action created: %s",
            text,
        )

        return action