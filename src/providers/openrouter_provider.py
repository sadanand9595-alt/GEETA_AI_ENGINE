"""
==============================================================================
GEETA AI Engine

File        : openrouter_provider.py
Package     : providers
Description : OpenRouter Provider

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Any

from openai import OpenAI

from config.logger import get_logger
from providers.base_provider import BaseProvider

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# OpenRouter Provider
###############################################################################


class OpenRouterProvider(BaseProvider):
    """
    OpenRouter provider implementation.

    Supports hundreds of models including:

    - GPT
    - Claude
    - Gemini
    - DeepSeek
    - Llama
    - Qwen
    - Mistral
    - Grok
    """

    BASE_URL = "https://openrouter.ai/api/v1"

    def __init__(
        self,
        api_key: str,
        model: str = "openai/gpt-5.5",
    ) -> None:

        super().__init__(
            name="openrouter",
            model=model,
        )

        self._client = OpenAI(
            api_key=api_key,
            base_url=self.BASE_URL,
        )

    ###########################################################################

    def generate(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        """
        Generate text.
        """

        logger.info(
            "OpenRouter generate request."
        )

        response = self._client.responses.create(
            model=self.model,
            input=prompt,
            **kwargs,
        )

        return response.output_text

    ###########################################################################

    def chat(
        self,
        messages: list[dict[str, str]],
        **kwargs: Any,
    ) -> str:
        """
        Chat completion.
        """

        logger.info(
            "OpenRouter chat request."
        )

        response = self._client.responses.create(
            model=self.model,
            input=messages,
            **kwargs,
        )

        return response.output_text

    ###########################################################################

    def embeddings(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate embeddings.
        """

        logger.info(
            "OpenRouter embedding request."
        )

        response = self._client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
        )

        return response.data[0].embedding
###############################################################################
# Health Check
###############################################################################

    def test_connection(self) -> bool:
        """
        Test OpenRouter connectivity.
        """

        try:

            self.generate(
                "Connection test.",
            )

            logger.info(
                "OpenRouter connection successful."
            )

            return True

        except Exception:

            logger.exception(
                "OpenRouter connection failed."
            )

            return False


###############################################################################
# Available Models
###############################################################################

    def available_models(
        self,
    ) -> list[str]:
        """
        Return commonly used OpenRouter models.
        """

        return [
            "openai/gpt-5.5",
            "openai/gpt-5",
            "anthropic/claude-sonnet-4",
            "anthropic/claude-opus-4",
            "google/gemini-2.5-pro",
            "google/gemini-2.5-flash",
            "deepseek/deepseek-chat",
            "meta-llama/llama-3.3-70b-instruct",
            "qwen/qwen3-235b-a22b",
            "mistralai/mistral-large",
        ]


###############################################################################
# Metadata
###############################################################################

    def metadata(self) -> dict[str, Any]:
        """
        Return provider metadata.
        """

        data = super().metadata()

        data.update(
            {
                "provider": "OpenRouter",
                "supports_chat": True,
                "supports_generate": True,
                "supports_embeddings": True,
                "multi_model": True,
            }
        )

        return data


###############################################################################
# Lifecycle
###############################################################################

    def initialize(self) -> None:
        """
        Initialize OpenRouter provider.
        """

        logger.info(
            "Initializing OpenRouter Provider..."
        )

        super().initialize()

    ###########################################################################

    def shutdown(self) -> None:
        """
        Shutdown OpenRouter provider.
        """

        logger.info(
            "Shutting down OpenRouter Provider..."
        )

        super().shutdown()


###############################################################################
# Representation
###############################################################################

    def __repr__(self) -> str:
        """
        Developer-friendly representation.
        """

        return (
            f"OpenRouterProvider("
            f"model='{self.model}', "
            f"enabled={self.enabled})"
        )


###############################################################################
# Exports
###############################################################################

__all__ = [
    "OpenRouterProvider",
]