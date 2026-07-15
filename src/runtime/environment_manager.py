"""
==============================================================================
GEETA AI Engine

File        : environment_manager.py
Package     : runtime
Description : Environment Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Environment Manager
###############################################################################


class EnvironmentManager:
    """
    Development environment manager.

    Responsibilities

    - Virtual environment detection
    - Python interpreter discovery
    - Environment variables
    - Dependency installation
    - .env support
    - Runtime profiles
    """

    def __init__(self) -> None:

        self._environment = dict(
            os.environ
        )

        logger.info(
            "Environment Manager initialized."
        )

    ###########################################################################

    def python_interpreter(
        self,
    ) -> str:
        """
        Return Python interpreter.
        """

        return (
            shutil.which("python")
            or shutil.which("python3")
            or "python"
        )

    ###########################################################################

    def virtual_environment(
        self,
    ) -> Path | None:
        """
        Detect active virtual environment.
        """

        value = self._environment.get(
            "VIRTUAL_ENV",
        )

        if value:

            return Path(value)

        return None

    ###########################################################################

    def load_dotenv(
        self,
        path: str | Path = ".env",
    ) -> bool:
        """
        Load a .env file.
        """

        file = Path(path)

        if not file.exists():

            return False

        for line in file.read_text(
            encoding="utf-8",
        ).splitlines():

            if (
                "=" not in line
                or line.startswith("#")
            ):

                continue

            key, value = line.split(
                "=",
                1,
            )

            self._environment[
                key.strip()
            ] = value.strip()

        logger.info(
            ".env loaded: %s",
            file,
        )

        return True

    ###########################################################################

    def install(
        self,
        package: str,
    ) -> subprocess.CompletedProcess[str]:
        """
        Install a Python package.
        """

        logger.info(
            "Installing package: %s",
            package,
        )

        return subprocess.run(
            [
                self.python_interpreter(),
                "-m",
                "pip",
                "install",
                package,
            ],
            text=True,
            capture_output=True,
            check=False,
        )
###############################################################################
# Virtual Environment Creation
###############################################################################

    def create_virtual_environment(
        self,
        path: str | Path = ".venv",
    ) -> subprocess.CompletedProcess[str]:
        """
        Create a Python virtual environment.
        """

        logger.info(
            "Creating virtual environment: %s",
            path,
        )

        return subprocess.run(
            [
                self.python_interpreter(),
                "-m",
                "venv",
                str(path),
            ],
            text=True,
            capture_output=True,
            check=False,
        )

###############################################################################
# Environment Variables
###############################################################################

    def set(
        self,
        key: str,
        value: str,
    ) -> None:
        """
        Set an environment variable.
        """

        self._environment[key] = value

    ###########################################################################

    def get(
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
# Package Information
###############################################################################

    def package_version(
        self,
        package: str,
    ) -> subprocess.CompletedProcess[str]:
        """
        Display installed package information.
        """

        return subprocess.run(
            [
                self.python_interpreter(),
                "-m",
                "pip",
                "show",
                package,
            ],
            text=True,
            capture_output=True,
            check=False,
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return environment statistics.
        """

        return {
            "python": self.python_interpreter(),
            "virtual_environment": (
                self.virtual_environment() is not None
            ),
            "environment_variables": len(
                self._environment
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return environment report.
        """

        return {
            "statistics": self.statistics(),
            "virtual_environment": (
                str(self.virtual_environment())
                if self.virtual_environment()
                else None
            ),
        }

###############################################################################
# Global Environment Manager
###############################################################################

environment_manager = EnvironmentManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "EnvironmentManager",
    "environment_manager",
]