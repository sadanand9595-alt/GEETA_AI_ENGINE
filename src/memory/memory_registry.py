"""
==============================================================================
GEETA AI Engine

File        : memory_registry.py
Package     : memory
Description : Memory Registry

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Type

from config.logger import get_logger

from memory.base_memory import BaseMemory
from memory.memory_manager import memory_manager

from memory.conversation_memory import ConversationMemory
from memory.project_memory import ProjectMemory
from memory.session_memory import SessionMemory
from memory.vector_memory import VectorMemory
from memory.semantic_memory import SemanticMemory
from memory.symbol_memory import SymbolMemory

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Memory Registry
###############################################################################


class MemoryRegistry:
    """
    Central registry for every memory implementation.
    """

    def __init__(self) -> None:

        self._registry: dict[
            str,
            Type[BaseMemory],
        ] = {}

    ###########################################################################

    def register(
        self,
        memory_name: str,
        memory_class: Type[BaseMemory],
    ) -> None:
        """
        Register memory class.
        """

        self._registry[
            memory_name
        ] = memory_class

        logger.info(
            "Registered memory class: %s",
            memory_name,
        )

    ###########################################################################

    def exists(
        self,
        memory_name: str,
    ) -> bool:
        """
        Check whether memory exists.
        """

        return memory_name in self._registry

    ###########################################################################

    def create(
        self,
        memory_name: str,
    ) -> BaseMemory:
        """
        Create memory instance.
        """

        memory_class = self._registry[
            memory_name
        ]

        return memory_class()

    ###########################################################################

    def register_instance(
        self,
        memory_name: str,
    ) -> None:
        """
        Create and register memory instance.
        """

        memory = self.create(
            memory_name,
        )

        if not memory_manager.exists(
            memory.name,
        ):

            memory_manager.register(
                memory,
            )
###############################################################################
# Registry Queries
###############################################################################

    def memories(
        self,
    ) -> list[str]:
        """
        Return registered memory names.
        """

        return sorted(
            self._registry.keys()
        )

    ###########################################################################

    def count(
        self,
    ) -> int:
        """
        Return registered memory count.
        """

        return len(
            self._registry
        )

###############################################################################
# Initialization
###############################################################################

    def initialize(
        self,
    ) -> None:
        """
        Register built-in memory implementations.
        """

        self.register(
            "conversation_memory",
            ConversationMemory,
        )

        self.register(
            "project_memory",
            ProjectMemory,
        )

        self.register(
            "session_memory",
            SessionMemory,
        )

        self.register(
            "vector_memory",
            VectorMemory,
        )

        self.register(
            "semantic_memory",
            SemanticMemory,
        )

        self.register(
            "symbol_memory",
            SymbolMemory,
        )

        logger.info(
            "Initialized %d memory classes.",
            self.count(),
        )

    ###########################################################################

    def create_all(
        self,
    ) -> None:
        """
        Instantiate and register every memory.
        """

        for memory_name in self.memories():

            self.register_instance(
                memory_name,
            )

###############################################################################
# Global Registry
###############################################################################

memory_registry = MemoryRegistry()

###############################################################################
# Helper Functions
###############################################################################


def initialize_memories() -> None:
    """
    Initialize and register all memories.
    """

    memory_registry.initialize()

    memory_registry.create_all()


def available_memories() -> list[str]:
    """
    Return available memory implementations.
    """

    return memory_registry.memories()


###############################################################################
# Exports
###############################################################################

__all__ = [
    "MemoryRegistry",
    "memory_registry",
    "initialize_memories",
    "available_memories",
]