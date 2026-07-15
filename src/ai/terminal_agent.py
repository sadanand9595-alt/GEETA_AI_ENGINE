"""
==============================================================================
GEETA AI IDE

File        : terminal_agent.py
Package     : ai
Description : Enterprise Autonomous Terminal Agent

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from enum import Enum

from config.logger import get_logger

from ai.context_manager import ContextManager
from ai.planner import AITask
from ai.task_manager import AITaskManager

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Terminal Status
###############################################################################


class TerminalStatus(str, Enum):

    IDLE = "idle"

    EXECUTING = "executing"

    ANALYZING = "analyzing"

    FINISHED = "finished"

    FAILED = "failed"

###############################################################################
# Terminal Command
###############################################################################


@dataclass(slots=True)
class TerminalCommand:

    command: str

    working_directory: str

    shell: bool = True

###############################################################################
# Command Result
###############################################################################


@dataclass(slots=True)
class CommandResult:

    success: bool = False

    return_code: int = -1

    stdout: str = ""

    stderr: str = ""

    execution_time: float = 0.0

###############################################################################
# Terminal Agent
###############################################################################


class TerminalAgent:
    """
    Enterprise Autonomous Terminal Agent.

    Responsibilities

    - Execute commands
    - Build automation
    - Git operations
    - Python execution
    - Error detection
    - AI command execution
    """

    ###########################################################################

    def __init__(
        self,
        context: ContextManager,
        task_manager: AITaskManager,
    ) -> None:

        self._context = context

        self._task_manager = task_manager

        self._status = (
            TerminalStatus.IDLE
        )

        logger.info(
            "Terminal Agent initialized."
        )

###############################################################################
# Status
###############################################################################

    @property
    def status(
        self,
    ) -> TerminalStatus:

        return self._status

###############################################################################
# Execute Command
###############################################################################

    def execute(
        self,
        task: AITask,
        command: TerminalCommand,
    ) -> CommandResult:
        """
        Execute terminal command.
        """

        self._status = (
            TerminalStatus.EXECUTING
        )

        self._task_manager.mark_running(
            task,
        )

        logger.info(
            "Executing: %s",
            command.command,
        )

        process = subprocess.run(
            command.command,
            cwd=command.working_directory,
            shell=command.shell,
            capture_output=True,
            text=True,
        )

        return CommandResult(
            success=(
                process.returncode == 0
            ),
            return_code=process.returncode,
            stdout=process.stdout,
            stderr=process.stderr,
        )

###############################################################################
# Detect Errors
###############################################################################

    def detect_errors(
        self,
        result: CommandResult,
    ) -> list[str]:
        """
        Detect command errors.
        """

        if result.success:

            return []

        return [
            line
            for line
            in result.stderr.splitlines()
            if line.strip()
        ]
###############################################################################
# Analyze Output
###############################################################################

    def analyze_output(
        self,
        result: CommandResult,
    ) -> dict[str, object]:
        """
        Analyze command output.
        """

        self._status = (
            TerminalStatus.ANALYZING
        )

        return {
            "success": result.success,
            "return_code": result.return_code,
            "stdout_lines": len(
                result.stdout.splitlines()
            ),
            "stderr_lines": len(
                result.stderr.splitlines()
            ),
            "errors": self.detect_errors(
                result,
            ),
        }

###############################################################################
# Suggest Command
###############################################################################

    def suggest_command(
        self,
        error: str,
    ) -> str:
        """
        Return AI command suggestion.

        Provider Layer will replace this implementation.
        """

        logger.info(
            "Generating command suggestion."
        )

        return (
            f"# Suggested fix for:\n"
            f"# {error}"
        )

###############################################################################
# Finish
###############################################################################

    def finish(
        self,
        task: AITask,
        result: CommandResult,
    ) -> bool:
        """
        Finish terminal task.
        """

        if result.success:

            self._task_manager.mark_completed(
                task,
            )

            self._status = (
                TerminalStatus.FINISHED
            )

            return True

        self._task_manager.mark_failed(
            task,
        )

        self._status = (
            TerminalStatus.FAILED
        )

        return False

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, object]:
        """
        Return Terminal Agent statistics.
        """

        return {
            "status": self._status.value,
            "project": (
                self._context.context.project_name
            ),
            "workspace": (
                self._context.context.workspace_path
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return Terminal Agent report.
        """

        return {
            "agent": "TerminalAgent",
            "statistics": self.statistics(),
        }

###############################################################################
# Global Agent
###############################################################################

terminal_agent: (
    TerminalAgent | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "TerminalStatus",
    "TerminalCommand",
    "CommandResult",
    "TerminalAgent",
    "terminal_agent",
]