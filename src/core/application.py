"""
==============================================================================
GEETA AI Engine

File        : application.py
Package     : core
Description : Core Application Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import signal
from typing import Optional

from config.logger import get_logger
from database.migrations import initialize_database

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Application
###############################################################################


class Application:
    """
    Main application lifecycle manager.
    """

    def __init__(self) -> None:

        self._running: bool = False

        logger.info("Application created.")

    ###########################################################################

    @property
    def running(self) -> bool:
        """
        Return application state.
        """

        return self._running

    ###########################################################################

    def initialize(self) -> None:
        """
        Initialize application resources.
        """

        logger.info("Initializing GEETA AI Engine...")

        initialize_database()

        logger.info("Database initialized.")

    ###########################################################################

    def start(self) -> None:
        """
        Start application.
        """

        if self._running:
            return

        logger.info("Starting GEETA AI Engine...")

        self.initialize()

        self._running = True

        logger.info("Application started successfully.")

    ###########################################################################

    def stop(self) -> None:
        """
        Stop application.
        """

        if not self._running:
            return

        logger.info("Stopping GEETA AI Engine...")

        self._running = False

        logger.info("Application stopped.")

    ###########################################################################

    def restart(self) -> None:
        """
        Restart application.
        """

        logger.info("Restarting application...")

        self.stop()

        self.start()
###############################################################################
# Signal Handling
###############################################################################

    def _handle_shutdown_signal(
        self,
        signum: int,
        frame: Optional[object],
    ) -> None:
        """
        Handle operating system shutdown signals.

        Args:
            signum:
                Signal number.

            frame:
                Current execution frame.
        """

        logger.info("Shutdown signal received (%s).", signum)

        self.stop()

    ###########################################################################

    def register_signal_handlers(self) -> None:
        """
        Register operating system signal handlers.
        """

        signal.signal(signal.SIGINT, self._handle_shutdown_signal)
        signal.signal(signal.SIGTERM, self._handle_shutdown_signal)

        logger.info("Signal handlers registered.")

    ###########################################################################

    def run(self) -> None:
        """
        Run the application.
        """

        self.register_signal_handlers()

        self.start()

        logger.info("GEETA AI Engine is running.")

        try:

            while self.running:
                signal.pause()

        except KeyboardInterrupt:

            logger.info("Keyboard interrupt received.")

            self.stop()

    ###########################################################################

    def shutdown(self) -> None:
        """
        Shutdown application gracefully.
        """

        logger.info("Gracefully shutting down application...")

        self.stop()

        logger.info("Shutdown complete.")


###############################################################################
# Global Application Instance
###############################################################################

application = Application()

###############################################################################
# Helper Functions
###############################################################################


def run_application() -> None:
    """
    Start and run the application.
    """

    application.run()


def stop_application() -> None:
    """
    Stop the application.
    """

    application.shutdown()


###############################################################################
# Exports
###############################################################################

__all__ = [
    "Application",
    "application",
    "run_application",
    "stop_application",
]