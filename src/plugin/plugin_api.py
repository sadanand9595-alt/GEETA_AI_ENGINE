"""
==============================================================================
GEETA AI Engine

File        : plugin_api.py
Package     : plugins
Description : Plugin API

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Plugin API
###############################################################################


class Plugin(ABC):
    """
    Base class for all GEETA AI IDE plugins.

    Responsibilities

    - Lifecycle management
    - Command registration
    - Service access
    - Version compatibility
    """

    name: str = "Unnamed Plugin"

    version: str = "1.0.0"

    author: str = "Unknown"

    minimum_ide_version: str = "1.0.0"

    ###########################################################################

    @abstractmethod
    def initialize(
        self,
    ) -> None:
        """
        Initialize the plugin.
        """

    ###########################################################################

    @abstractmethod
    def shutdown(
        self,
    ) -> None:
        """
        Shutdown the plugin.
        """

    ###########################################################################

    def reload(
        self,
    ) -> None:
        """
        Reload plugin.
        """

        self.shutdown()

        self.initialize()

    ###########################################################################

    def commands(
        self,
    ) -> dict[str, Any]:
        """
        Return plugin commands.
        """

        return {}

    ###########################################################################

    def services(
        self,
    ) -> dict[str, Any]:
        """
        Return exposed services.
        """

        return {}

    ###########################################################################

    def metadata(
        self,
    ) -> dict[str, Any]:
        """
        Return plugin metadata.
        """

        return {
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "minimum_ide_version":
                self.minimum_ide_version,
        }
###############################################################################
# IDE Services
###############################################################################

    def workspace(
        self,
    ) -> Any | None:
        """
        Return the Workspace service.

        Future versions will return the
        Workspace Manager instance.
        """

        return None

    ###########################################################################

    def runtime(
        self,
    ) -> Any | None:
        """
        Return the Runtime service.

        Future versions will return the
        Runtime Manager instance.
        """

        return None

    ###########################################################################

    def git(
        self,
    ) -> Any | None:
        """
        Return the Git service.

        Future versions will return the
        Git Manager instance.
        """

        return None

    ###########################################################################

    def ai(
        self,
    ) -> Any | None:
        """
        Return the AI service.

        Future versions will return the
        AI Engine instance.
        """

        return None

###############################################################################
# Compatibility
###############################################################################

    def compatible(
        self,
        ide_version: str,
    ) -> bool:
        """
        Validate IDE compatibility.

        Placeholder implementation.
        Future versions will support
        Semantic Version validation.
        """

        return (
            ide_version
            >= self.minimum_ide_version
        )
    
###############################################################################
# Exports
###############################################################################

__all__ = [
    "Plugin",
]