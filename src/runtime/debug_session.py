"""
==============================================================================
GEETA AI Engine

File        : debug_session.py
Package     : runtime
Description : Interactive Debug Session

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from time import time
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Debug Status
###############################################################################


class DebugState(str, Enum):
    """
    Debug session state.
    """

    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    FINISHED = "finished"


###############################################################################
# Breakpoint
###############################################################################


@dataclass(slots=True)
class Breakpoint:
    """
    Debug breakpoint.
    """

    file: str

    line: int

    enabled: bool = True


###############################################################################
# Debug Session
###############################################################################


class DebugSession:
    """
    Interactive debug session.

    Responsibilities

    - Breakpoint management
    - Session lifecycle
    - Variable inspection
    - Call stack
    - Watch expressions
    """

    def __init__(
        self,
        session_id: str,
    ) -> None:

        self.session_id = session_id

        self.state = DebugState.CREATED

        self.created_at = time()

        self.breakpoints: list[
            Breakpoint
        ] = []

        self.watch_expressions: list[
            str
        ] = []

        logger.info(
            "Debug session created: %s",
            session_id,
        )

    ###########################################################################

    def start(
        self,
    ) -> None:
        """
        Start debugging.
        """

        self.state = DebugState.RUNNING

        logger.info(
            "Debug session started."
        )

    ###########################################################################

    def pause(
        self,
    ) -> None:
        """
        Pause debugging.
        """

        self.state = DebugState.PAUSED

    ###########################################################################

    def resume(
        self,
    ) -> None:
        """
        Resume debugging.
        """

        self.state = DebugState.RUNNING

    ###########################################################################

    def stop(
        self,
    ) -> None:
        """
        Stop debugging.
        """

        self.state = DebugState.STOPPED

    ###########################################################################

    def add_breakpoint(
        self,
        file: str,
        line: int,
    ) -> None:
        """
        Register a breakpoint.
        """

        self.breakpoints.append(
            Breakpoint(
                file=file,
                line=line,
            )
        )

    ###########################################################################

    def remove_breakpoint(
        self,
        file: str,
        line: int,
    ) -> bool:
        """
        Remove a breakpoint.
        """

        for breakpoint in self.breakpoints:

            if (
                breakpoint.file == file
                and breakpoint.line == line
            ):

                self.breakpoints.remove(
                    breakpoint,
                )

                return True

        return False
###############################################################################
# Execution Control
###############################################################################

    def step_into(
        self,
    ) -> None:
        """
        Execute one step into.
        """

        logger.info(
            "Step Into"
        )

    ###########################################################################

    def step_over(
        self,
    ) -> None:
        """
        Execute one step over.
        """

        logger.info(
            "Step Over"
        )

    ###########################################################################

    def step_out(
        self,
    ) -> None:
        """
        Execute one step out.
        """

        logger.info(
            "Step Out"
        )

    ###########################################################################

    def continue_execution(
        self,
    ) -> None:
        """
        Continue execution.
        """

        self.resume()

###############################################################################
# Watch Expressions
###############################################################################

    def add_watch(
        self,
        expression: str,
    ) -> None:
        """
        Add a watch expression.
        """

        self.watch_expressions.append(
            expression,
        )

###############################################################################
# Inspection
###############################################################################

    def variables(
        self,
    ) -> dict[str, Any]:
        """
        Return visible variables.

        Placeholder implementation.
        """

        return {}

    ###########################################################################

    def call_stack(
        self,
    ) -> list[dict[str, Any]]:
        """
        Return current call stack.

        Placeholder implementation.
        """

        return []

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return session statistics.
        """

        return {
            "session_id": self.session_id,
            "state": self.state.value,
            "breakpoints": len(
                self.breakpoints
            ),
            "watch_expressions": len(
                self.watch_expressions
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return debug session report.
        """

        return {
            "statistics": self.statistics(),
            "variables": self.variables(),
            "call_stack": self.call_stack(),
        }

###############################################################################
# Exports
###############################################################################

__all__ = [
    "DebugState",
    "Breakpoint",
    "DebugSession",
]