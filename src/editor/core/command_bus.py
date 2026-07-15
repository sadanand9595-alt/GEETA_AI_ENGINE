"""
==============================================================================
GEETA AI ENGINE

File        : command_bus.py
Package     : editor.core
Description : Command Bus

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from threading import RLock

from config.logger import get_logger

from editor.core.undo_engine import (
    ChangeType,
    EditOperation,
    UndoEngine,
)

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Base Command
###############################################################################


class Command(ABC):
    """
    Base editor command.
    """

    @abstractmethod
    def execute(
        self,
    ) -> None:
        """
        Execute command.
        """

    ###########################################################################

    @abstractmethod
    def undo(
        self,
    ) -> None:
        """
        Undo command.
        """

###############################################################################
# Command Bus
###############################################################################


class CommandBus:
    """
    Central command dispatcher.

    Responsibilities
    ----------------
    • Execute commands
    • Register undo operations
    • Redo support
    • Future transactions
    """

    ###########################################################################

    def __init__(
        self,
        undo_engine: UndoEngine,
    ) -> None:

        self._lock = RLock()

        self._undo = undo_engine

        logger.info(
            "Command Bus initialized."
        )
        ###############################################################################
# Command Execution
###############################################################################

    def execute(
        self,
        command: Command,
    ) -> None:
        """
        Execute a command.

        The command is responsible for modifying the
        document. After successful execution an
        EditOperation is created and pushed to the
        UndoEngine if supported.
        """

        with self._lock:

            command.execute()

            operation = getattr(
                command,
                "operation",
                None,
            )

            if isinstance(
                operation,
                EditOperation,
            ):

                self._undo.push(
                    operation,
                )

            logger.debug(
                "Executed command: %s",
                command.__class__.__name__,
            )

###############################################################################
# Undo
###############################################################################

    def undo(
        self,
    ) -> bool:
        """
        Undo the last command.
        """

        with self._lock:

            operation = self._undo.undo()

            if operation is None:

                return False

            logger.debug(
                "Undo: %s",
                operation.change.value,
            )

            return True

###############################################################################
# Redo
###############################################################################

    def redo(
        self,
    ) -> bool:
        """
        Redo the last command.
        """

        with self._lock:

            operation = self._undo.redo()

            if operation is None:

                return False

            logger.debug(
                "Redo: %s",
                operation.change.value,
            )

            return True

###############################################################################
# History
###############################################################################

    def can_undo(
        self,
    ) -> bool:
        """
        Return True if undo is available.
        """

        return self._undo.can_undo()

    ###########################################################################

    def can_redo(
        self,
    ) -> bool:
        """
        Return True if redo is available.
        """

        return self._undo.can_redo()

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return command statistics.
        """

        return self._undo.statistics()
        ###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return Command Bus diagnostics.
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
        Reset command history.
        """

        with self._lock:

            self._undo.clear()

        logger.info(
            "Command Bus reset."
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

command_bus = CommandBus(
    undo_engine=UndoEngine(),
)

###############################################################################
# Helper Functions
###############################################################################

def execute_command(
    command: Command,
) -> None:
    """
    Execute a command using the global Command Bus.
    """

    command_bus.execute(
        command,
    )


def undo_command(
) -> bool:
    """
    Undo the most recent command.
    """

    return command_bus.undo()


def redo_command(
) -> bool:
    """
    Redo the most recent command.
    """

    return command_bus.redo()


###############################################################################
# Exports
###############################################################################

__all__ = [
    "Command",
    "CommandBus",
    "command_bus",
    "execute_command",
    "undo_command",
    "redo_command",
]