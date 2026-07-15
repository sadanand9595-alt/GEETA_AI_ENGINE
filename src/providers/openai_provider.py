"""
==============================================================================
GEETA AI Engine

File        : openai_provider.py
Package     : providers
Description : OpenAI Provider

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
# OpenAI Provider
###############################################################################


class OpenAIProvider(BaseProvider):
    """
    OpenAI provider implementation.

    Supports:

    - GPT-5.5
    - GPT-5
    - GPT-4.1
    - Future OpenAI models
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-5.5",
    ) -> None:

        super().__init__(
            name="openai",
            model=model,
        )

        self._client = OpenAI(
            api_key=api_key,
        )

    ###########################################################################

    def generate(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        """
        Generate text completion.
        """

        logger.info(
            "OpenAI generate request."
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
            "OpenAI chat request."
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
            "OpenAI embeddings request."
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
        Test OpenAI connectivity.
        """

        try:

            self._client.models.list()

            logger.info(
                "OpenAI connection successful."
            )

            return True

        except Exception:

            logger.exception(
                "OpenAI connection failed."
            )

            return False


###############################################################################
# Model Management
###############################################################################

    def available_models(
        self,
    ) -> list[str]:
        """
        Return available OpenAI models.
        """

        return [
            "gpt-5.5",
            "gpt-5",
            "gpt-4.1",
            "gpt-4.1-mini",
            "gpt-4o",
            "gpt-4o-mini",
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
                "provider": "OpenAI",
                "supports_chat": True,
                "supports_generate": True,
                "supports_embeddings": True,
            }
        )

        return data


###############################################################################
# Lifecycle
###############################################################################

    def initialize(self) -> None:
        """
        Initialize provider.
        """

        logger.info(
            "Initializing OpenAI Provider..."
        )

        super().initialize()


    def shutdown(self) -> None:
        """
        Shutdown provider.
        """

        logger.info(
            "Shutting down OpenAI Provider..."
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
            f"OpenAIProvider("
            f"model='{self.model}', "
            f"enabled={self.enabled})"
        )


###############################################################################
# Exports
###############################################################################

__all__ = [
    "OpenAIProvider",
]