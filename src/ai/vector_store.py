"""
==============================================================================
GEETA AI Engine

File        : vector_store.py
Package     : ai
Description : Vector Store Abstraction

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from threading import RLock
from typing import Any

from config.logger import get_logger
from core.service import BaseService

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Vector Document
###############################################################################


@dataclass(slots=True)
class VectorDocument:
    """
    Document stored in a vector database.
    """

    id: str

    text: str

    vector: list[float]

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

###############################################################################
# Search Result
###############################################################################


@dataclass(slots=True)
class SearchResult:
    """
    Vector search result.
    """

    document: VectorDocument

    score: float

###############################################################################
# Base Vector Store
###############################################################################


class BaseVectorStore(
    BaseService,
    ABC,
):
    """
    Abstract Vector Store.
    """

    def __init__(
        self,
        name: str,
    ) -> None:

        super().__init__(name)

        self._lock = RLock()

    ###########################################################################

    @abstractmethod
    def add(
        self,
        document: VectorDocument,
    ) -> None:
        """
        Add a document.
        """

    ###########################################################################

    @abstractmethod
    def search(
        self,
        vector: list[float],
        limit: int = 10,
    ) -> list[SearchResult]:
        """
        Search similar vectors.
        """

    ###########################################################################

    @abstractmethod
    def remove(
        self,
        document_id: str,
    ) -> None:
        """
        Remove a document.
        """

    ###########################################################################

    @abstractmethod
    def clear(
        self,
    ) -> None:
        """
        Remove every document.
        """
        ###############################################################################
# In-Memory Vector Store
###############################################################################


class InMemoryVectorStore(BaseVectorStore):
    """
    Default in-memory vector store.

    Useful for:

    - Development
    - Testing
    - Small projects
    """

    def __init__(self) -> None:

        super().__init__(
            "InMemoryVectorStore",
        )

        self._documents: dict[
            str,
            VectorDocument,
        ] = {}

        logger.info(
            "InMemoryVectorStore initialized."
        )

    ###########################################################################

    def add(
        self,
        document: VectorDocument,
    ) -> None:
        """
        Add or replace a document.
        """

        with self._lock:

            self._documents[
                document.id
            ] = document

    ###########################################################################

    def remove(
        self,
        document_id: str,
    ) -> None:
        """
        Remove a document.
        """

        with self._lock:

            self._documents.pop(
                document_id,
                None,
            )

    ###########################################################################

    def search(
        self,
        vector: list[float],
        limit: int = 10,
    ) -> list[SearchResult]:
        """
        Simple vector search.

        NOTE:
        Placeholder implementation.
        Will be replaced with cosine similarity
        in future versions.
        """

        results: list[
            SearchResult
        ] = []

        for document in self._documents.values():

            score = 0.0

            if (
                len(vector)
                == len(document.vector)
                and vector
            ):

                score = sum(
                    a * b
                    for a, b in zip(
                        vector,
                        document.vector,
                    )
                )

            results.append(
                SearchResult(
                    document=document,
                    score=score,
                )
            )

        results.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        return results[:limit]

    ###########################################################################

    def clear(
        self,
    ) -> None:
        """
        Remove every document.
        """

        with self._lock:

            self._documents.clear()

###############################################################################
# Queries
###############################################################################

    def count(
        self,
    ) -> int:
        """
        Return number of documents.
        """

        return len(
            self._documents,
        )

    ###########################################################################

    def exists(
        self,
        document_id: str,
    ) -> bool:
        """
        Check whether a document exists.
        """

        return (
            document_id
            in self._documents
        )
        ###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, Any]:
        """
        Return vector store diagnostics.
        """

        return {
            "service": self.name,
            "healthy": self.healthy(),
            "documents": self.count(),
            "initialized": self.initialized,
            "enabled": self.enabled,
        }

###############################################################################
# Export
###############################################################################

    def documents(
        self,
    ) -> list[VectorDocument]:
        """
        Return every stored document.
        """

        return list(
            self._documents.values()
        )

###############################################################################
# Shutdown
###############################################################################

    def shutdown(
        self,
    ) -> None:
        """
        Shutdown vector store.
        """

        self.clear()

        super().shutdown()

###############################################################################
# Global Store
###############################################################################

vector_store = InMemoryVectorStore()

###############################################################################
# Helper Functions
###############################################################################

def add_document(
    document: VectorDocument,
) -> None:
    """
    Add document.
    """

    vector_store.add(
        document,
    )


def search_documents(
    vector: list[float],
    limit: int = 10,
) -> list[SearchResult]:
    """
    Search documents.
    """

    return vector_store.search(
        vector,
        limit,
    )


def clear_documents(
) -> None:
    """
    Clear store.
    """

    vector_store.clear()


def vector_store_diagnostics(
) -> dict[str, Any]:
    """
    Return diagnostics.
    """

    return vector_store.diagnostics()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "VectorDocument",
    "SearchResult",
    "BaseVectorStore",
    "InMemoryVectorStore",
    "vector_store",
    "add_document",
    "search_documents",
    "clear_documents",
    "vector_store_diagnostics",
]