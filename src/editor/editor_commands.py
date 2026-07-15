"""
==============================================================================
GEETA AI Engine

File        : editor_commands.py
Package     : editor
Description : Editor Command Framework

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Command
###############################################################################


@dataclass(slots=True)
class EditorCommand:
    """
    Represents an editor command.
    """

    name: str

    callback: Callable[..., Any]

    description: str = ""

    shortcut: str = ""

    enabled: bool = True

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

###############################################################################
# Editor Commands
###############################################################################


class EditorCommands:
    """
    Command registry.

    Responsibilities

    - Register commands
    - Execute commands
    - Keyboard shortcuts
    - Command palette
    - Plugin commands
    """

    def __init__(
        self,
    ) -> None:

        self._commands: dict[
            str,
            EditorCommand,
        ] = {}

        self._history: list[str] = []

        logger.info(
            "Editor Commands initialized."
        )

###############################################################################
# Register
###############################################################################

    def register(
        self,
        command: EditorCommand,
    ) -> None:
        """
        Register a command.
        """

        self._commands[
            command.name
        ] = command

###############################################################################
# Unregister
###############################################################################

    def unregister(
        self,
        name: str,
    ) -> bool:
        """
        Remove a command.
        """

        if name not in self._commands:

            return False

        del self._commands[name]

        return True

###############################################################################
# Execute
###############################################################################

    def execute(
        self,
        name: str,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Execute a command.
        """

        command = self._commands.get(
            name,
        )

        if command is None:

            raise KeyError(
                f"Unknown command: {name}"
            )

        if not command.enabled:

            raise RuntimeError(
                f"Command '{name}' is disabled."
            )

        self._history.append(
            name,
        )

        return command.callback(
            *args,
            **kwargs,
        )

###############################################################################
# Lookup
###############################################################################

    def command(
        self,
        name: str,
    ) -> EditorCommand | None:
        """
        Return a command.
        """

        return self._commands.get(
            name,
        )
###############################################################################
# Enable / Disable
###############################################################################

    def enable(
        self,
        name: str,
    ) -> bool:
        """
        Enable a command.
        """

        command = self._commands.get(
            name,
        )

        if command is None:

            return False

        command.enabled = True

        return True

    ###########################################################################

    def disable(
        self,
        name: str,
    ) -> bool:
        """
        Disable a command.
        """

        command = self._commands.get(
            name,
        )

        if command is None:

            return False

        command.enabled = False

        return True

###############################################################################
# Command History
###############################################################################

    def history(
        self,
    ) -> list[str]:
        """
        Return executed command history.
        """

        return list(
            self._history
        )

###############################################################################
# Command Palette Search
###############################################################################

    def search(
        self,
        query: str,
    ) -> list[EditorCommand]:
        """
        Search registered commands.
        """

        query = query.lower()

        return [
            command
            for command
            in self._commands.values()
            if (
                query in command.name.lower()
                or query in command.description.lower()
            )
        ]

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return command statistics.
        """

        return {
            "registered_commands": len(
                self._commands
            ),
            "enabled_commands": sum(
                command.enabled
                for command
                in self._commands.values()
            ),
            "history_entries": len(
                self._history
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return command framework report.
        """

        return {
            "statistics": self.statistics(),
            "commands": [
                {
                    "name": command.name,
                    "shortcut": command.shortcut,
                    "enabled": command.enabled,
                }
                for command
                in self._commands.values()
            ],
            "history": self.history(),
        }

###############################################################################
# Global Editor Commands
###############################################################################

editor_commands = EditorCommands()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "EditorCommand",
    "EditorCommands",
    "editor_commands",
]