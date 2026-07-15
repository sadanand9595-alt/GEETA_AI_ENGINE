"""
==============================================================================
GEETA AI Engine

File        : process_utils.py
Package     : utils
Description : Process Utility Functions

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Sequence

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Process Result
###############################################################################


class ProcessResult:
    """
    Represents the result of a process execution.
    """

    def __init__(
        self,
        return_code: int,
        stdout: str,
        stderr: str,
    ) -> None:

        self.return_code = return_code

        self.stdout = stdout

        self.stderr = stderr

    @property
    def success(self) -> bool:
        """
        Return True if process completed successfully.
        """

        return self.return_code == 0


###############################################################################
# Process Execution
###############################################################################


def run(
    command: Sequence[str],
    cwd: Path | None = None,
    timeout: int | None = None,
) -> ProcessResult:
    """
    Execute a process.

    Args:
        command:
            Command and arguments.

        cwd:
            Working directory.

        timeout:
            Timeout in seconds.

    Returns:
        ProcessResult
    """

    logger.info(
        "Executing command: %s",
        " ".join(command),
    )

    completed = subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )

    return ProcessResult(
        return_code=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


###############################################################################
# Shell Execution
###############################################################################


def run_shell(
    command: str,
    cwd: Path | None = None,
    timeout: int | None = None,
) -> ProcessResult:
    """
    Execute shell command.
    """

    logger.info(
        "Executing shell command: %s",
        command,
    )

    completed = subprocess.run(
        command,
        shell=True,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )

    return ProcessResult(
        completed.returncode,
        completed.stdout,
        completed.stderr,
    )


###############################################################################
# Convenience Helpers
###############################################################################


def run_python(
    script: Path,
) -> ProcessResult:
    """
    Execute a Python script.
    """

    import sys

    return run(
        [
            sys.executable,
            str(script),
        ]
    )


def command_exists(
    command: str,
) -> bool:
    """
    Check whether a command exists.
    """

    import shutil

    return shutil.which(command) is not None
###############################################################################
# Process Utilities
###############################################################################


def check_output(
    command: Sequence[str],
    cwd: Path | None = None,
    timeout: int | None = None,
) -> str:
    """
    Execute a command and return stdout.

    Raises:
        subprocess.CalledProcessError
    """

    logger.info(
        "Reading command output: %s",
        " ".join(command),
    )

    return subprocess.check_output(
        command,
        cwd=str(cwd) if cwd else None,
        timeout=timeout,
        text=True,
    )


###############################################################################
# Process Status
###############################################################################


def is_success(
    result: ProcessResult,
) -> bool:
    """
    Return True if process completed successfully.
    """

    return result.success


###############################################################################
# Working Directory
###############################################################################


def run_in_directory(
    command: Sequence[str],
    directory: Path,
) -> ProcessResult:
    """
    Execute command inside a directory.
    """

    return run(
        command=command,
        cwd=directory,
    )


###############################################################################
# Environment
###############################################################################


def run_with_environment(
    command: Sequence[str],
    environment: dict[str, str],
    cwd: Path | None = None,
) -> ProcessResult:
    """
    Execute command with custom environment variables.
    """

    completed = subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    return ProcessResult(
        completed.returncode,
        completed.stdout,
        completed.stderr,
    )


###############################################################################
# Process Information
###############################################################################


def print_result(
    result: ProcessResult,
) -> None:
    """
    Print process result.
    """

    logger.info(
        "Exit Code : %s",
        result.return_code,
    )

    if result.stdout:

        logger.info(
            "STDOUT\n%s",
            result.stdout,
        )

    if result.stderr:

        logger.error(
            "STDERR\n%s",
            result.stderr,
        )


###############################################################################
# Exports
###############################################################################

__all__ = [
    "ProcessResult",
    "run",
    "run_shell",
    "run_python",
    "run_in_directory",
    "run_with_environment",
    "check_output",
    "command_exists",
    "is_success",
    "print_result",
]