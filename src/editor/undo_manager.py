"""
==============================================================================
GEETA AI Engine

File        : undo_manager.py
Package     : editor
Description : Undo Manager

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
# Undo Action
###############################################################################


@dataclass(slots=True)
class UndoAction:
    """
    Represents an undoable action.
    """

    description: str

    before: str

    after: str

###############################################################################
# Undo Manager
###############################################################################


class UndoManager:
    """
    Undo history manager.

    Responsibilities

    - Undo stack
    - Redo stack
    - History management
    - Transactions
    - AI edit support
    """

    def __init__(
        self,
        max_history: int = 500,
    ) -> None:

        self._undo_stack: list[
            UndoAction
        ] = []

        self._redo_stack: list[
            UndoAction
        ] = []

        self._max_history = max_history

        logger.info(
            "Undo Manager initialized."
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
        Push an undo action.
        """

        self._undo_stack.append(
            UndoAction(
                description=description,
                before=before,
                after=after,
            )
        )

        self._redo_stack.clear()

        if (
            len(self._undo_stack)
            > self._max_history
        ):

            self._undo_stack.pop(0)

###############################################################################
# Undo
###############################################################################

    def undo(
        self,
    ) -> UndoAction | None:
        """
        Undo the latest action.
        """

        if not self._undo_stack:

            return None

        action = self._undo_stack.pop()

        self._redo_stack.append(
            action,
        )

        return action

###############################################################################
# Redo
###############################################################################

    def redo(
        self,
    ) -> UndoAction | None:
        """
        Redo the latest action.
        """

        if not self._redo_stack:

            return None

        action = self._redo_stack.pop()

        self._undo_stack.append(
            action,
        )

        return action

###############################################################################
# Clear
###############################################################################

    def clear(
        self,
    ) -> None:
        """
        Clear history.
        """

        self._undo_stack.clear()

        self._redo_stack.clear()
###############################################################################
# Availability
###############################################################################

    def can_undo(
        self,
    ) -> bool:
        """
        Return whether undo is available.
        """

        return bool(
            self._undo_stack
        )

    ###########################################################################

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

    def undo_history(
        self,
    ) -> list[UndoAction]:
        """
        Return undo history.
        """

        return list(
            self._undo_stack
        )

    ###########################################################################

    def redo_history(
        self,
    ) -> list[UndoAction]:
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
        Return undo manager statistics.
        """

        return {
            "undo_actions": len(
                self._undo_stack
            ),
            "redo_actions": len(
                self._redo_stack
            ),
            "max_history": (
                self._max_history
            ),
            "can_undo": self.can_undo(),
            "can_redo": self.can_redo(),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return undo manager report.
        """

        return {
            "statistics": self.statistics(),
            "undo_history": [
                action.description
                for action
                in self._undo_stack
            ],
            "redo_history": [
                action.description
                for action
                in self._redo_stack
            ],
        }

###############################################################################
# Global Undo Manager
###############################################################################

undo_manager = UndoManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "UndoAction",
    "UndoManager",
    "undo_manager",
]