"""
==============================================================================
GEETA AI Engine

File        : base_memory.py
Package     : memory
Description : Base Memory Interface

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Base Memory
###############################################################################


class BaseMemory(ABC):
    """
    Base class for every GEETA AI memory implementation.

    Examples:

    - Conversation Memory
    - Project Memory
    - Symbol Memory
    - Semantic Memory
    - Vector Memory
    - Session Memory
    """

    def __init__(
        self,
        name: str,
    ) -> None:

        self._name = name

        self._enabled = True

        self._created_at = datetime.utcnow()

        logger.info(
            "Initialized memory: %s",
            self._name,
        )

    ###########################################################################

    @property
    def name(self) -> str:
        """
        Memory name.
        """

        return self._name

    ###########################################################################

    @property
    def enabled(self) -> bool:
        """
        Return memory state.
        """

        return self._enabled

    ###########################################################################

    @property
    def created_at(self) -> datetime:
        """
        Return creation timestamp.
        """

        return self._created_at

    ###########################################################################

    def enable(self) -> None:
        """
        Enable memory.
        """

        self._enabled = True

    ###########################################################################

    def disable(self) -> None:
        """
        Disable memory.
        """

        self._enabled = False

    ###########################################################################

    @abstractmethod
    def store(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store memory item.
        """

    ###########################################################################

    @abstractmethod
    def retrieve(
        self,
        key: str,
    ) -> Any:
        """
        Retrieve memory item.
        """

    ###########################################################################

    @abstractmethod
    def delete(
        self,
        key: str,
    ) -> None:
        """
        Delete memory item.
        """

    ###########################################################################

    @abstractmethod
    def clear(self) -> None:
        """
        Clear memory.
        """
###############################################################################
# Metadata
###############################################################################

    def metadata(self) -> dict[str, Any]:
        """
        Return memory metadata.
        """

        return {
            "name": self.name,
            "enabled": self.enabled,
            "created_at": self.created_at.isoformat(),
        }

###############################################################################
# Statistics
###############################################################################

    def statistics(self) -> dict[str, Any]:
        """
        Return memory statistics.

        Override in subclasses for detailed metrics.
        """

        return {
            "memory": self.name,
            "enabled": self.enabled,
        }

###############################################################################
# Health Check
###############################################################################

    def healthy(self) -> bool:
        """
        Return memory health.
        """

        return self.enabled

###############################################################################
# Lifecycle
###############################################################################

    def initialize(self) -> None:
        """
        Initialize memory resources.
        """

        logger.info(
            "Initializing memory: %s",
            self.name,
        )

    ###########################################################################

    def shutdown(self) -> None:
        """
        Shutdown memory resources.
        """

        logger.info(
            "Shutting down memory: %s",
            self.name,
        )

###############################################################################
# Representation
###############################################################################

    def __repr__(self) -> str:
        """
        Developer-friendly representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}', "
            f"enabled={self.enabled})"
        )

###############################################################################
# Exports
###############################################################################

__all__ = [
    "BaseMemory",
]