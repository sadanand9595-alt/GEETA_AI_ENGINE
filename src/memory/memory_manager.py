"""
==============================================================================
GEETA AI Engine

File        : memory_manager.py
Package     : memory
Description : Memory Manager

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
# Memory Manager
###############################################################################


class MemoryManager:
    """
    Central manager for all memory implementations.

    Responsibilities:

    - Register memory modules
    - Store data
    - Retrieve data
    - Delete data
    - Synchronize memories
    - Lifecycle management
    """

    def __init__(self) -> None:

        self._memories: dict[str, BaseMemory] = {}

        logger.info(
            "Memory Manager initialized."
        )

    ###########################################################################

    def register(
        self,
        memory: BaseMemory,
    ) -> None:
        """
        Register a memory implementation.
        """

        if memory.name in self._memories:

            raise ValueError(
                f"Memory '{memory.name}' already exists."
            )

        memory.initialize()

        self._memories[memory.name] = memory

        logger.info(
            "Registered memory: %s",
            memory.name,
        )

    ###########################################################################

    def unregister(
        self,
        name: str,
    ) -> None:
        """
        Remove a memory implementation.
        """

        memory = self._memories.pop(
            name,
            None,
        )

        if memory is None:
            return

        memory.shutdown()

        logger.info(
            "Removed memory: %s",
            name,
        )

    ###########################################################################

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check whether memory exists.
        """

        return name in self._memories

    ###########################################################################

    def get(
        self,
        name: str,
    ) -> BaseMemory:
        """
        Return memory instance.
        """

        return self._memories[name]

    ###########################################################################

    def memories(
        self,
    ) -> list[str]:
        """
        Return registered memories.
        """

        return sorted(
            self._memories.keys()
        )
###############################################################################
# Memory Operations
###############################################################################

    def store(
        self,
        memory_name: str,
        key: str,
        value: Any,
    ) -> None:
        """
        Store a value in the specified memory.
        """

        self.get(
            memory_name,
        ).store(
            key,
            value,
        )

    ###########################################################################

    def retrieve(
        self,
        memory_name: str,
        key: str,
    ) -> Any:
        """
        Retrieve a value from the specified memory.
        """

        return self.get(
            memory_name,
        ).retrieve(
            key,
        )

    ###########################################################################

    def delete(
        self,
        memory_name: str,
        key: str,
    ) -> None:
        """
        Delete a value from the specified memory.
        """

        self.get(
            memory_name,
        ).delete(
            key,
        )

###############################################################################
# Management
###############################################################################

    def clear_all(self) -> None:
        """
        Clear every registered memory.
        """

        for memory in self._memories.values():

            memory.clear()

        logger.info(
            "All memories cleared."
        )

    ###########################################################################

    def shutdown_all(self) -> None:
        """
        Shutdown every registered memory.
        """

        for memory in self._memories.values():

            memory.shutdown()

        logger.info(
            "All memories shut down."
        )

    ###########################################################################

    def count(self) -> int:
        """
        Return number of registered memories.
        """

        return len(
            self._memories
        )

###############################################################################
# Global Manager
###############################################################################

memory_manager = MemoryManager()

###############################################################################
# Helper Functions
###############################################################################


def register_memory(
    memory: BaseMemory,
) -> None:
    """
    Register a memory implementation.
    """

    memory_manager.register(
        memory,
    )


def registered_memories() -> list[str]:
    """
    Return registered memory names.
    """

    return memory_manager.memories()


###############################################################################
# Exports
###############################################################################

__all__ = [
    "MemoryManager",
    "memory_manager",
    "register_memory",
    "registered_memories",
]