"""
==============================================================================
GEETA AI Engine

File        : gemini_provider.py
Package     : providers
Description : Google Gemini AI Provider

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from google import genai

from config.logger import get_logger
from providers.base_provider import BaseProvider

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Gemini Provider
###############################################################################


class GeminiProvider(BaseProvider):
    """
    Google Gemini Provider.

    Supports:

    - Text Generation
    - Chat Completion
    - Embeddings
    - Model Switching
    - Connection Testing
    """

    DEFAULT_MODEL = "gemini-2.5-flash"

    ###########################################################################

    def __init__(
        self,
        model: str | None = None,
    ) -> None:

        super().__init__(
            name="gemini",
            model=model or self.DEFAULT_MODEL,
        )

        load_dotenv()

        self._api_key = os.getenv(
            "GEMINI_API_KEY",
        )

        if not self._api_key:

            raise RuntimeError(
                "GEMINI_API_KEY not found in environment."
            )

        self._client: genai.Client | None = None

    ###########################################################################

    def initialize(
        self,
    ) -> None:
        """
        Initialize Gemini client.
        """

        super().initialize()

        self._client = genai.Client(
            api_key=self._api_key,
        )

        logger.info(
            "Gemini Provider initialized."
        )

    ###########################################################################

    @property
    def client(
        self,
    ) -> genai.Client:

        if self._client is None:

            raise RuntimeError(
                "Gemini Provider not initialized."
            )

        return self._client

    ###########################################################################

    def test_connection(
        self,
    ) -> bool:
        """
        Test Gemini connectivity.
        """

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents="Reply with OK",
            )

            return bool(
                response.text,
            )

        except Exception:

            logger.exception(
                "Gemini connection failed."
            )

            return False
            ###########################################################################
    # Text Generation
    ###########################################################################

    def generate(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        """
        Generate text using Gemini.
        """

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )

            if hasattr(response, "text") and response.text:

                return response.text

            return ""

        except Exception as exc:

            logger.exception(
                "Gemini generation failed: %s",
                exc,
            )

            raise

    ###########################################################################
    # Chat
    ###########################################################################

    def chat(
        self,
        messages: list[dict[str, str]],
        **kwargs: Any,
    ) -> str:
        """
        Execute chat completion.
        """

        prompt = "\n".join(
            f"{item['role']}: {item['content']}"
            for item in messages
        )

        return self.generate(
            prompt,
            **kwargs,
        )

    ###########################################################################
    # Embeddings
    ###########################################################################

    def embeddings(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate embeddings.
        """

        try:

            response = self.client.models.embed_content(
                model="gemini-embedding-001",
                contents=text,
            )

            if hasattr(response, "embeddings"):

                if response.embeddings:

                    return response.embeddings[0].values

            return []

        except Exception as exc:

            logger.exception(
                "Gemini embedding failed: %s",
                exc,
            )

            raise

    ###########################################################################
    # Model Management
    ###########################################################################

    def available_models(
        self,
    ) -> list[str]:
        """
        Return available Gemini models.
        """

        try:

            return sorted(
                model.name
                for model in self.client.models.list()
            )

        except Exception:

            logger.exception(
                "Unable to retrieve Gemini models."
            )

            return []
            ###########################################################################
    # Health Check
    ###########################################################################

    def healthy(
        self,
    ) -> bool:
        """
        Return provider health.
        """

        if not self.enabled:

            return False

        return self.test_connection()

    ###########################################################################
    # Lifecycle
    ###########################################################################

    def shutdown(
        self,
    ) -> None:
        """
        Shutdown provider.
        """

        logger.info(
            "Shutting down Gemini Provider."
        )

        self._client = None

        super().shutdown()

    ###########################################################################
    # Provider Information
    ###########################################################################

    def metadata(
        self,
    ) -> dict[str, Any]:
        """
        Return provider metadata.
        """

        data = super().metadata()

        data.update(
            {
                "vendor": "Google",
                "provider": "Gemini",
                "sdk": "google-genai",
                "default_model": self.DEFAULT_MODEL,
                "current_model": self.model,
                "connected": self.test_connection(),
            }
        )

        return data

    ###########################################################################
    # Model Switching
    ###########################################################################

    def switch_model(
        self,
        model: str,
    ) -> None:
        """
        Switch active Gemini model.
        """

        logger.info(
            "Switching Gemini model to %s",
            model,
        )

        self.set_model(model)

    ###########################################################################
    # String Representation
    ###########################################################################

    def __str__(
        self,
    ) -> str:

        return (
            f"GeminiProvider("
            f"model='{self.model}')"
        )


###############################################################################
# Exports
###############################################################################

__all__ = [
    "GeminiProvider",
]