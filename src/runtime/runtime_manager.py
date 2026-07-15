"""
==============================================================================
GEETA AI Engine

File        : runtime_manager.py
Package     : runtime
Description : Runtime Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Runtime Manager
###############################################################################


class RuntimeManager:
    """
    Runtime execution manager.

    Responsibilities

    - Python execution
    - Process management
    - Virtual environments
    - Environment variables
    - Output streaming
    - Runtime diagnostics
    """

    def __init__(self) -> None:

        self._workspace: Path | None = None

        self._environment = dict(
            os.environ
        )

        logger.info(
            "Runtime Manager initialized."
        )

    ###########################################################################

    def set_workspace(
        self,
        workspace: str | Path,
    ) -> None:
        """
        Set active workspace.
        """

        self._workspace = Path(
            workspace
        ).resolve()

    ###########################################################################

    @property
    def workspace(
        self,
    ) -> Path | None:
        """
        Return active workspace.
        """

        return self._workspace

    ###########################################################################

    def execute(
        self,
        command: list[str],
        timeout: int | None = None,
    ) -> subprocess.CompletedProcess[str]:
        """
        Execute a command.
        """

        logger.info(
            "Executing command: %s",
            " ".join(command),
        )

        return subprocess.run(
            command,
            cwd=self._workspace,
            env=self._environment,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )

    ###########################################################################

    def run_python(
        self,
        script: str | Path,
        *arguments: str,
    ) -> subprocess.CompletedProcess[str]:
        """
        Execute a Python script.
        """

        command = [
            "python",
            str(script),
            *arguments,
        ]

        return self.execute(
            command,
        )

    ###########################################################################

    def environment(
        self,
    ) -> dict[str, str]:
        """
        Return runtime environment.
        """

        return dict(
            self._environment
        )
###############################################################################
# Virtual Environment
###############################################################################

    def detect_virtual_environment(
        self,
    ) -> Path | None:
        """
        Detect an active Python virtual environment.
        """

        virtual_env = self._environment.get(
            "VIRTUAL_ENV",
        )

        if virtual_env:

            return Path(
                virtual_env,
            )

        return None

###############################################################################
# Environment Variables
###############################################################################

    def set_environment(
        self,
        key: str,
        value: str,
    ) -> None:
        """
        Set an environment variable.
        """

        self._environment[key] = value

    ###########################################################################

    def get_environment(
        self,
        key: str,
        default: str | None = None,
    ) -> str | None:
        """
        Return an environment variable.
        """

        return self._environment.get(
            key,
            default,
        )

###############################################################################
# Runtime Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, Any]:
        """
        Return runtime diagnostics.
        """

        return {
            "workspace": (
                str(self._workspace)
                if self._workspace
                else None
            ),
            "virtual_environment": (
                str(
                    self.detect_virtual_environment()
                )
                if self.detect_virtual_environment()
                else None
            ),
            "environment_variables": len(
                self._environment
            ),
        }

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return runtime statistics.
        """

        return {
            "workspace_loaded": (
                self._workspace is not None
            ),
            "environment_size": len(
                self._environment
            ),
            "virtual_environment": (
                self.detect_virtual_environment()
                is not None
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return runtime report.
        """

        return {
            "statistics": self.statistics(),
            "diagnostics": self.diagnostics(),
        }

###############################################################################
# Global Runtime Manager
###############################################################################

runtime_manager = RuntimeManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "RuntimeManager",
    "runtime_manager",
]