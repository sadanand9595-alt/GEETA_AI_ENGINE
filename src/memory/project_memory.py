"""
==============================================================================
GEETA AI Engine

File        : project_memory.py
Package     : memory
Description : Project Memory

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
# Project Memory
###############################################################################


class ProjectMemory(BaseMemory):
    """
    Persistent project knowledge.

    Stores:

    - Files
    - Symbols
    - Classes
    - Functions
    - Imports
    - Architecture
    - AI Decisions
    - Coding Patterns
    """

    def __init__(self) -> None:

        super().__init__(
            name="project_memory",
        )

        self._storage: dict[
            str,
            Any,
        ] = {}

    ###########################################################################

    def store(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store project information.
        """

        self._storage[key] = value

    ###########################################################################

    def retrieve(
        self,
        key: str,
    ) -> Any:
        """
        Retrieve stored value.
        """

        return self._storage.get(key)

    ###########################################################################

    def delete(
        self,
        key: str,
    ) -> None:
        """
        Delete stored value.
        """

        self._storage.pop(
            key,
            None,
        )

    ###########################################################################

    def clear(self) -> None:
        """
        Clear project memory.
        """

        self._storage.clear()

        logger.info(
            "Project memory cleared."
        )

    ###########################################################################

    def keys(
        self,
    ) -> list[str]:
        """
        Return all stored keys.
        """

        return sorted(
            self._storage.keys()
        )
###############################################################################
# Project Information
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
        Return all key/value pairs.
        """

        return list(
            self._storage.items()
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(self) -> dict[str, Any]:
        """
        Return project memory statistics.
        """

        data = super().statistics()

        data.update(
            {
                "entries": len(
                    self._storage
                ),
                "keys": len(
                    self.keys()
                ),
            }
        )

        return data

###############################################################################
# Workspace Summary
###############################################################################

    def workspace_summary(self) -> dict[str, Any]:
        """
        Return a high-level workspace summary.
        """

        return {
            "memory": self.name,
            "total_entries": len(
                self._storage
            ),
            "keys": self.keys(),
        }

###############################################################################
# Architecture Report
###############################################################################

    def report(self) -> dict[str, Any]:
        """
        Build a structured project memory report.
        """

        return {
            "metadata": self.metadata(),
            "statistics": self.statistics(),
            "workspace": self.workspace_summary(),
        }


###############################################################################
# Exports
###############################################################################

__all__ = [
    "ProjectMemory",
]