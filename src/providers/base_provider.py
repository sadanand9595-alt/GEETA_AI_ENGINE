"""
==============================================================================
GEETA AI Engine

File        : base_provider.py
Package     : providers
Description : Base AI Provider

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
# Base Provider
###############################################################################


class BaseProvider(ABC):
    """
    Base class for every AI provider.

    Examples:

    - OpenAI
    - Claude
    - Gemini
    - DeepSeek
    - OpenRouter
    - Ollama
    - LM Studio
    """

    def __init__(
        self,
        name: str,
        model: str,
    ) -> None:

        self._name = name

        self._model = model

        self._enabled = True

        logger.info(
            "Initialized provider: %s",
            self._name,
        )

    ###########################################################################

    @property
    def name(self) -> str:
        """
        Provider name.
        """

        return self._name

    ###########################################################################

    @property
    def model(self) -> str:
        """
        Active model.
        """

        return self._model

    ###########################################################################

    @property
    def enabled(self) -> bool:
        """
        Return provider state.
        """

        return self._enabled

    ###########################################################################

    def enable(self) -> None:
        """
        Enable provider.
        """

        self._enabled = True

    ###########################################################################

    def disable(self) -> None:
        """
        Disable provider.
        """

        self._enabled = False

    ###########################################################################

    @abstractmethod
    def generate(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        """
        Generate text response.
        """

    ###########################################################################

    @abstractmethod
    def chat(
        self,
        messages: list[dict[str, str]],
        **kwargs: Any,
    ) -> str:
        """
        Chat completion.
        """

    ###########################################################################

    @abstractmethod
    def embeddings(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate embeddings.
        """
###############################################################################
# Provider Information
###############################################################################

    def metadata(self) -> dict[str, Any]:
        """
        Return provider metadata.
        """

        return {
            "name": self.name,
            "model": self.model,
            "enabled": self.enabled,
        }


###############################################################################
# Model Management
###############################################################################

    def set_model(
        self,
        model: str,
    ) -> None:
        """
        Change the active model.
        """

        logger.info(
            "Changing model from '%s' to '%s'",
            self._model,
            model,
        )

        self._model = model


###############################################################################
# Health Check
###############################################################################

    def healthy(self) -> bool:
        """
        Return provider health status.
        """

        return self.enabled


###############################################################################
# Connection Test
###############################################################################

    def test_connection(self) -> bool:
        """
        Test provider availability.

        Override in provider implementations if
        API connectivity checks are supported.
        """

        logger.info(
            "Testing provider: %s",
            self.name,
        )

        return self.healthy()


###############################################################################
# Lifecycle
###############################################################################

    def initialize(self) -> None:
        """
        Initialize provider resources.
        """

        logger.info(
            "Initializing provider: %s",
            self.name,
        )


    def shutdown(self) -> None:
        """
        Release provider resources.
        """

        logger.info(
            "Shutting down provider: %s",
            self.name,
        )


###############################################################################
# Representation
###############################################################################

    def __repr__(self) -> str:
        """
        Developer-friendly representation.
        """

        return (
            f"{self.__class__.__name__}"
            f"(name='{self.name}', "
            f"model='{self.model}', "
            f"enabled={self.enabled})"
        )


###############################################################################
# Exports
###############################################################################

__all__ = [
    "BaseProvider",
]