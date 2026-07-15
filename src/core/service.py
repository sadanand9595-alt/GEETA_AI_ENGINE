"""
==============================================================================
GEETA AI Engine

File        : service.py
Package     : core
Description : Base Service Infrastructure

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from abc import ABC
from threading import RLock
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Base Service
###############################################################################


class BaseService(ABC):
    """
    Enterprise base class for every long-running service.

    Features
    --------
    - Lifecycle management
    - Health reporting
    - Diagnostics
    - Thread safety
    - Metadata
    - Enable / Disable
    """

    ###########################################################################

    def __init__(
        self,
        name: str,
    ) -> None:

        self._name = name

        self._enabled = True

        self._initialized = False

        self._lock = RLock()

        logger.info(
            "%s created.",
            self._name,
        )

    ###########################################################################
    # Properties
    ###########################################################################

    @property
    def name(
        self,
    ) -> str:

        return self._name

    ###########################################################################

    @property
    def enabled(
        self,
    ) -> bool:

        return self._enabled

    ###########################################################################

    @property
    def initialized(
        self,
    ) -> bool:

        return self._initialized

    ###########################################################################
    # Lifecycle
    ###########################################################################

    def initialize(
        self,
    ) -> None:
        """
        Initialize service.
        """

        with self._lock:

            if self._initialized:

                return

            self._initialized = True

            logger.info(
                "%s initialized.",
                self._name,
            )

    ###########################################################################

    def shutdown(
        self,
    ) -> None:
        """
        Shutdown service.
        """

        with self._lock:

            self._initialized = False

            logger.info(
                "%s shutdown.",
                self._name,
            )
            ###############################################################################
# State Management
###############################################################################

    def enable(
        self,
    ) -> None:
        """
        Enable service.
        """

        with self._lock:

            self._enabled = True

            logger.info(
                "%s enabled.",
                self._name,
            )

    ###########################################################################

    def disable(
        self,
    ) -> None:
        """
        Disable service.
        """

        with self._lock:

            self._enabled = False

            logger.info(
                "%s disabled.",
                self._name,
            )

###############################################################################
# Health
###############################################################################

    def healthy(
        self,
    ) -> bool:
        """
        Return service health.
        """

        return (
            self._enabled
            and self._initialized
        )

###############################################################################
# Metadata
###############################################################################

    def metadata(
        self,
    ) -> dict[str, Any]:
        """
        Return service metadata.
        """

        return {
            "name": self.name,
            "enabled": self.enabled,
            "initialized": self.initialized,
            "healthy": self.healthy(),
        }

###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, Any]:
        """
        Return service diagnostics.
        """

        return self.metadata()

###############################################################################
# Reset
###############################################################################

    def reset(
        self,
    ) -> None:
        """
        Reset service state.
        """

        with self._lock:

            self._initialized = False

        logger.info(
            "%s reset.",
            self._name,
        )

###############################################################################
# Representation
###############################################################################

    def __repr__(
        self,
    ) -> str:
        """
        Developer-friendly representation.
        """

        return (
            f"{self.__class__.__name__}"
            f"(name='{self.name}', "
            f"enabled={self.enabled}, "
            f"initialized={self.initialized})"
        )
        ###############################################################################
# Lifecycle Hooks
###############################################################################

    def before_initialize(
        self,
    ) -> None:
        """
        Hook executed before initialize().

        Override in derived services when needed.
        """

    ###########################################################################

    def after_initialize(
        self,
    ) -> None:
        """
        Hook executed after initialize().

        Override in derived services when needed.
        """

    ###########################################################################

    def before_shutdown(
        self,
    ) -> None:
        """
        Hook executed before shutdown().

        Override in derived services when needed.
        """

    ###########################################################################

    def after_shutdown(
        self,
    ) -> None:
        """
        Hook executed after shutdown().

        Override in derived services when needed.
        """

###############################################################################
# Context Manager
###############################################################################

    def __enter__(
        self,
    ) -> "BaseService":

        self.initialize()

        return self

    ###########################################################################

    def __exit__(
        self,
        exc_type,
        exc,
        tb,
    ) -> bool:

        self.shutdown()

        return False

###############################################################################
# Utility
###############################################################################

    def is_ready(
        self,
    ) -> bool:
        """
        Return True when the service can be used.
        """

        return (
            self.initialized
            and self.enabled
        )

###############################################################################
# Exports
###############################################################################

__all__ = [
    "BaseService",
]