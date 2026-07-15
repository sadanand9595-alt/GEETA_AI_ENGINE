"""
==============================================================================
GEETA AI Engine

File        : vector_memory.py
Package     : memory
Description : Vector Memory

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Any

from config.logger import get_logger
from memory.base_memory import BaseMemory

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Vector Memory
###############################################################################


class VectorMemory(BaseMemory):
    """
    Semantic vector memory.

    Responsibilities:

    - Embedding storage
    - Similarity search
    - Semantic retrieval
    - RAG support
    - Long-term knowledge
    - Cross-file search
    """

    def __init__(
        self,
    ) -> None:

        super().__init__(
            name="vector_memory",
        )

        self._vectors: dict[
            str,
            dict[str, Any],
        ] = {}

    ###########################################################################

    def store(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store vector document.
        """

        self._vectors[key] = value

    ###########################################################################

    def retrieve(
        self,
        key: str,
    ) -> Any:
        """
        Retrieve stored document.
        """

        return self._vectors.get(
            key,
        )

    ###########################################################################

    def delete(
        self,
        key: str,
    ) -> None:
        """
        Delete vector document.
        """

        self._vectors.pop(
            key,
            None,
        )

    ###########################################################################

    def clear(
        self,
    ) -> None:
        """
        Clear vector memory.
        """

        self._vectors.clear()

        logger.info(
            "Vector memory cleared."
        )

    ###########################################################################

    def keys(
        self,
    ) -> list[str]:
        """
        Return stored vector ids.
        """

        return sorted(
            self._vectors.keys()
        )
###############################################################################
# Semantic Search
###############################################################################

    def search(
        self,
        query_embedding: list[float],
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Perform semantic similarity search.

        This base implementation simply returns the first
        stored entries. Concrete implementations (Qdrant,
        FAISS, ChromaDB, etc.) should override this method.
        """

        return list(
            self._vectors.values()
        )[:limit]

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return vector memory statistics.
        """

        data = super().statistics()

        data.update(
            {
                "documents": len(
                    self._vectors
                ),
                "vector_ids": len(
                    self.keys()
                ),
            }
        )

        return data

###############################################################################
# RAG Helpers
###############################################################################

    def retrieve_context(
        self,
        query_embedding: list[float],
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Retrieve context for Retrieval-Augmented Generation.
        """

        return self.search(
            query_embedding=query_embedding,
            limit=limit,
        )

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return vector memory report.
        """

        return {
            "metadata": self.metadata(),
            "statistics": self.statistics(),
            "documents": self.keys(),
        }

###############################################################################
# Exports
###############################################################################

__all__ = [
    "VectorMemory",
]