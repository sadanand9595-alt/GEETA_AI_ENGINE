"""
==============================================================================
GEETA AI Engine

File        : provider_switcher.py
Package     : providers
Description : Runtime AI Provider Switcher

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from threading import RLock
from typing import Any

from config.logger import get_logger

from providers.base_provider import BaseProvider
from providers.provider_factory import provider_factory
from providers.provider_manager import provider_manager
from providers.provider_settings import provider_settings

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Provider Switcher
###############################################################################


class ProviderSwitcher:
    """
    Runtime Provider Switcher.

    Features
    --------
    • Runtime switching
    • Automatic initialization
    • Thread safe
    • Provider validation
    • Settings synchronization
    """

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._lock = RLock()

        logger.info(
            "Provider Switcher initialized."
        )

    ###########################################################################
    # Current Provider
    ###########################################################################

    def current(
        self,
    ) -> BaseProvider | None:
        """
        Return current provider.
        """

        return provider_manager.active_provider

    ###########################################################################
    # Switch Provider
    ###########################################################################

    def switch(
        self,
        provider_name: str,
        **kwargs: Any,
    ) -> BaseProvider:
        """
        Switch active provider.
        """

        with self._lock:

            logger.info(
                "Switching provider to %s",
                provider_name,
            )

            provider = provider_factory.get(
                provider_name,
                **kwargs,
            )

            provider_manager.set_active(
                provider.name,
            )

            provider_settings.set_provider(
                provider.name,
            )

            logger.info(
                "Provider switched successfully."
            )

            return provider
            ###########################################################################
    # Model Switching
    ###########################################################################

    def switch_model(
        self,
        model: str,
    ) -> None:
        """
        Switch active provider model.
        """

        provider = self.current()

        if provider is None:

            raise RuntimeError(
                "No active provider."
            )

        provider.set_model(
            model,
        )

        provider_settings.set_model(
            model,
        )

        logger.info(
            "Active model changed to %s",
            model,
        )

    ###########################################################################
    # Health
    ###########################################################################

    def healthy(
        self,
    ) -> bool:
        """
        Verify current provider.
        """

        provider = self.current()

        if provider is None:

            return False

        return provider.healthy()

    ###########################################################################
    # Reload
    ###########################################################################

    def reload(
        self,
    ) -> BaseProvider:
        """
        Reload current provider.
        """

        provider = self.current()

        if provider is None:

            raise RuntimeError(
                "No active provider."
            )

        logger.info(
            "Reloading provider %s",
            provider.name,
        )

        return provider_factory.reload(
            provider.name,
        )

    ###########################################################################
    # Reset
    ###########################################################################

    def reset(
        self,
    ) -> None:
        """
        Reset provider cache.
        """

        provider_factory.clear()

        logger.info(
            "Provider cache reset."
        )

    ###########################################################################
    # Validation
    ###########################################################################

    def validate(
        self,
        provider_name: str,
    ) -> bool:
        """
        Validate provider availability.
        """

        return (
            provider_name
            in provider_factory.providers()
        )

    ###########################################################################
    # Available Providers
    ###########################################################################

    def available(
        self,
    ) -> list[str]:
        """
        Return available providers.
        """

        return provider_factory.providers()
        ###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, Any]:
        """
        Return Provider Switcher diagnostics.
        """

        provider = self.current()

        return {
            "active_provider": (
                provider.name
                if provider
                else None
            ),
            "active_model": (
                provider.model
                if provider
                else None
            ),
            "healthy": self.healthy(),
            "available_providers": self.available(),
        }

###############################################################################
# Active Information
###############################################################################

    def active_name(
        self,
    ) -> str | None:
        """
        Return active provider name.
        """

        provider = self.current()

        return (
            provider.name
            if provider
            else None
        )

    ###########################################################################

    def active_model(
        self,
    ) -> str | None:
        """
        Return active model.
        """

        provider = self.current()

        return (
            provider.model
            if provider
            else None
        )

###############################################################################
# Global Switcher
###############################################################################

provider_switcher = ProviderSwitcher()

###############################################################################
# Helper Functions
###############################################################################


def switch_provider(
    provider_name: str,
    **kwargs: Any,
) -> BaseProvider:
    """
    Switch active provider.
    """

    return provider_switcher.switch(
        provider_name,
        **kwargs,
    )


def current_provider(
) -> BaseProvider | None:
    """
    Return active provider.
    """

    return provider_switcher.current()


def provider_health(
) -> bool:
    """
    Return provider health.
    """

    return provider_switcher.healthy()


def provider_info(
) -> dict[str, Any]:
    """
    Return provider diagnostics.
    """

    return provider_switcher.diagnostics()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "ProviderSwitcher",
    "provider_switcher",
    "switch_provider",
    "current_provider",
    "provider_health",
    "provider_info",
]