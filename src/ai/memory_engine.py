"""
==============================================================================
GEETA AI IDE

File        : memory_engine.py
Package     : ai
Description : Enterprise AI Memory Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Memory Type
###############################################################################


class MemoryType(str, Enum):

    PROJECT = "project"

    CONVERSATION = "conversation"

    CODE = "code"

    DEBUG = "debug"

    KNOWLEDGE = "knowledge"

###############################################################################
# Memory Entry
###############################################################################


@dataclass(slots=True)
class MemoryEntry:
    """
    AI Memory Entry.
    """

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    memory_type: MemoryType = (
        MemoryType.PROJECT
    )

    title: str = ""

    content: str = ""

    tags: list[str] = field(
        default_factory=list
    )

    score: float = 0.0

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

###############################################################################
# Memory Engine
###############################################################################


class MemoryEngine:
    """
    Enterprise AI Memory Engine.

    Responsibilities

    - Project memory
    - Conversation memory
    - Semantic retrieval
    - Persistent knowledge
    - Memory ranking
    """

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._memory: dict[
            str,
            MemoryEntry
        ] = {}

        logger.info(
            "Memory Engine initialized."
        )

###############################################################################
# Store
###############################################################################

    def store(
        self,
        memory: MemoryEntry,
    ) -> None:
        """
        Store memory.
        """

        self._memory[
            memory.id
        ] = memory

###############################################################################
# Lookup
###############################################################################

    def memory(
        self,
        memory_id: str,
    ) -> MemoryEntry | None:
        """
        Lookup memory.
        """

        return self._memory.get(
            memory_id
        )

###############################################################################
# Search
###############################################################################

    def search(
        self,
        keyword: str,
    ) -> list[MemoryEntry]:
        """
        Search memory.
        """

        keyword = keyword.lower()

        return [
            memory
            for memory
            in self._memory.values()
            if (
                keyword in memory.title.lower()
                or keyword
                in memory.content.lower()
            )
        ]
###############################################################################
# Rank Memories
###############################################################################

    def rank(
        self,
        entries: list[MemoryEntry],
    ) -> list[MemoryEntry]:
        """
        Rank memories by relevance score.
        """

        return sorted(
            entries,
            key=lambda entry: entry.score,
            reverse=True,
        )

###############################################################################
# Retrieve Context
###############################################################################

    def retrieve_context(
        self,
        keyword: str,
        limit: int = 10,
    ) -> list[MemoryEntry]:
        """
        Retrieve ranked context memories.
        """

        matches = self.search(
            keyword,
        )

        return self.rank(
            matches,
        )[:limit]

###############################################################################
# Delete Memory
###############################################################################

    def delete(
        self,
        memory_id: str,
    ) -> bool:
        """
        Delete a memory entry.
        """

        if memory_id not in self._memory:

            return False

        del self._memory[
            memory_id
        ]

        return True

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return memory statistics.
        """

        return {
            "total_memories": len(
                self._memory
            ),
            "project": sum(
                1
                for memory
                in self._memory.values()
                if memory.memory_type
                == MemoryType.PROJECT
            ),
            "conversation": sum(
                1
                for memory
                in self._memory.values()
                if memory.memory_type
                == MemoryType.CONVERSATION
            ),
            "code": sum(
                1
                for memory
                in self._memory.values()
                if memory.memory_type
                == MemoryType.CODE
            ),
            "debug": sum(
                1
                for memory
                in self._memory.values()
                if memory.memory_type
                == MemoryType.DEBUG
            ),
            "knowledge": sum(
                1
                for memory
                in self._memory.values()
                if memory.memory_type
                == MemoryType.KNOWLEDGE
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return memory engine report.
        """

        return {
            "statistics": self.statistics(),
            "entries": [
                {
                    "id": memory.id,
                    "title": memory.title,
                    "type": memory.memory_type.value,
                    "score": memory.score,
                    "tags": memory.tags,
                }
                for memory
                in self._memory.values()
            ],
        }

###############################################################################
# Global Memory Engine
###############################################################################

memory_engine: (
    MemoryEngine | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "MemoryType",
    "MemoryEntry",
    "MemoryEngine",
    "memory_engine",
]