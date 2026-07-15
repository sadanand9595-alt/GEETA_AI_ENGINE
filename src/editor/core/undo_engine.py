"""
==============================================================================
GEETA AI ENGINE

File        : undo_engine.py
Package     : editor.core
Description : Undo / Redo Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from threading import RLock
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Change Type
###############################################################################


class ChangeType(Enum):
    """
    Supported edit operations.
    """

    INSERT = "insert"

    DELETE = "delete"

    REPLACE = "replace"

###############################################################################
# Edit Operation
###############################################################################


@dataclass(slots=True)
class EditOperation:
    """
    Single undoable operation.
    """

    change: ChangeType

    offset: int

    old_text: str

    new_text: str

    metadata: dict[str, Any] | None = None

###############################################################################
# Undo Engine
###############################################################################


class UndoEngine:
    """
    Enterprise Undo / Redo Engine.

    Features
    --------
    • Unlimited Undo
    • Unlimited Redo
    • Thread Safe
    • Command Based
    • Future Transaction Support
    """

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._lock = RLock()

        self._undo_stack: list[
            EditOperation
        ] = []

        self._redo_stack: list[
            EditOperation
        ] = []

        logger.info(
            "Undo Engine initialized."
        )
        ###############################################################################
# Stack Management
###############################################################################

    def push(
        self,
        operation: EditOperation,
    ) -> None:
        """
        Push a new operation onto the undo stack.

        Adding a new operation invalidates the redo history.
        """

        with self._lock:

            self._undo_stack.append(
                operation,
            )

            self._redo_stack.clear()

            logger.debug(
                "Undo operation added (%s).",
                operation.change.value,
            )

###############################################################################
# Undo
###############################################################################

    def undo(
        self,
    ) -> EditOperation | None:
        """
        Pop the most recent operation from the undo stack.

        The operation is moved to the redo stack.
        """

        with self._lock:

            if not self._undo_stack:

                return None

            operation = self._undo_stack.pop()

            self._redo_stack.append(
                operation,
            )

            logger.debug(
                "Undo operation: %s",
                operation.change.value,
            )

            return operation

###############################################################################
# Redo
###############################################################################

    def redo(
        self,
    ) -> EditOperation | None:
        """
        Pop the most recent operation from the redo stack.

        The operation is moved back to the undo stack.
        """

        with self._lock:

            if not self._redo_stack:

                return None

            operation = self._redo_stack.pop()

            self._undo_stack.append(
                operation,
            )

            logger.debug(
                "Redo operation: %s",
                operation.change.value,
            )

            return operation

###############################################################################
# Clear
###############################################################################

    def clear(
        self,
    ) -> None:
        """
        Clear both undo and redo stacks.
        """

        with self._lock:

            self._undo_stack.clear()

            self._redo_stack.clear()

        logger.info(
            "Undo history cleared."
        )

###############################################################################
# Queries
###############################################################################

    def can_undo(
        self,
    ) -> bool:
        """
        Return True if an undo operation is available.
        """

        return bool(
            self._undo_stack,
        )

    ###########################################################################

    def can_redo(
        self,
    ) -> bool:
        """
        Return True if a redo operation is available.
        """

        return bool(
            self._redo_stack,
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return stack statistics.
        """

        return {
            "undo_count": len(
                self._undo_stack,
            ),
            "redo_count": len(
                self._redo_stack,
            ),
        }
        ###############################################################################
# History
###############################################################################

    def undo_history(
        self,
    ) -> list[EditOperation]:
        """
        Return a copy of the undo history.
        """

        with self._lock:

            return self._undo_stack.copy()

    ###########################################################################

    def redo_history(
        self,
    ) -> list[EditOperation]:
        """
        Return a copy of the redo history.
        """

        with self._lock:

            return self._redo_stack.copy()

###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return Undo Engine diagnostics.
        """

        stats = self.statistics()

        return {
            **stats,
            "can_undo": self.can_undo(),
            "can_redo": self.can_redo(),
        }

###############################################################################
# Reset
###############################################################################

    def reset(
        self,
    ) -> None:
        """
        Reset the Undo Engine.
        """

        self.clear()

        logger.info(
            "Undo Engine reset."
        )

###############################################################################
# Representation
###############################################################################

    def __repr__(
        self,
    ) -> str:
        """
        Developer-friendly representation.
        """

        stats = self.statistics()

        return (
            f"{self.__class__.__name__}"
            f"(undo={stats['undo_count']}, "
            f"redo={stats['redo_count']})"
        )

###############################################################################
# Global Instance
###############################################################################

undo_engine = UndoEngine()

###############################################################################
# Helper Functions
###############################################################################

def push_operation(
    operation: EditOperation,
) -> None:
    """
    Push an operation to the global Undo Engine.
    """

    undo_engine.push(
        operation,
    )


def undo_operation(
) -> EditOperation | None:
    """
    Perform an undo.
    """

    return undo_engine.undo()


def redo_operation(
) -> EditOperation | None:
    """
    Perform a redo.
    """

    return undo_engine.redo()


###############################################################################
# Exports
###############################################################################

__all__ = [
    "ChangeType",
    "EditOperation",
    "UndoEngine",
    "undo_engine",
    "push_operation",
    "undo_operation",
    "redo_operation",
]