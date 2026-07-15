"""
==============================================================================
GEETA AI Engine

File        : plugin_manager.py
Package     : core
Description : Plugin Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import threading
from abc import ABC, abstractmethod

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Plugin Base
###############################################################################


class Plugin(ABC):
    """
    Base class for all GEETA AI Engine plugins.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Plugin name.
        """

    @property
    @abstractmethod
    def version(self) -> str:
        """
        Plugin version.
        """

    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the plugin.
        """

    @abstractmethod
    def shutdown(self) -> None:
        """
        Shutdown the plugin.
        """


###############################################################################
# Plugin Manager
###############################################################################


class PluginManager:
    """
    Thread-safe Plugin Manager.
    """

    def __init__(self) -> None:

        self._lock = threading.RLock()

        self._plugins: dict[str, Plugin] = {}

        logger.info("PluginManager initialized.")

    ###########################################################################

    def register(
        self,
        plugin: Plugin,
    ) -> None:
        """
        Register a plugin.
        """

        with self._lock:

            if plugin.name in self._plugins:

                raise ValueError(
                    f"Plugin '{plugin.name}' already registered."
                )

            plugin.initialize()

            self._plugins[plugin.name] = plugin

            logger.info(
                "Plugin registered: %s (%s)",
                plugin.name,
                plugin.version,
            )

    ###########################################################################

    def unregister(
        self,
        name: str,
    ) -> None:
        """
        Unregister a plugin.
        """

        with self._lock:

            plugin = self._plugins.pop(name, None)

            if plugin is None:
                return

            plugin.shutdown()

            logger.info(
                "Plugin unregistered: %s",
                name,
            )

    ###########################################################################

    def get(
        self,
        name: str,
    ) -> Plugin:
        """
        Return plugin instance.
        """

        return self._plugins[name]

    ###########################################################################

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check whether plugin exists.
        """

        return name in self._plugins
###############################################################################
# Plugin Management
###############################################################################

    def plugins(self) -> list[str]:
        """
        Return all registered plugin names.
        """

        with self._lock:

            return sorted(self._plugins.keys())

    ###########################################################################

    def plugin_count(self) -> int:
        """
        Return number of registered plugins.
        """

        with self._lock:

            return len(self._plugins)

    ###########################################################################

    def initialize_all(self) -> None:
        """
        Initialize all registered plugins.
        """

        with self._lock:

            for plugin in self._plugins.values():

                logger.info(
                    "Initializing plugin: %s",
                    plugin.name,
                )

                plugin.initialize()

    ###########################################################################

    def shutdown_all(self) -> None:
        """
        Shutdown all registered plugins.
        """

        with self._lock:

            for plugin in reversed(
                list(self._plugins.values())
            ):

                logger.info(
                    "Shutting down plugin: %s",
                    plugin.name,
                )

                plugin.shutdown()

    ###########################################################################

    def clear(self) -> None:
        """
        Shutdown and remove all plugins.
        """

        self.shutdown_all()

        with self._lock:

            self._plugins.clear()

            logger.info(
                "All plugins removed."
            )


###############################################################################
# Global Plugin Manager
###############################################################################

plugin_manager = PluginManager()

###############################################################################
# Helper Functions
###############################################################################


def register_plugin(
    plugin: Plugin,
) -> None:
    """
    Register a plugin.
    """

    plugin_manager.register(plugin)


def unregister_plugin(
    name: str,
) -> None:
    """
    Unregister a plugin.
    """

    plugin_manager.unregister(name)


def get_plugin(
    name: str,
) -> Plugin:
    """
    Return plugin instance.
    """

    return plugin_manager.get(name)


###############################################################################
# Exports
###############################################################################

__all__ = [
    "Plugin",
    "PluginManager",
    "plugin_manager",
    "register_plugin",
    "unregister_plugin",
    "get_plugin",
]