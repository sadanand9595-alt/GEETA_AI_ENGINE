"""
==============================================================================
GEETA AI Engine

File        : claude_provider.py
Package     : providers
Description : Anthropic Claude Provider

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Any

from anthropic import Anthropic

from config.logger import get_logger
from providers.base_provider import BaseProvider

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Claude Provider
###############################################################################


class ClaudeProvider(BaseProvider):
    """
    Anthropic Claude provider implementation.

    Supports:

    - Claude Sonnet
    - Claude Opus
    - Claude Haiku
    - Future Claude models
    """

    def __init__(
        self,
        api_key: str,
        model: str = "claude-sonnet-4",
    ) -> None:

        super().__init__(
            name="claude",
            model=model,
        )

        self._client = Anthropic(
            api_key=api_key,
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
            "Claude generate request."
        )

        response = self._client.messages.create(
            model=self.model,
            max_tokens=kwargs.pop(
                "max_tokens",
                4096,
            ),
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            **kwargs,
        )

        return response.content[0].text

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
            "Claude chat request."
        )

        response = self._client.messages.create(
            model=self.model,
            max_tokens=kwargs.pop(
                "max_tokens",
                4096,
            ),
            messages=messages,
            **kwargs,
        )

        return response.content[0].text

    ###########################################################################

    def embeddings(
        self,
        text: str,
    ) -> list[float]:
        """
        Claude does not currently provide
        public embedding models.
        """

        raise NotImplementedError(
            "Claude embeddings are not supported."
        )
###############################################################################
# Health Check
###############################################################################

    def test_connection(self) -> bool:
        """
        Test Claude connectivity.
        """

        try:

            self.generate(
                "Connection test.",
                max_tokens=8,
            )

            logger.info(
                "Claude connection successful."
            )

            return True

        except Exception:

            logger.exception(
                "Claude connection failed."
            )

            return False


###############################################################################
# Available Models
###############################################################################

    def available_models(
        self,
    ) -> list[str]:
        """
        Return supported Claude models.
        """

        return [
            "claude-opus-4",
            "claude-sonnet-4",
            "claude-3-7-sonnet-latest",
            "claude-3-5-sonnet-latest",
            "claude-3-5-haiku-latest",
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
                "provider": "Anthropic",
                "supports_chat": True,
                "supports_generate": True,
                "supports_embeddings": False,
            }
        )

        return data


###############################################################################
# Lifecycle
###############################################################################

    def initialize(self) -> None:
        """
        Initialize Claude provider.
        """

        logger.info(
            "Initializing Claude Provider..."
        )

        super().initialize()


    def shutdown(self) -> None:
        """
        Shutdown Claude provider.
        """

        logger.info(
            "Shutting down Claude Provider..."
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
            f"ClaudeProvider("
            f"model='{self.model}', "
            f"enabled={self.enabled})"
        )


###############################################################################
# Exports
###############################################################################

__all__ = [
    "ClaudeProvider",
]