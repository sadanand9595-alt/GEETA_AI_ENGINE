"""
==============================================================================
GEETA AI Engine

File        : redo_manager.py
Package     : editor
Description : Redo Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Redo Action
###############################################################################


@dataclass(slots=True)
class RedoAction:
    """
    Represents a redoable action.
    """

    description: str

    before: str

    after: str

###############################################################################
# Redo Manager
###############################################################################


class RedoManager:
    """
    Redo history manager.

    Responsibilities

    - Redo stack
    - Replay history
    - Transaction replay
    - Compound operations
    - AI edit replay
    """

    def __init__(
        self,
        max_history: int = 500,
    ) -> None:

        self._redo_stack: list[
            RedoAction
        ] = []

        self._max_history = max_history

        logger.info(
            "Redo Manager initialized."
        )

###############################################################################
# Push
###############################################################################

    def push(
        self,
        description: str,
        before: str,
        after: str,
    ) -> None:
        """
        Push a redo action.
        """

        self._redo_stack.append(
            RedoAction(
                description=description,
                before=before,
                after=after,
            )
        )

        if (
            len(self._redo_stack)
            > self._max_history
        ):

            self._redo_stack.pop(0)

###############################################################################
# Redo
###############################################################################

    def redo(
        self,
    ) -> RedoAction | None:
        """
        Replay the latest redo action.
        """

        if not self._redo_stack:

            return None

        return self._redo_stack.pop()

###############################################################################
# Clear
###############################################################################

    def clear(
        self,
    ) -> None:
        """
        Clear redo history.
        """

        self._redo_stack.clear()

###############################################################################
# Availability
###############################################################################

    def can_redo(
        self,
    ) -> bool:
        """
        Return whether redo is available.
        """

        return bool(
            self._redo_stack
        )
###############################################################################
# History
###############################################################################

    def history(
        self,
    ) -> list[RedoAction]:
        """
        Return redo history.
        """

        return list(
            self._redo_stack
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return redo manager statistics.
        """

        return {
            "redo_actions": len(
                self._redo_stack
            ),
            "max_history": (
                self._max_history
            ),
            "can_redo": (
                self.can_redo()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return redo manager report.
        """

        return {
            "statistics": (
                self.statistics()
            ),
            "history": [
                action.description
                for action
                in self._redo_stack
            ],
        }

###############################################################################
# Global Redo Manager
###############################################################################

redo_manager = RedoManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "RedoAction",
    "RedoManager",
    "redo_manager",
]