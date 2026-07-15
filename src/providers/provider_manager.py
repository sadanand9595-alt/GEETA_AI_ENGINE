"""
==============================================================================
GEETA AI Engine

File        : provider_manager.py
Package     : providers
Description : AI Provider Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Any

from config.logger import get_logger
from providers.base_provider import BaseProvider

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Provider Manager
###############################################################################


class ProviderManager:
    """
    Central manager for all AI providers.

    Responsibilities:

    - Register providers
    - Remove providers
    - Select active provider
    - Model switching
    - Provider failover
    """

    def __init__(self) -> None:

        self._providers: dict[str, BaseProvider] = {}

        self._active_provider: str | None = None

        logger.info(
            "Provider Manager initialized."
        )

    ###########################################################################

    def register(
        self,
        provider: BaseProvider,
    ) -> None:
        """
        Register a provider.
        """

        if provider.name in self._providers:

            raise ValueError(
                f"Provider '{provider.name}' already exists."
            )

        provider.initialize()

        self._providers[
            provider.name
        ] = provider

        if self._active_provider is None:

            self._active_provider = provider.name

        logger.info(
            "Registered provider: %s",
            provider.name,
        )

    ###########################################################################

    def unregister(
        self,
        name: str,
    ) -> None:
        """
        Remove provider.
        """

        provider = self._providers.pop(
            name,
            None,
        )

        if provider is None:
            return

        provider.shutdown()

        logger.info(
            "Removed provider: %s",
            name,
        )

        if self._active_provider == name:

            self._active_provider = None

    ###########################################################################

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check provider existence.
        """

        return name in self._providers

    ###########################################################################

    def get(
        self,
        name: str,
    ) -> BaseProvider:
        """
        Return provider instance.
        """

        return self._providers[name]

    ###########################################################################

    def providers(
        self,
    ) -> list[str]:
        """
        Return provider names.
        """

        return sorted(
            self._providers.keys()
        )

    ###########################################################################

    @property
    def active_provider(
        self,
    ) -> BaseProvider | None:
        """
        Return active provider.
        """

        if self._active_provider is None:

            return None

        return self._providers[
            self._active_provider
        ]
###############################################################################
# Active Provider
###############################################################################

    def set_active(
        self,
        name: str,
    ) -> None:
        """
        Set active provider.
        """

        if name not in self._providers:

            raise ValueError(
                f"Unknown provider: {name}"
            )

        self._active_provider = name

        logger.info(
            "Active provider changed to: %s",
            name,
        )

###############################################################################
# AI Operations
###############################################################################

    def generate(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        """
        Generate text using active provider.
        """

        provider = self.active_provider

        if provider is None:

            raise RuntimeError(
                "No active provider."
            )

        return provider.generate(
            prompt,
            **kwargs,
        )

    ###########################################################################

    def chat(
        self,
        messages: list[dict[str, str]],
        **kwargs: Any,
    ) -> str:
        """
        Execute chat completion.
        """

        provider = self.active_provider

        if provider is None:

            raise RuntimeError(
                "No active provider."
            )

        return provider.chat(
            messages,
            **kwargs,
        )

    ###########################################################################

    def embeddings(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate embeddings.
        """

        provider = self.active_provider

        if provider is None:

            raise RuntimeError(
                "No active provider."
            )

        return provider.embeddings(text)

###############################################################################
# Shutdown
###############################################################################

    def shutdown_all(self) -> None:
        """
        Shutdown every registered provider.
        """

        for provider in self._providers.values():

            provider.shutdown()

        logger.info(
            "All providers shut down."
        )

###############################################################################
# Utilities
###############################################################################

    def count(self) -> int:
        """
        Return provider count.
        """

        return len(self._providers)

###############################################################################
# Global Manager
###############################################################################

provider_manager = ProviderManager()

###############################################################################
# Helper Functions
###############################################################################


def register_provider(
    provider: BaseProvider,
) -> None:
    """
    Register provider.
    """

    provider_manager.register(provider)


def active_provider() -> BaseProvider | None:
    """
    Return current active provider.
    """

    return provider_manager.active_provider


###############################################################################
# Exports
###############################################################################

__all__ = [
    "ProviderManager",
    "provider_manager",
    "register_provider",
    "active_provider",
]