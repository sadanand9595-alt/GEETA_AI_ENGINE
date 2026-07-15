"""
==============================================================================
GEETA AI Engine

File        : plugin_context.py
Package     : plugins
Description : Plugin Context

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Plugin Context
###############################################################################


class PluginContext:
    """
    Dependency-injected execution context
    for GEETA AI IDE plugins.

    Responsibilities

    - Workspace access
    - Runtime access
    - Git access
    - AI Engine access
    - Event access
    - Shared state
    """

    def __init__(self) -> None:

        self._services: dict[
            str,
            Any,
        ] = {}

        self._shared_state: dict[
            str,
            Any,
        ] = {}

        logger.info(
            "Plugin Context initialized."
        )

    ###########################################################################

    def register_service(
        self,
        name: str,
        service: Any,
    ) -> None:
        """
        Register a service.
        """

        self._services[
            name
        ] = service

    ###########################################################################

    def service(
        self,
        name: str,
    ) -> Any | None:
        """
        Return a registered service.
        """

        return self._services.get(
            name,
        )

    ###########################################################################

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store shared state.
        """

        self._shared_state[
            key
        ] = value

    ###########################################################################

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Return shared state.
        """

        return self._shared_state.get(
            key,
            default,
        )
###############################################################################
# Service Information
###############################################################################

    def services(
        self,
    ) -> dict[str, Any]:
        """
        Return registered services.
        """

        return dict(
            self._services
        )

###############################################################################
# Shared State
###############################################################################

    def shared_state(
        self,
    ) -> dict[str, Any]:
        """
        Return shared plugin state.
        """

        return dict(
            self._shared_state
        )

    ###########################################################################

    def clear_state(
        self,
    ) -> None:
        """
        Clear all shared state.
        """

        self._shared_state.clear()

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return plugin context statistics.
        """

        return {
            "registered_services": len(
                self._services
            ),
            "shared_entries": len(
                self._shared_state
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return plugin context report.
        """

        return {
            "statistics": self.statistics(),
            "services": list(
                self._services.keys()
            ),
            "shared_keys": list(
                self._shared_state.keys()
            ),
        }

###############################################################################
# Global Plugin Context
###############################################################################

plugin_context = PluginContext()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "PluginContext",
    "plugin_context",
]