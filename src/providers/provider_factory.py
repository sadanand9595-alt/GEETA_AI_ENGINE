"""
==============================================================================
GEETA AI Engine

File        : provider_factory.py
Package     : providers
Description : AI Provider Factory

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from threading import Lock
from typing import Any

from config.logger import get_logger

from providers.base_provider import BaseProvider
from providers.provider_manager import provider_manager
from providers.provider_registry import provider_registry

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Provider Factory
###############################################################################


class ProviderFactory:
    """
    Enterprise AI Provider Factory.

    Responsibilities
    ----------------

    • Lazy provider creation
    • Singleton provider instances
    • Provider caching
    • Thread safety
    • Dependency injection ready
    • Automatic ProviderManager integration
    """

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._instances: dict[
            str,
            BaseProvider,
        ] = {}

        self._lock = Lock()

        logger.info(
            "ProviderFactory initialized."
        )

    ###########################################################################
    # Queries
    ###########################################################################

    def exists(
        self,
        provider_name: str,
    ) -> bool:

        return provider_name in self._instances

    ###########################################################################

    def providers(
        self,
    ) -> list[str]:

        return provider_registry.providers()

    ###########################################################################

    def count(
        self,
    ) -> int:

        return len(
            self._instances,
        )

    ###########################################################################
    # Provider Creation
    ###########################################################################

    def create(
        self,
        provider_name: str,
        **kwargs: Any,
    ) -> BaseProvider:
        """
        Create provider instance.

        Existing instances are reused.
        """

        with self._lock:

            if provider_name in self._instances:

                logger.debug(
                    "Using cached provider: %s",
                    provider_name,
                )

                return self._instances[
                    provider_name
                ]

            logger.info(
                "Creating provider: %s",
                provider_name,
            )

            provider = provider_registry.create(
                provider_name,
                **kwargs,
            )

            provider.initialize()

            self._instances[
                provider_name
            ] = provider

            if not provider_manager.exists(
                provider.name,
            ):

                provider_manager.register(
                    provider,
                )

            return provider
            ###########################################################################
    # Provider Retrieval
    ###########################################################################

    def get(
        self,
        provider_name: str,
        **kwargs: Any,
    ) -> BaseProvider:
        """
        Return provider instance.

        Creates provider lazily if necessary.
        """

        if self.exists(
            provider_name,
        ):

            return self._instances[
                provider_name
            ]

        return self.create(
            provider_name,
            **kwargs,
        )

    ###########################################################################
    # Active Provider
    ###########################################################################

    def active(
        self,
    ) -> BaseProvider | None:
        """
        Return active provider.
        """

        return provider_manager.active_provider

    ###########################################################################
    # Provider Switching
    ###########################################################################

    def switch(
        self,
        provider_name: str,
        **kwargs: Any,
    ) -> BaseProvider:
        """
        Switch active provider.

        Provider is created automatically if
        it does not already exist.
        """

        provider = self.get(
            provider_name,
            **kwargs,
        )

        provider_manager.set_active(
            provider.name,
        )

        logger.info(
            "Switched active provider to %s",
            provider.name,
        )

        return provider

    ###########################################################################
    # Reload Provider
    ###########################################################################

    def reload(
        self,
        provider_name: str,
        **kwargs: Any,
    ) -> BaseProvider:
        """
        Reload provider instance.
        """

        self.remove(
            provider_name,
        )

        return self.create(
            provider_name,
            **kwargs,
        )

    ###########################################################################
    # Remove Provider
    ###########################################################################

    def remove(
        self,
        provider_name: str,
    ) -> None:
        """
        Remove cached provider.
        """

        with self._lock:

            provider = self._instances.pop(
                provider_name,
                None,
            )

            if provider is None:

                return

            provider.shutdown()

            provider_manager.unregister(
                provider.name,
            )

            logger.info(
                "Removed provider: %s",
                provider.name,
            )

    ###########################################################################
    # Clear Cache
    ###########################################################################

    def clear(
        self,
    ) -> None:
        """
        Remove every provider instance.
        """

        for provider_name in list(
            self._instances.keys(),
        ):

            self.remove(
                provider_name,
            )

        logger.info(
            "Provider cache cleared."
        )
        ###########################################################################
    # Health
    ###########################################################################

    def healthy(
        self,
    ) -> bool:
        """
        Verify every cached provider.
        """

        for provider in self._instances.values():

            if not provider.healthy():

                return False

        return True

    ###########################################################################
    # Diagnostics
    ###########################################################################

    def diagnostics(
        self,
    ) -> dict[str, Any]:
        """
        Return factory diagnostics.
        """

        return {
            "provider_count": self.count(),
            "providers": list(self._instances.keys()),
            "registered": provider_registry.providers(),
            "active": (
                provider_manager.active_provider.name
                if provider_manager.active_provider
                else None
            ),
            "healthy": self.healthy(),
        }

    ###########################################################################
    # Shutdown
    ###########################################################################

    def shutdown(
        self,
    ) -> None:
        """
        Shutdown Provider Factory.
        """

        logger.info(
            "Shutting down Provider Factory."
        )

        self.clear()

###############################################################################
# Global Factory
###############################################################################

provider_factory = ProviderFactory()

###############################################################################
# Helper Functions
###############################################################################


def get_provider(
    provider_name: str,
    **kwargs: Any,
) -> BaseProvider:
    """
    Return provider instance.
    """

    return provider_factory.get(
        provider_name,
        **kwargs,
    )


def switch_provider(
    provider_name: str,
    **kwargs: Any,
) -> BaseProvider:
    """
    Switch active provider.
    """

    return provider_factory.switch(
        provider_name,
        **kwargs,
    )


def provider_diagnostics(
) -> dict[str, Any]:
    """
    Return diagnostics.
    """

    return provider_factory.diagnostics()


###############################################################################
# Exports
###############################################################################

__all__ = [
    "ProviderFactory",
    "provider_factory",
    "get_provider",
    "switch_provider",
    "provider_diagnostics",
]