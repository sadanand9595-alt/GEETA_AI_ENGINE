"""
==============================================================================
GEETA AI Engine

File        : embedding_engine.py
Package     : ai
Description : Embedding Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import RLock
from typing import Any

from config.logger import get_logger

from core.service import BaseService
from providers.provider_manager import provider_manager

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Embedding Result
###############################################################################


@dataclass(slots=True)
class EmbeddingResult:
    """
    Embedding generation result.
    """

    text: str

    vector: list[float]

    provider: str

    model: str

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

###############################################################################
# Embedding Engine
###############################################################################


class EmbeddingEngine(BaseService):
    """
    Enterprise Embedding Engine.

    Features
    --------

    • Multi-provider embeddings
    • Model abstraction
    • Future vector database support
    • Batch embeddings
    • Thread safe
    """

    def __init__(self) -> None:

        super().__init__(
            "EmbeddingEngine",
        )

        self._lock = RLock()

        logger.info(
            "Embedding Engine initialized."
        )
        ###############################################################################
# Single Embedding
###############################################################################

    def embed(
        self,
        text: str,
        **kwargs: Any,
    ) -> EmbeddingResult:
        """
        Generate embedding for a single text.
        """

        provider = provider_manager.active_provider

        if provider is None:

            raise RuntimeError(
                "No active provider."
            )

        vector = provider.embeddings(
            text,
        )

        return EmbeddingResult(
            text=text,
            vector=vector,
            provider=provider.name,
            model=provider.model,
            metadata=kwargs,
        )

###############################################################################
# Batch Embeddings
###############################################################################

    def embed_batch(
        self,
        texts: list[str],
        **kwargs: Any,
    ) -> list[EmbeddingResult]:
        """
        Generate embeddings for multiple texts.
        """

        results: list[
            EmbeddingResult
        ] = []

        for text in texts:

            results.append(
                self.embed(
                    text,
                    **kwargs,
                )
            )

        logger.info(
            "Generated %d embeddings.",
            len(results),
        )

        return results

###############################################################################
# Validation
###############################################################################

    def validate(
        self,
        result: EmbeddingResult,
    ) -> bool:
        """
        Validate embedding result.
        """

        return (
            len(result.vector) > 0
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
        results: list[EmbeddingResult],
    ) -> dict[str, int]:
        """
        Return embedding statistics.
        """

        return {
            "count": len(results),
            "dimensions": (
                len(results[0].vector)
                if results
                else 0
            ),
        }

###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, Any]:
        """
        Return engine diagnostics.
        """

        provider = provider_manager.active_provider

        return {
            "service": self.name,
            "healthy": self.healthy(),
            "provider": (
                provider.name
                if provider
                else None
            ),
            "model": (
                provider.model
                if provider
                else None
            ),
        }
        ###############################################################################
# Cache Hooks
###############################################################################

    def clear_cache(
        self,
    ) -> None:
        """
        Clear embedding cache.

        Reserved for future implementations.
        """

        logger.info(
            "Embedding cache cleared."
        )

###############################################################################
# Vector Store Hook
###############################################################################

    def export(
        self,
        results: list[EmbeddingResult],
    ) -> list[EmbeddingResult]:
        """
        Export embeddings.

        Future versions will forward results to
        FAISS, Qdrant, ChromaDB, Milvus, PGVector,
        or other vector databases.
        """

        logger.info(
            "Exporting %d embeddings.",
            len(results),
        )

        return results

###############################################################################
# Shutdown
###############################################################################

    def shutdown(
        self,
    ) -> None:
        """
        Shutdown embedding engine.
        """

        self.clear_cache()

        super().shutdown()

###############################################################################
# Global Engine
###############################################################################

embedding_engine = EmbeddingEngine()

###############################################################################
# Helper Functions
###############################################################################


def generate_embedding(
    text: str,
    **kwargs: Any,
) -> EmbeddingResult:
    """
    Generate a single embedding.
    """

    return embedding_engine.embed(
        text,
        **kwargs,
    )


def generate_embeddings(
    texts: list[str],
    **kwargs: Any,
) -> list[EmbeddingResult]:
    """
    Generate multiple embeddings.
    """

    return embedding_engine.embed_batch(
        texts,
        **kwargs,
    )


def embedding_diagnostics(
) -> dict[str, Any]:
    """
    Return engine diagnostics.
    """

    return embedding_engine.diagnostics()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "EmbeddingResult",
    "EmbeddingEngine",
    "embedding_engine",
    "generate_embedding",
    "generate_embeddings",
    "embedding_diagnostics",
]