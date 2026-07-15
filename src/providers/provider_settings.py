"""
==============================================================================
GEETA AI Engine

File        : provider_settings.py
Package     : providers
Description : AI Provider Settings

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Provider Settings
###############################################################################


@dataclass(slots=True)
class ProviderSettings:
    """
    Provider configuration.

    Used by:

    - ProviderFactory
    - ProviderManager
    - Settings UI
    - AI Chat
    """

    ###########################################################################
    # Provider
    ###########################################################################

    provider: str = "gemini"

    model: str = "gemini-2.5-flash"

    ###########################################################################
    # Generation
    ###########################################################################

    temperature: float = 0.7

    max_tokens: int = 8192

    top_p: float = 0.95

    top_k: int = 40

    stream: bool = False

    ###########################################################################
    # Timeouts
    ###########################################################################

    timeout: int = 120

    retries: int = 3

    ###########################################################################
    # Embeddings
    ###########################################################################

    embedding_model: str = "gemini-embedding-001"

    ###########################################################################
    # API
    ###########################################################################

    api_key_env: str = "GEMINI_API_KEY"

    base_url: str | None = None

    ###########################################################################
    # Extra
    ###########################################################################

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

###############################################################################
# Settings Manager
###############################################################################


class ProviderSettingsManager:

    """
    Manage Provider Settings.
    """

    def __init__(
        self,
    ) -> None:

        self._settings = ProviderSettings()

        logger.info(
            "Provider Settings initialized."
        )

    ###########################################################################

    @property
    def settings(
        self,
    ) -> ProviderSettings:

        return self._settings
        ###############################################################################
# Load / Save
###############################################################################

    def load(
        self,
        path: str | Path,
    ) -> None:
        """
        Load settings from JSON file.
        """

        import json

        path = Path(path)

        if not path.exists():

            logger.warning(
                "Settings file not found: %s",
                path,
            )

            return

        data = json.loads(
            path.read_text(
                encoding="utf-8",
            )
        )

        self._settings = ProviderSettings(
            **data,
        )

        logger.info(
            "Loaded provider settings."
        )

    ###########################################################################

    def save(
        self,
        path: str | Path,
    ) -> None:
        """
        Save settings.
        """

        import json

        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            json.dumps(
                self._settings.__dict__,
                indent=4,
            ),
            encoding="utf-8",
        )

        logger.info(
            "Saved provider settings."
        )

###############################################################################
# Provider
###############################################################################

    def set_provider(
        self,
        provider: str,
    ) -> None:

        self._settings.provider = provider

    ###########################################################################

    def provider(
        self,
    ) -> str:

        return self._settings.provider

###############################################################################
# Model
###############################################################################

    def set_model(
        self,
        model: str,
    ) -> None:

        self._settings.model = model

    ###########################################################################

    def model(
        self,
    ) -> str:

        return self._settings.model

###############################################################################
# Temperature
###############################################################################

    def set_temperature(
        self,
        value: float,
    ) -> None:

        if value < 0:

            value = 0

        if value > 2:

            value = 2

        self._settings.temperature = value

    ###########################################################################

    def temperature(
        self,
    ) -> float:

        return self._settings.temperature

###############################################################################
# Max Tokens
###############################################################################

    def set_max_tokens(
        self,
        tokens: int,
    ) -> None:

        self._settings.max_tokens = max(
            1,
            tokens,
        )

    ###########################################################################

    def max_tokens(
        self,
    ) -> int:

        return self._settings.max_tokens
        ###############################################################################
# Streaming
###############################################################################

    def set_stream(
        self,
        enabled: bool,
    ) -> None:
        """
        Enable or disable streaming.
        """

        self._settings.stream = enabled

    ###########################################################################

    def stream(
        self,
    ) -> bool:

        return self._settings.stream

###############################################################################
# Timeout
###############################################################################

    def set_timeout(
        self,
        seconds: int,
    ) -> None:

        self._settings.timeout = max(
            1,
            seconds,
        )

    ###########################################################################

    def timeout(
        self,
    ) -> int:

        return self._settings.timeout

###############################################################################
# Retries
###############################################################################

    def set_retries(
        self,
        retries: int,
    ) -> None:

        self._settings.retries = max(
            0,
            retries,
        )

    ###########################################################################

    def retries(
        self,
    ) -> int:

        return self._settings.retries

###############################################################################
# Metadata
###############################################################################

    def metadata(
        self,
    ) -> dict[str, Any]:

        return dict(
            self._settings.metadata,
        )

###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, Any]:
        """
        Return current provider settings.
        """

        return {
            "provider": self.provider(),
            "model": self.model(),
            "temperature": self.temperature(),
            "max_tokens": self.max_tokens(),
            "stream": self.stream(),
            "timeout": self.timeout(),
            "retries": self.retries(),
            "embedding_model": (
                self._settings.embedding_model
            ),
            "api_key_env": (
                self._settings.api_key_env
            ),
        }

###############################################################################
# Global Manager
###############################################################################

provider_settings = ProviderSettingsManager()

###############################################################################
# Helper Functions
###############################################################################


def settings() -> ProviderSettings:
    """
    Return ProviderSettings instance.
    """

    return provider_settings.settings


def diagnostics() -> dict[str, Any]:
    """
    Return provider diagnostics.
    """

    return provider_settings.diagnostics()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "ProviderSettings",
    "ProviderSettingsManager",
    "provider_settings",
    "settings",
    "diagnostics",
]