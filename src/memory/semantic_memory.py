"""
==============================================================================
GEETA AI Engine

File        : semantic_memory.py
Package     : memory
Description : Semantic Memory

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Any

from config.logger import get_logger
from memory.vector_memory import VectorMemory

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Semantic Memory
###############################################################################


class SemanticMemory(VectorMemory):
    """
    Semantic project memory.

    Responsibilities:

    - Semantic chunks
    - Context ranking
    - Embedding indexing
    - Relevant retrieval
    - RAG context
    - AI knowledge retrieval
    """

    def __init__(self) -> None:

        super().__init__()

        self._name = "semantic_memory"

    ###########################################################################

    def add_document(
        self,
        document_id: str,
        text: str,
        embedding: list[float],
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Store semantic document.
        """

        self.store(
            document_id,
            {
                "text": text,
                "embedding": embedding,
                "metadata": metadata or {},
            },
        )

        logger.info(
            "Indexed semantic document: %s",
            document_id,
        )

    ###########################################################################

    def get_document(
        self,
        document_id: str,
    ) -> dict[str, Any] | None:
        """
        Retrieve indexed document.
        """

        return self.retrieve(
            document_id,
        )

    ###########################################################################

    def remove_document(
        self,
        document_id: str,
    ) -> None:
        """
        Remove indexed document.
        """

        self.delete(
            document_id,
        )

    def remove_file(
        self,
        file: str,
    ) -> None:
        """Remove all semantic chunks associated with a workspace file."""

        for document_id, document in list(self._vectors.items()):

            if document.get("metadata", {}).get("file") == file:

                self.delete(document_id)

    ###########################################################################

    def search_text(
        self,
        embedding: list[float],
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Search semantic documents.
        """

        return self.search(
            query_embedding=embedding,
            limit=limit,
        )
###############################################################################
# Context Ranking
###############################################################################

    def rank_context(
        self,
        embedding: list[float],
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Rank semantic context by relevance.

        The default implementation delegates to the
        underlying vector search. Subclasses may override
        this with custom scoring strategies.
        """

        return self.search(
            query_embedding=embedding,
            limit=limit,
        )

###############################################################################
# RAG Context Builder
###############################################################################

    def build_context(
        self,
        embedding: list[float],
        limit: int = 5,
    ) -> str:
        """
        Build context for Retrieval-Augmented Generation.
        """

        documents = self.rank_context(
            embedding=embedding,
            limit=limit,
        )

        return "\n\n".join(
            document.get(
                "text",
                "",
            )
            for document in documents
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return semantic memory statistics.
        """

        data = super().statistics()

        data.update(
            {
                "documents": len(
                    self._vectors
                ),
                "memory_type": "semantic",
            }
        )

        return data

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return semantic memory report.
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
    "SemanticMemory",
]
