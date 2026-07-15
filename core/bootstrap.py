"""
GEETA AI ENGINE
Bootstrap Manager
"""

from __future__ import annotations

import logging

from core.event_bus import EventBus, event_bus
from ui.main_window import MainWindow

logger = logging.getLogger(__name__)


class Bootstrap:
    """
    Application Bootstrap Manager.
    Creates and initializes all core services.
    """

    def __init__(self, events: EventBus | None = None) -> None:

        logger.info("Bootstrap created")

        self.database = None
        self.providers = None
        self.plugins = None
        self.worker = None
        self.vscode = None
        self.command_palette = None
        self.chat_panel = None
        self.inline_ai = None
        self._events = events or event_bus
        self._initialized = False
        self._window: MainWindow | None = None

    @property
    def initialized(self) -> bool:
        """Return whether the desktop composition root has been initialized."""
        return self._initialized

    ####################################################################

    def initialize(self) -> MainWindow:
        """
        Create the main application window.
        """

        if self._window is not None:
            return self._window

        logger.info("Initializing GEETA AI ENGINE")

        window = MainWindow(
            database=self.database,
            providers=self.providers,
            plugins=self.plugins,
            worker=self.worker,
            vscode=self.vscode,
            command_palette=self.command_palette,
            chat_panel=self.chat_panel,
            inline_ai=self.inline_ai,
        )

        self._window = window
        self._initialized = True
        self._events.publish("application.window_created", window=window)

        logger.info("Main Window created")

        return window

    def shutdown(self) -> None:
        """Publish application shutdown and release bootstrap-owned references."""
        if not self._initialized:
            return

        self._events.publish("application.shutting_down")
        self._window = None
        self._initialized = False
        logger.info("GEETA AI ENGINE bootstrap shut down")
