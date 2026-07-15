"""
==============================================================================
GEETA AI Engine

File        : ollama_provider.py
Package     : providers
Description : Ollama Provider

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Any

import ollama

from config.logger import get_logger
from providers.base_provider import BaseProvider

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Ollama Provider
###############################################################################


class OllamaProvider(BaseProvider):
    """
    Ollama provider implementation.

    Supports local models such as:

    - Llama 3.x
    - DeepSeek R1
    - Qwen
    - Gemma
    - Phi
    - Mistral
    - CodeLlama
    """

    def __init__(
        self,
        model: str = "llama3.3",
        host: str = "http://localhost:11434",
    ) -> None:

        super().__init__(
            name="ollama",
            model=model,
        )

        self._client = ollama.Client(
            host=host,
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
            "Ollama generate request."
        )

        response = self._client.generate(
            model=self.model,
            prompt=prompt,
            **kwargs,
        )

        return response["response"]

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
            "Ollama chat request."
        )

        response = self._client.chat(
            model=self.model,
            messages=messages,
            **kwargs,
        )

        return response["message"]["content"]

    ###########################################################################

    def embeddings(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate embeddings.
        """

        logger.info(
            "Ollama embedding request."
        )

        response = self._client.embeddings(
            model=self.model,
            prompt=text,
        )

        return response["embedding"]
###############################################################################
# Health Check
###############################################################################

    def test_connection(self) -> bool:
        """
        Test Ollama server connectivity.
        """

        try:

            self._client.list()

            logger.info(
                "Ollama connection successful."
            )

            return True

        except Exception:

            logger.exception(
                "Ollama connection failed."
            )

            return False


###############################################################################
# Model Management
###############################################################################

    def available_models(
        self,
    ) -> list[str]:
        """
        Return installed Ollama models.
        """

        try:

            response = self._client.list()

            return [
                model["model"]
                for model in response.get(
                    "models",
                    [],
                )
            ]

        except Exception:

            logger.exception(
                "Unable to retrieve Ollama models."
            )

            return []


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
                "provider": "Ollama",
                "supports_chat": True,
                "supports_generate": True,
                "supports_embeddings": True,
                "offline": True,
                "local": True,
            }
        )

        return data


###############################################################################
# Lifecycle
###############################################################################

    def initialize(self) -> None:
        """
        Initialize Ollama provider.
        """

        logger.info(
            "Initializing Ollama Provider..."
        )

        super().initialize()

    ###########################################################################

    def shutdown(self) -> None:
        """
        Shutdown Ollama provider.
        """

        logger.info(
            "Shutting down Ollama Provider..."
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
            f"OllamaProvider("
            f"model='{self.model}', "
            f"enabled={self.enabled})"
        )


###############################################################################
# Exports
###############################################################################

__all__ = [
    "OllamaProvider",
]