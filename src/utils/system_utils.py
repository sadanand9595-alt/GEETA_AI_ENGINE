"""
==============================================================================
GEETA AI Engine

File        : system_utils.py
Package     : utils
Description : System Utility Functions

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import os
import platform
import socket
import sys
from pathlib import Path

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Operating System
###############################################################################


def operating_system() -> str:
    """
    Return operating system name.
    """

    return platform.system()


def operating_system_version() -> str:
    """
    Return operating system version.
    """

    return platform.version()


def machine() -> str:
    """
    Return machine architecture.
    """

    return platform.machine()


def processor() -> str:
    """
    Return processor information.
    """

    return platform.processor()


###############################################################################
# Python
###############################################################################


def python_version() -> str:
    """
    Return Python version.
    """

    return platform.python_version()


def executable() -> Path:
    """
    Return Python executable.
    """

    return Path(sys.executable)


###############################################################################
# Working Directory
###############################################################################


def current_directory() -> Path:
    """
    Return current working directory.
    """

    return Path.cwd()


def change_directory(path: Path) -> None:
    """
    Change current working directory.
    """

    os.chdir(path)

    logger.info(
        "Changed working directory: %s",
        path,
    )


###############################################################################
# Environment Variables
###############################################################################


def get_env(
    key: str,
    default: str | None = None,
) -> str | None:
    """
    Return environment variable.
    """

    return os.getenv(key, default)


def set_env(
    key: str,
    value: str,
) -> None:
    """
    Set environment variable.
    """

    os.environ[key] = value

    logger.debug(
        "Environment variable set: %s",
        key,
    )


###############################################################################
# Host Information
###############################################################################


def hostname() -> str:
    """
    Return host name.
    """

    return socket.gethostname()


def ip_address() -> str:
    """
    Return primary IP address.
    """

    return socket.gethostbyname(
        socket.gethostname()
    )
###############################################################################
# CPU Information
###############################################################################


def cpu_count() -> int:
    """
    Return available CPU cores.
    """

    return os.cpu_count() or 1


###############################################################################
# Platform Flags
###############################################################################


def is_windows() -> bool:
    """
    Check if running on Windows.
    """

    return platform.system() == "Windows"


def is_linux() -> bool:
    """
    Check if running on Linux.
    """

    return platform.system() == "Linux"


def is_macos() -> bool:
    """
    Check if running on macOS.
    """

    return platform.system() == "Darwin"


###############################################################################
# Environment
###############################################################################


def environment() -> dict[str, str]:
    """
    Return all environment variables.
    """

    return dict(os.environ)


def home_directory() -> Path:
    """
    Return user's home directory.
    """

    return Path.home()


def temp_directory() -> Path:
    """
    Return system temporary directory.
    """

    import tempfile

    return Path(tempfile.gettempdir())


###############################################################################
# Python Information
###############################################################################


def python_implementation() -> str:
    """
    Return Python implementation.
    """

    return platform.python_implementation()


###############################################################################
# Exports
###############################################################################

__all__ = [
    "operating_system",
    "operating_system_version",
    "machine",
    "processor",
    "python_version",
    "python_implementation",
    "executable",
    "current_directory",
    "change_directory",
    "get_env",
    "set_env",
    "environment",
    "hostname",
    "ip_address",
    "cpu_count",
    "home_directory",
    "temp_directory",
    "is_windows",
    "is_linux",
    "is_macos",
]