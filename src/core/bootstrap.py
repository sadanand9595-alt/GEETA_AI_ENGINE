"""
==============================================================================
GEETA AI Engine

File        : bootstrap.py
Package     : core
Description : Application Bootstrap

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from config.logger import get_logger
from core.application import application
from core.event_bus import event_bus
from core.plugin_manager import plugin_manager
from core.service_container import service_container
from database.database import database
from database.migrations import migration_manager

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Bootstrap
###############################################################################


class Bootstrap:
    """
    Responsible for bootstrapping the GEETA AI Engine.

    Initializes all core infrastructure before the application starts.
    """

    def __init__(self) -> None:

        self._initialized = False

    ###########################################################################

    @property
    def initialized(self) -> bool:
        """
        Return initialization status.
        """

        return self._initialized

    ###########################################################################

    def initialize(self) -> None:
        """
        Initialize all core services.
        """

        if self._initialized:
            return

        logger.info("=" * 80)
        logger.info("GEETA AI Engine Bootstrap")
        logger.info("=" * 80)

        #######################################################################
        # Database
        #######################################################################

        logger.info("Initializing Database...")

        migration_manager.initialize()

        #######################################################################
        # Register Core Services
        #######################################################################

        logger.info("Registering Core Services...")

        service_container.register_singleton(
            "database",
            database,
        )

        service_container.register_singleton(
            "event_bus",
            event_bus,
        )

        service_container.register_singleton(
            "plugin_manager",
            plugin_manager,
        )

        service_container.register_singleton(
            "application",
            application,
        )

        #######################################################################
        # Plugins
        #######################################################################

        logger.info("Initializing Plugin Manager...")

        plugin_manager.initialize_all()

        self._initialized = True

        logger.info("Bootstrap completed successfully.")
###############################################################################
# Shutdown
###############################################################################

    def shutdown(self) -> None:
        """
        Shutdown all core services gracefully.
        """

        if not self._initialized:
            return

        logger.info("=" * 80)
        logger.info("Shutting down GEETA AI Engine...")
        logger.info("=" * 80)

        #######################################################################
        # Shutdown Plugins
        #######################################################################

        logger.info("Shutting down plugins...")

        plugin_manager.shutdown_all()

        #######################################################################
        # Close Database
        #######################################################################

        logger.info("Closing database connection...")

        database.disconnect()

        #######################################################################
        # Clear Service Container
        #######################################################################

        logger.info("Clearing service container...")

        service_container.clear()

        self._initialized = False

        logger.info("Bootstrap shutdown completed successfully.")


###############################################################################
# Global Bootstrap Instance
###############################################################################

bootstrap = Bootstrap()

###############################################################################
# Helper Functions
###############################################################################


def initialize() -> None:
    """
    Initialize GEETA AI Engine.
    """

    bootstrap.initialize()


def shutdown() -> None:
    """
    Shutdown GEETA AI Engine.
    """

    bootstrap.shutdown()


###############################################################################
# Exports
###############################################################################

__all__ = [
    "Bootstrap",
    "bootstrap",
    "initialize",
    "shutdown",
]