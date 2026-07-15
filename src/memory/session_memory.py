"""
==============================================================================
GEETA AI Engine

File        : session_memory.py
Package     : memory
Description : Session Memory

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
# Session Memory
###############################################################################


class SessionMemory(BaseMemory):
    """
    Stores temporary runtime information for the
    current GEETA AI IDE session.

    Responsibilities:

    - Active workspace
    - Open files
    - Active editor
    - Selected provider
    - Selected agent
    - Runtime state
    - Temporary variables
    """

    def __init__(self) -> None:

        super().__init__(
            name="session_memory",
        )

        self._storage: dict[str, Any] = {}

    ###########################################################################

    def store(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store session value.
        """

        self._storage[key] = value

    ###########################################################################

    def retrieve(
        self,
        key: str,
    ) -> Any:
        """
        Retrieve session value.
        """

        return self._storage.get(key)

    ###########################################################################

    def delete(
        self,
        key: str,
    ) -> None:
        """
        Delete session value.
        """

        self._storage.pop(
            key,
            None,
        )

    ###########################################################################

    def clear(self) -> None:
        """
        Clear entire session.
        """

        self._storage.clear()

        logger.info(
            "Session memory cleared."
        )

    ###########################################################################

    def keys(
        self,
    ) -> list[str]:
        """
        Return stored keys.
        """

        return sorted(
            self._storage.keys()
        )
###############################################################################
# Session Utilities
###############################################################################

    def values(
        self,
    ) -> list[Any]:
        """
        Return all stored values.
        """

        return list(
            self._storage.values()
        )

    ###########################################################################

    def items(
        self,
    ) -> list[tuple[str, Any]]:
        """
        Return all session items.
        """

        return list(
            self._storage.items()
        )

###############################################################################
# Convenience Helpers
###############################################################################

    def active_workspace(self) -> str | None:
        """
        Return active workspace.
        """

        return self.retrieve(
            "workspace"
        )

    ###########################################################################

    def active_provider(self) -> str | None:
        """
        Return active AI provider.
        """

        return self.retrieve(
            "provider"
        )

    ###########################################################################

    def active_agent(self) -> str | None:
        """
        Return active AI agent.
        """

        return self.retrieve(
            "agent"
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(self) -> dict[str, Any]:
        """
        Return session statistics.
        """

        data = super().statistics()

        data.update(
            {
                "entries": len(
                    self._storage
                ),
                "workspace": self.active_workspace(),
                "provider": self.active_provider(),
                "agent": self.active_agent(),
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
        Return complete session report.
        """

        return {
            "metadata": self.metadata(),
            "statistics": self.statistics(),
            "keys": self.keys(),
        }


###############################################################################
# Exports
###############################################################################

__all__ = [
    "SessionMemory",
]