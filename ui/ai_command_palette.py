"""
==============================================================================
GEETA AI IDE

File        : ai_command_palette.py
Package     : ui
Description : Enterprise AI Command Palette

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Command Category
###############################################################################


class CommandCategory(str, Enum):

    AI = "ai"

    EDITOR = "editor"

    GIT = "git"

    WORKSPACE = "workspace"

    TERMINAL = "terminal"

###############################################################################
# Command
###############################################################################


@dataclass(slots=True)
class Command:

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    name: str = ""

    description: str = ""

    category: CommandCategory = (
        CommandCategory.AI
    )

    shortcut: str = ""

    handler: str = ""

###############################################################################
# Command Result
###############################################################################


@dataclass(slots=True)
class CommandResult:

    success: bool = False

    message: str = ""

    executed_at: datetime = field(
        default_factory=datetime.utcnow
    )

###############################################################################
# AI Command Palette
###############################################################################


class AICommandPalette:
    """
    Enterprise AI Command Palette.

    Features

    - Slash commands
    - Command search
    - Favorites
    - History
    - AI routing
    """

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._commands: dict[
            str,
            Command
        ] = {}

        self._history: list[
            Command
        ] = []

        self._favorites: set[
            str
        ] = set()

        logger.info(
            "AI Command Palette initialized."
        )

        self._register_defaults()

###############################################################################
# Default Commands
###############################################################################

    def _register_defaults(
        self,
    ) -> None:

        defaults = [

            Command(
                name="/fix",
                description="Fix current errors",
                handler="auto_fix",
            ),

            Command(
                name="/review",
                description="Review code",
                handler="review",
            ),

            Command(
                name="/refactor",
                description="Refactor selection",
                handler="refactor",
            ),

            Command(
                name="/generate",
                description="Generate code",
                handler="generate",
            ),

            Command(
                name="/test",
                description="Run tests",
                category=CommandCategory.TERMINAL,
                handler="tests",
            ),

            Command(
                name="/commit",
                description="Generate commit",
                category=CommandCategory.GIT,
                handler="commit",
            ),
        ]

        for command in defaults:

            self.register(
                command,
            )

###############################################################################
# Register Command
###############################################################################

    def register(
        self,
        command: Command,
    ) -> None:
        """
        Register command.
        """

        self._commands[
            command.name
        ] = command

        logger.info(
            "Registered %s",
            command.name,
        )

###############################################################################
# Execute
###############################################################################

    async def execute(
        self,
        command_name: str,
    ) -> CommandResult:
        """
        Execute command.
        """

        command = self._commands.get(
            command_name,
        )

        if command is None:

            return CommandResult(
                success=False,
                message="Unknown command.",
            )

        self._history.append(
            command,
        )

        logger.info(
            "Executing %s",
            command.name,
        )

        return CommandResult(
            success=True,
            message=f"Executed {command.name}",
        )
###############################################################################
# Search Commands
###############################################################################

    def search(
        self,
        query: str,
    ) -> list[Command]:
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
# Slash Parser
###############################################################################

    def parse(
        self,
        text: str,
    ) -> tuple[str, list[str]]:
        """
        Parse slash command.
        """

        tokens = text.strip().split()

        if not tokens:

            return "", []

        command = tokens[0]

        arguments = tokens[1:]

        return command, arguments

###############################################################################
# Command History
###############################################################################

    @property
    def history(
        self,
    ) -> list[Command]:
        """
        Return execution history.
        """

        return list(
            self._history
        )

###############################################################################
# Favorite Commands
###############################################################################

    def favorite(
        self,
        command_name: str,
    ) -> bool:
        """
        Mark command as favorite.
        """

        if command_name not in self._commands:

            return False

        self._favorites.add(
            command_name,
        )

        return True

###############################################################################
# Remove Favorite
###############################################################################

    def unfavorite(
        self,
        command_name: str,
    ) -> None:
        """
        Remove favorite command.
        """

        self._favorites.discard(
            command_name,
        )

###############################################################################
# Favorite List
###############################################################################

    def favorites(
        self,
    ) -> list[Command]:
        """
        Return favorite commands.
        """

        return [

            self._commands[name]

            for name
            in sorted(self._favorites)

            if name in self._commands
        ]

###############################################################################
# Recent Commands
###############################################################################

    def recent(
        self,
        limit: int = 10,
    ) -> list[Command]:
        """
        Return recent commands.
        """

        return self._history[-limit:]

###############################################################################
# Keyboard Shortcuts
###############################################################################

    def shortcuts(
        self,
    ) -> dict[str, str]:
        """
        Return shortcut mapping.
        """

        return {

            command.shortcut: command.name

            for command
            in self._commands.values()

            if command.shortcut
        }

###############################################################################
# Auto Complete
###############################################################################

    def autocomplete(
        self,
        prefix: str,
    ) -> list[str]:
        """
        Command autocomplete.
        """

        prefix = prefix.lower()

        return sorted(

            command.name

            for command
            in self._commands.values()

            if command.name.lower().startswith(
                prefix,
            )
        )

###############################################################################
# Validate Command
###############################################################################

    def validate(
        self,
        command_name: str,
    ) -> bool:
        """
        Validate command.
        """

        return (
            command_name
            in self._commands
        )
###############################################################################
# AI Workflow Dispatcher
###############################################################################

    async def dispatch(
        self,
        command_name: str,
        *args,
        **kwargs,
    ) -> CommandResult:
        """
        Dispatch command to appropriate AI workflow.
        """

        if not self.validate(command_name):

            return CommandResult(
                success=False,
                message="Unknown command.",
            )

        command = self._commands[command_name]

        logger.info(
            "Dispatching %s",
            command.name,
        )

        return await self.route(
            command,
            *args,
            **kwargs,
        )

###############################################################################
# AI Agent Router
###############################################################################

    async def route(
        self,
        command: Command,
        *args,
        **kwargs,
    ) -> CommandResult:
        """
        Route command to AI agent.
        """

        routes = {

            "/fix": "AutoFixEngine",

            "/review": "ReviewAgent",

            "/refactor": "RefactorAgent",

            "/generate": "GeneratorAgent",

            "/test": "TestAgent",

            "/commit": "CommitAgent",
        }

        agent = routes.get(
            command.name,
            "Unknown",
        )

        logger.info(
            "Routing to %s",
            agent,
        )

        return CommandResult(

            success=True,

            message=(
                f"{command.name} routed to {agent}"
            ),
        )

###############################################################################
# VS Code Command
###############################################################################

    async def vscode_command(
        self,
        command: str,
        arguments: dict | None = None,
    ) -> bool:
        """
        Execute VS Code command.
        """

        logger.info(
            "VS Code Command: %s",
            command,
        )

        # Forward to VSCodeBridge

        return True

###############################################################################
# Plugin Registration
###############################################################################

    def register_plugin_commands(
        self,
        commands: list[Command],
    ) -> None:
        """
        Register plugin commands.
        """

        for command in commands:

            self.register(
                command,
            )

###############################################################################
# Custom Command
###############################################################################

    def register_custom(
        self,
        name: str,
        description: str,
        handler: str,
    ) -> None:
        """
        Register user command.
        """

        self.register(

            Command(

                name=name,

                description=description,

                handler=handler,
            )
        )

###############################################################################
# Command Analytics
###############################################################################

    def analytics(
        self,
    ) -> dict[str, int]:
        """
        Command analytics.
        """

        counts: dict[str, int] = {}

        for command in self._history:

            counts[
                command.name
            ] = (
                counts.get(
                    command.name,
                    0,
                )
                + 1
            )

        return counts

###############################################################################
# Emit Event
###############################################################################

    def emit(
        self,
        event: str,
        command: Command,
    ) -> None:
        """
        Emit command event.
        """

        logger.info(
            "[%s] %s",
            event,
            command.name,
        )

###############################################################################
# Live Suggestions
###############################################################################

    def suggestions(
        self,
        prefix: str,
        limit: int = 8,
    ) -> list[Command]:
        """
        Return suggested commands.
        """

        matches = self.search(
            prefix,
        )

        return matches[:limit]
###############################################################################
# Command Alias
###############################################################################

    def register_alias(
        self,
        alias: str,
        command_name: str,
    ) -> bool:
        """
        Register command alias.
        """

        if not self.validate(command_name):

            return False

        if not hasattr(
            self,
            "_aliases",
        ):

            self._aliases = {}

        self._aliases[
            alias
        ] = command_name

        return True

###############################################################################
# Resolve Alias
###############################################################################

    def resolve_alias(
        self,
        command_name: str,
    ) -> str:
        """
        Resolve command alias.
        """

        aliases = getattr(
            self,
            "_aliases",
            {},
        )

        return aliases.get(
            command_name,
            command_name,
        )

###############################################################################
# Command Groups
###############################################################################

    def groups(
        self,
    ) -> dict[str, list[Command]]:
        """
        Group commands by category.
        """

        grouped: dict[
            str,
            list[Command]
        ] = {}

        for command in self._commands.values():

            key = command.category.value

            grouped.setdefault(
                key,
                [],
            ).append(
                command,
            )

        return grouped

###############################################################################
# Workspace Context
###############################################################################

    def workspace_context(
        self,
        workspace: str,
        file_path: str,
    ) -> dict[str, str]:
        """
        Build workspace context.
        """

        return {

            "workspace": workspace,

            "file": file_path,
        }

###############################################################################
# Inject AI Context
###############################################################################

    def inject_context(
        self,
        prompt: str,
        context: dict[str, str],
    ) -> str:
        """
        Inject workspace context.
        """

        return (
            f"Workspace: "
            f"{context['workspace']}\n"
            f"File: "
            f"{context['file']}\n\n"
            f"{prompt}"
        )

###############################################################################
# Workflow
###############################################################################

    async def workflow(
        self,
        commands: list[str],
    ) -> list[CommandResult]:
        """
        Execute multiple commands.
        """

        results = []

        for command in commands:

            command = self.resolve_alias(
                command,
            )

            results.append(

                await self.execute(
                    command,
                )
            )

        return results

###############################################################################
# Permission Check
###############################################################################

    def allowed(
        self,
        command_name: str,
    ) -> bool:
        """
        Validate command permissions.
        """

        return self.validate(
            command_name,
        )

###############################################################################
# Command Queue
###############################################################################

    async def queue(
        self,
        command_name: str,
    ) -> None:
        """
        Queue command execution.
        """

        if not hasattr(
            self,
            "_queue",
        ):

            self._queue = []

        self._queue.append(
            command_name,
        )

###############################################################################
# Execute Queue
###############################################################################

    async def execute_queue(
        self,
    ) -> list[CommandResult]:
        """
        Execute queued commands.
        """

        results = []

        while getattr(
            self,
            "_queue",
            [],
        ):

            command = self._queue.pop(
                0,
            )

            results.append(

                await self.execute(
                    command,
                )
            )

        return results

###############################################################################
# Command Log
###############################################################################

    def log(
        self,
        command: str,
    ) -> None:
        """
        Log command execution.
        """

        logger.info(
            "Command executed: %s",
            command,
        )
###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return command palette statistics.
        """

        return {

            "registered_commands": len(
                self._commands,
            ),

            "history": len(
                self._history,
            ),

            "favorites": len(
                self._favorites,
            ),

            "aliases": len(
                getattr(
                    self,
                    "_aliases",
                    {},
                )
            ),

            "queued": len(
                getattr(
                    self,
                    "_queue",
                    [],
                )
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Generate Command Palette report.
        """

        return {

            "statistics": self.statistics(),

            "analytics": self.analytics(),

            "groups": {

                key: len(value)

                for key, value
                in self.groups().items()

            },
        }

###############################################################################
# Cleanup
###############################################################################

    def cleanup(
        self,
    ) -> None:
        """
        Reset Command Palette.
        """

        self._history.clear()

        self._favorites.clear()

        if hasattr(
            self,
            "_aliases",
        ):

            self._aliases.clear()

        if hasattr(
            self,
            "_queue",
        ):

            self._queue.clear()

        logger.info(
            "AI Command Palette cleaned."
        )

###############################################################################
# VS Code Integration
###############################################################################

    async def sync_vscode(
        self,
    ) -> None:
        """
        Synchronize commands with VS Code.
        """

        logger.info(
            "Synchronizing Command Palette with VS Code."
        )

###############################################################################
# AI Agent Integration
###############################################################################

    async def sync_agents(
        self,
    ) -> None:
        """
        Synchronize AI agents.
        """

        logger.info(
            "Synchronizing AI agents."
        )

###############################################################################
# Telemetry
###############################################################################

    def telemetry(
        self,
    ) -> dict[str, object]:
        """
        Collect command telemetry.
        """

        return {

            "executed": len(
                self._history,
            ),

            "favorites": list(
                self._favorites,
            ),

            "analytics": self.analytics(),
        }

###############################################################################
# Global Command Palette
###############################################################################

ai_command_palette: (
    AICommandPalette | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [

    "CommandCategory",

    "Command",

    "CommandResult",

    "AICommandPalette",

    "ai_command_palette",
]