"""
==============================================================================
GEETA AI Engine

File        : execution_engine.py
Package     : runtime
Description : Execution Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from config.logger import get_logger

from engine.debug_engine import debug_engine
from runtime.process_manager import process_manager
from runtime.runtime_manager import runtime_manager
from runtime.terminal_manager import terminal_manager

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Execution Engine
###############################################################################


class ExecutionEngine:
    """
    Central runtime execution engine.

    Responsibilities

    - Build projects
    - Run projects
    - Execute tests
    - Capture output
    - Runtime diagnostics
    - Process orchestration
    """

    def __init__(self) -> None:

        self._history: list[
            dict[str, Any]
        ] = []

        logger.info(
            "Execution Engine initialized."
        )

    ###########################################################################

    def execute_command(
        self,
        command: str,
        cwd: str | Path | None = None,
    ) -> int:
        """
        Execute a shell command.
        """

        logger.info(
            "Executing command: %s",
            command,
        )

        pid = terminal_manager.execute(
            command=command,
            cwd=cwd,
        )

        self._history.append(
            {
                "type": "command",
                "command": command,
                "pid": pid,
            }
        )

        return pid

    ###########################################################################

    def run_python(
        self,
        script: str | Path,
        *arguments: str,
    ):
        """
        Execute a Python script.
        """

        result = runtime_manager.run_python(
            script,
            *arguments,
        )

        self._history.append(
            {
                "type": "python",
                "script": str(script),
                "returncode": result.returncode,
            }
        )

        return result

    ###########################################################################

    def run_tests(
        self,
        path: str | Path = ".",
    ) -> int:
        """
        Execute pytest.
        """

        return self.execute_command(
            "pytest",
            cwd=path,
        )

    ###########################################################################

    def diagnose(
        self,
        source: str,
        error: str,
    ) -> str:
        """
        Run AI diagnostics.
        """

        return debug_engine.suggest_fix(
            source=source,
            error=error,
        )
###############################################################################
# Execution History
###############################################################################

    def history(
        self,
    ) -> list[dict[str, Any]]:
        """
        Return execution history.
        """

        return list(
            self._history
        )

###############################################################################
# Output
###############################################################################

    def output(
        self,
        pid: int,
    ) -> tuple[str, str]:
        """
        Return process stdout and stderr.
        """

        return process_manager.read_output(
            pid,
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return execution engine statistics.
        """

        return {
            "executions": len(
                self._history
            ),
            "runtime": (
                runtime_manager.statistics()
            ),
            "terminal": (
                terminal_manager.statistics()
            ),
            "processes": (
                process_manager.statistics()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return execution engine report.
        """

        return {
            "statistics": self.statistics(),
            "history": self.history(),
        }

###############################################################################
# Global Engine
###############################################################################

execution_engine = ExecutionEngine()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "ExecutionEngine",
    "execution_engine",
]