"""
==============================================================================
GEETA AI Engine

File        : model_manager.py
Package     : providers
Description : AI Model Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import RLock
from typing import Any

from config.logger import get_logger

logger = get_logger(__name__)

###############################################################################
# Model Information
###############################################################################


@dataclass(slots=True)
class ModelInfo:
    """
    AI model metadata.
    """

    name: str

    provider: str

    context_window: int = 8192

    supports_chat: bool = True

    supports_embeddings: bool = False

    supports_streaming: bool = False

    supports_functions: bool = False

    supports_vision: bool = False

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

###############################################################################
# Model Manager
###############################################################################


class ModelManager:
    """
    Central AI model manager.

    Responsibilities
    ----------------
    • Model registration
    • Model lookup
    • Default model selection
    • Capability queries
    """

    def __init__(self) -> None:

        self._lock = RLock()

        self._models: dict[str, ModelInfo] = {}

        self._default_model: str | None = None

        logger.info(
            "Model Manager initialized."
        )
        ###############################################################################
# Model Registration
###############################################################################

    def register(
        self,
        model: ModelInfo,
    ) -> None:
        """
        Register a model.
        """

        with self._lock:

            self._models[
                model.name
            ] = model

            if self._default_model is None:

                self._default_model = model.name

            logger.info(
                "Registered model: %s",
                model.name,
            )

    ###########################################################################

    def unregister(
        self,
        model_name: str,
    ) -> None:
        """
        Remove model.
        """

        with self._lock:

            self._models.pop(
                model_name,
                None,
            )

            logger.info(
                "Removed model: %s",
                model_name,
            )

###############################################################################
# Queries
###############################################################################

    def exists(
        self,
        model_name: str,
    ) -> bool:

        return model_name in self._models

    ###########################################################################

    def get(
        self,
        model_name: str,
    ) -> ModelInfo:

        return self._models[
            model_name
        ]

    ###########################################################################

    def models(
        self,
    ) -> list[str]:

        return sorted(
            self._models.keys()
        )

###############################################################################
# Default Model
###############################################################################

    def set_default(
        self,
        model_name: str,
    ) -> None:
        """
        Set default model.
        """

        if model_name not in self._models:

            raise ValueError(
                f"Unknown model: {model_name}"
            )

        self._default_model = model_name

        logger.info(
            "Default model changed to %s",
            model_name,
        )

    ###########################################################################

    @property
    def default_model(
        self,
    ) -> ModelInfo | None:
        """
        Return default model.
        """

        if self._default_model is None:

            return None

        return self._models[
            self._default_model
        ]

###############################################################################
# Capabilities
###############################################################################

    def supports_chat(
        self,
        model_name: str,
    ) -> bool:

        return self.get(
            model_name,
        ).supports_chat

    ###########################################################################

    def supports_embeddings(
        self,
        model_name: str,
    ) -> bool:

        return self.get(
            model_name,
        ).supports_embeddings

    ###########################################################################

    def supports_streaming(
        self,
        model_name: str,
    ) -> bool:

        return self.get(
            model_name,
        ).supports_streaming

    ###########################################################################

    def supports_vision(
        self,
        model_name: str,
    ) -> bool:

        return self.get(
            model_name,
        ).supports_vision
        ###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, Any]:
        """
        Return Model Manager diagnostics.
        """

        return {
            "model_count": len(self._models),
            "default_model": (
                self._default_model
            ),
            "models": self.models(),
        }

###############################################################################
# Built-in Models
###############################################################################

    def initialize(
        self,
    ) -> None:
        """
        Register built-in models.
        """

        self.register(
            ModelInfo(
                name="gemini-2.5-flash",
                provider="gemini",
                context_window=1048576,
                supports_chat=True,
                supports_embeddings=True,
                supports_streaming=True,
                supports_functions=True,
                supports_vision=True,
            )
        )

        self.register(
            ModelInfo(
                name="gpt-5.5",
                provider="openai",
                context_window=400000,
                supports_chat=True,
                supports_embeddings=True,
                supports_streaming=True,
                supports_functions=True,
                supports_vision=True,
            )
        )

        self.register(
            ModelInfo(
                name="claude-sonnet-4",
                provider="claude",
                context_window=200000,
                supports_chat=True,
                supports_streaming=True,
                supports_functions=True,
            )
        )

        self.register(
            ModelInfo(
                name="openrouter-auto",
                provider="openrouter",
                supports_chat=True,
                supports_streaming=True,
            )
        )

        self.register(
            ModelInfo(
                name="llama3",
                provider="ollama",
                supports_chat=True,
                supports_streaming=True,
            )
        )

        logger.info(
            "Initialized %d AI models.",
            len(self._models),
        )

###############################################################################
# Shutdown
###############################################################################

    def shutdown(
        self,
    ) -> None:
        """
        Shutdown Model Manager.
        """

        with self._lock:

            self._models.clear()

            self._default_model = None

        logger.info(
            "Model Manager shut down."
        )

###############################################################################
# Global Manager
###############################################################################

model_manager = ModelManager()

model_manager.initialize()

###############################################################################
# Helper Functions
###############################################################################

def available_models() -> list[str]:
    """
    Return available models.
    """

    return model_manager.models()


def default_model() -> ModelInfo | None:
    """
    Return default model.
    """

    return model_manager.default_model


def model_diagnostics() -> dict[str, Any]:
    """
    Return diagnostics.
    """

    return model_manager.diagnostics()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "ModelInfo",
    "ModelManager",
    "model_manager",
    "available_models",
    "default_model",
    "model_diagnostics",
]
