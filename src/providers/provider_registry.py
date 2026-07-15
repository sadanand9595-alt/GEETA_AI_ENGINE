"""
==============================================================================
GEETA AI Engine

File        : provider_registry.py
Package     : providers
Description : Provider Registry

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Type

from config.logger import get_logger

from providers.base_provider import BaseProvider
from providers.provider_manager import provider_manager

from providers.openai_provider import OpenAIProvider
from providers.claude_provider import ClaudeProvider
from providers.gemini_provider import GeminiProvider
from providers.openrouter_provider import (
    OpenRouterProvider,
)
from providers.ollama_provider import OllamaProvider

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Provider Registry
###############################################################################


class ProviderRegistry:
    """
    Central registry for all AI providers.
    """

    def __init__(self) -> None:

        self._registry: dict[
            str,
            Type[BaseProvider],
        ] = {}

    ###########################################################################

    def register(
        self,
        provider_name: str,
        provider_class: Type[BaseProvider],
    ) -> None:
        """
        Register a provider class.
        """

        self._registry[
            provider_name
        ] = provider_class

        logger.info(
            "Registered provider class: %s",
            provider_name,
        )

    ###########################################################################

    def exists(
        self,
        provider_name: str,
    ) -> bool:
        """
        Check provider existence.
        """

        return provider_name in self._registry

    ###########################################################################

    def create(
        self,
        provider_name: str,
        **kwargs,
    ) -> BaseProvider:
        """
        Create provider instance.
        """

        provider_class = self._registry[
            provider_name
        ]

        return provider_class(
            **kwargs,
        )

    ###########################################################################

    def register_instance(
        self,
        provider_name: str,
        **kwargs,
    ) -> None:
        """
        Create and register provider with
        Provider Manager.
        """

        provider = self.create(
            provider_name,
            **kwargs,
        )

        if not provider_manager.exists(
            provider.name,
        ):

            provider_manager.register(
                provider,
            )
###############################################################################
# Registry Queries
###############################################################################

    def providers(
        self,
    ) -> list[str]:
        """
        Return registered provider names.
        """

        return sorted(
            self._registry.keys()
        )

    ###########################################################################

    def count(
        self,
    ) -> int:
        """
        Return number of registered provider classes.
        """

        return len(
            self._registry
        )

###############################################################################
# Initialization
###############################################################################

    def initialize(self) -> None:
        """
        Register all built-in providers.
        """

        self.register(
            "openai",
            OpenAIProvider,
        )

        self.register(
            "claude",
            ClaudeProvider,
        )

        self.register(
            "gemini",
            GeminiProvider,
        )

        self.register(
            "openrouter",
            OpenRouterProvider,
        )

        self.register(
            "ollama",
            OllamaProvider,
        )

        logger.info(
            "Initialized %d provider classes.",
            self.count(),
        )

###############################################################################
# Global Registry
###############################################################################

provider_registry = ProviderRegistry()

###############################################################################
# Helper Functions
###############################################################################


def initialize_providers() -> None:
    """
    Initialize provider registry.
    """

    provider_registry.initialize()


def available_providers() -> list[str]:
    """
    Return available provider names.
    """

    return provider_registry.providers()


###############################################################################
# Exports
###############################################################################

__all__ = [
    "ProviderRegistry",
    "provider_registry",
    "initialize_providers",
    "available_providers",
]