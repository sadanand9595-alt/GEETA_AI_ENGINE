"""
==============================================================================
GEETA AI Engine

File        : semantic_indexer.py
Package     : workspace
Description : Semantic Indexer

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from config.logger import get_logger

from memory.semantic_memory import SemanticMemory
from providers.provider_manager import provider_manager
from workspace.workspace_manager import workspace_manager

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Semantic Indexer
###############################################################################


class SemanticIndexer:
    """
    Builds semantic project index.

    Responsibilities

    - Chunk source files
    - Generate embeddings
    - Store semantic documents
    - Incremental indexing
    - RAG support
    """

    def __init__(self) -> None:

        self._memory = SemanticMemory()

        logger.info(
            "Semantic Indexer initialized."
        )

    ###########################################################################

    def build(
        self,
    ) -> None:
        """
        Build semantic index.
        """

        logger.info(
            "Building semantic index..."
        )

        self._memory.clear()

        for file in workspace_manager.scan_files(
            "*.py",
        ):

            self.index_file(
                file,
            )

        logger.info(
            "Semantic indexing completed."
        )

    ###########################################################################

    def index_file(
        self,
        file: Path,
    ) -> None:
        """
        Index a single file.
        """

        try:

            text = file.read_text(
                encoding="utf-8",
            )

            chunks = self.chunk_text(
                text,
            )

            provider = (
                provider_manager.active_provider()
            )

            for index, chunk in enumerate(
                chunks,
            ):

                embedding = provider.embeddings(
                    chunk,
                )

                self._memory.add_document(
                    document_id=(
                        f"{file}:{index}"
                    ),
                    text=chunk,
                    embedding=embedding,
                    metadata={
                        "file": str(file),
                        "chunk": index,
                    },
                )

        except Exception:

            logger.exception(
                "Semantic indexing failed: %s",
                file,
            )

    ###########################################################################

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 1000,
    ) -> list[str]:
        """
        Split text into chunks.
        """

        return [
            text[i:i + chunk_size]
            for i in range(
                0,
                len(text),
                chunk_size,
            )
        ]
###############################################################################
# Semantic Search
###############################################################################

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Perform semantic search.
        """

        provider = provider_manager.active_provider()

        embedding = provider.embeddings(
            query,
        )

        return self._memory.search_text(
            embedding=embedding,
            limit=limit,
        )

###############################################################################
# Incremental Indexing
###############################################################################

    def reindex_file(
        self,
        file: Path,
    ) -> None:
        """
        Re-index a single source file.
        """

        logger.info(
            "Re-indexing %s",
            file,
        )

        self.index_file(
            file,
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return semantic indexing statistics.
        """

        return self._memory.statistics()

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return semantic indexing report.
        """

        return {
            "statistics": self.statistics(),
            "memory": self._memory.report(),
        }

###############################################################################
# Global Semantic Indexer
###############################################################################

semantic_indexer = SemanticIndexer()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "SemanticIndexer",
    "semantic_indexer",
]