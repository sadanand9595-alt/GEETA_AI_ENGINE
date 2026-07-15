"""
==============================================================================
GEETA AI Engine

File        : terminal_manager.py
Package     : runtime
Description : Terminal Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import os
import platform
from pathlib import Path
from typing import Any

from config.logger import get_logger
from runtime.process_manager import process_manager

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Terminal Manager
###############################################################################


class TerminalManager:
    """
    Integrated terminal manager.

    Responsibilities

    - Interactive terminals
    - Shell management
    - Command execution
    - Terminal sessions
    - Command history
    - Environment inheritance
    """

    def __init__(self) -> None:

        self._history: list[str] = []

        self._sessions: dict[
            int,
            dict[str, Any],
        ] = {}

        logger.info(
            "Terminal Manager initialized."
        )

    ###########################################################################

    def default_shell(
        self,
    ) -> str:
        """
        Return default system shell.
        """

        system = platform.system()

        if system == "Windows":

            return os.environ.get(
                "COMSPEC",
                "powershell.exe",
            )

        return os.environ.get(
            "SHELL",
            "/bin/bash",
        )

    ###########################################################################

    def execute(
        self,
        command: str,
        cwd: str | Path | None = None,
    ) -> int:
        """
        Execute a shell command.
        """

        shell = self.default_shell()

        self._history.append(
            command,
        )

        if platform.system() == "Windows":

            args = [
                shell,
                "/c",
                command,
            ]

        else:

            args = [
                shell,
                "-c",
                command,
            ]

        pid = process_manager.start(
            command=args,
            cwd=cwd,
        )

        self._sessions[pid] = {
            "command": command,
            "shell": shell,
            "cwd": (
                str(cwd)
                if cwd
                else None
            ),
        }

        logger.info(
            "Terminal command started: %d",
            pid,
        )

        return pid

    ###########################################################################

    def history(
        self,
    ) -> list[str]:
        """
        Return command history.
        """

        return list(
            self._history
        )
###############################################################################
# Session Management
###############################################################################

    def session(
        self,
        pid: int,
    ) -> dict[str, Any]:
        """
        Return terminal session information.
        """

        return self._sessions[
            pid
        ]

    ###########################################################################

    def terminate(
        self,
        pid: int,
    ) -> None:
        """
        Terminate a terminal session.
        """

        process_manager.terminate(
            pid,
        )

        self._sessions.pop(
            pid,
            None,
        )

        logger.info(
            "Terminal session terminated: %d",
            pid,
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return terminal statistics.
        """

        return {
            "active_sessions": len(
                self._sessions
            ),
            "command_history": len(
                self._history
            ),
            "default_shell": (
                self.default_shell()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return terminal manager report.
        """

        return {
            "statistics": self.statistics(),
            "sessions": list(
                self._sessions.keys()
            ),
            "history": self.history(),
        }

###############################################################################
# Global Terminal Manager
###############################################################################

terminal_manager = TerminalManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "TerminalManager",
    "terminal_manager",
]
