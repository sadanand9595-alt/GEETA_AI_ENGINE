"""
GEETA AI ENGINE
Application Lifecycle Manager
"""

from __future__ import annotations

import logging

from PySide6.QtCore import QObject, QSettings, Signal
from PySide6.QtWidgets import QApplication, QSplashScreen

logger = logging.getLogger(__name__)


class Application(QObject):
    """
    GEETA Application Lifecycle.
    """

    started = Signal()

    shutting_down = Signal()

    restarted = Signal()

    def __init__(
        self,
        app: QApplication,
    ) -> None:

        super().__init__()

        self.app = app

        self.settings = QSettings(
            "GEETA",
            "AI_ENGINE",
        )

        self.splash: QSplashScreen | None = None

    ###########################################################################

    def show_splash(
        self,
        splash: QSplashScreen,
    ) -> None:

        self.splash = splash

        splash.show()

        self.app.processEvents()

    ###########################################################################

    def finish_splash(
        self,
        window,
    ) -> None:

        if self.splash is not None:

            self.splash.finish(window)

            self.splash = None

    ###########################################################################

    def load_theme(
        self,
        stylesheet: str = "",
    ) -> None:

        self.app.setStyleSheet(
            stylesheet,
        )

        logger.info(
            "Theme loaded."
        )

    ###########################################################################

    def restore_window(
        self,
        window,
    ) -> None:

        geometry = self.settings.value(
            "window/geometry",
        )

        if geometry:

            window.restoreGeometry(
                geometry,
            )

    ###########################################################################

    def save_window(
        self,
        window,
    ) -> None:

        self.settings.setValue(
            "window/geometry",
            window.saveGeometry(),
        )

    ###########################################################################

    def shutdown(
        self,
    ) -> None:

        logger.info(
            "Application shutting down."
        )

        self.shutting_down.emit()

        self.app.quit()

    ###########################################################################

    def restart(
        self,
    ) -> None:

        logger.info(
            "Application restarting."
        )

        self.restarted.emit()

        self.shutdown()

        QApplication.exit(
            100,
        )

    ###########################################################################

    def execute(
        self,
    ) -> int:

        self.started.emit()

        logger.info(
            "Application started."
        )

        return self.app.exec()