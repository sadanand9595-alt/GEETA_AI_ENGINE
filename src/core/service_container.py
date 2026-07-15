"""
==============================================================================
GEETA AI Engine

File        : service_container.py
Package     : core
Description : Dependency Injection Service Container

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import threading
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Service Container
###############################################################################


class ServiceContainer:
    """
    Thread-safe Dependency Injection Container.

    Responsible for:

    - Service registration
    - Singleton registration
    - Service resolution
    - Instance management
    """

    def __init__(self) -> None:

        self._lock = threading.RLock()

        self._services: dict[str, Any] = {}

        self._singletons: dict[str, Any] = {}

        logger.info("ServiceContainer initialized.")

    ###########################################################################

    def register(
        self,
        name: str,
        service: Any,
    ) -> None:
        """
        Register a transient service.
        """

        with self._lock:

            self._services[name] = service

            logger.debug(
                "Service registered: %s",
                name,
            )

    ###########################################################################

    def register_singleton(
        self,
        name: str,
        instance: Any,
    ) -> None:
        """
        Register a singleton instance.
        """

        with self._lock:

            self._singletons[name] = instance

            logger.debug(
                "Singleton registered: %s",
                name,
            )

    ###########################################################################

    def resolve(
        self,
        name: str,
    ) -> Any:
        """
        Resolve a service.
        """

        with self._lock:

            if name in self._singletons:
                return self._singletons[name]

            if name in self._services:

                service = self._services[name]

                if callable(service):
                    return service()

                return service

            raise KeyError(
                f"Service '{name}' is not registered."
            )

    ###########################################################################

    def is_registered(
        self,
        name: str,
    ) -> bool:
        """
        Check whether a service is registered.
        """

        return (
            name in self._services
            or name in self._singletons
        )
###############################################################################
# Container Management
###############################################################################

    def remove(
        self,
        name: str,
    ) -> bool:
        """
        Remove a registered service.

        Returns:
            True if removed successfully.
        """

        with self._lock:

            if name in self._services:
                del self._services[name]

                logger.debug(
                    "Service removed: %s",
                    name,
                )

                return True

            if name in self._singletons:
                del self._singletons[name]

                logger.debug(
                    "Singleton removed: %s",
                    name,
                )

                return True

        return False

    ###########################################################################

    def clear(self) -> None:
        """
        Remove all registered services.
        """

        with self._lock:

            self._services.clear()

            self._singletons.clear()

            logger.info(
                "Service container cleared."
            )

    ###########################################################################

    def registered_services(
        self,
    ) -> list[str]:
        """
        Return all registered service names.
        """

        names = set()

        names.update(self._services.keys())

        names.update(self._singletons.keys())

        return sorted(names)

    ###########################################################################

    def service_count(self) -> int:
        """
        Return total registered services.
        """

        return (
            len(self._services)
            + len(self._singletons)
        )


###############################################################################
# Global Service Container
###############################################################################

service_container = ServiceContainer()

###############################################################################
# Helper Functions
###############################################################################


def register_service(
    name: str,
    service: Any,
) -> None:
    """
    Register a transient service.
    """

    service_container.register(name, service)


def register_singleton(
    name: str,
    instance: Any,
) -> None:
    """
    Register a singleton instance.
    """

    service_container.register_singleton(
        name,
        instance,
    )


def resolve(
    name: str,
) -> Any:
    """
    Resolve a registered service.
    """

    return service_container.resolve(name)


###############################################################################
# Exports
###############################################################################

__all__ = [
    "ServiceContainer",
    "service_container",
    "register_service",
    "register_singleton",
    "resolve",
]