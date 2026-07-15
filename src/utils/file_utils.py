"""
==============================================================================
GEETA AI Engine

File        : file_utils.py
Package     : utils
Description : File Utility Functions

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Read File
###############################################################################


def read_text(path: Path, encoding: str = "utf-8") -> str:
    """
    Read a text file.

    Args:
        path:
            File path.

        encoding:
            File encoding.

    Returns:
        File contents.
    """

    logger.debug("Reading file: %s", path)

    return path.read_text(
        encoding=encoding,
    )


###############################################################################
# Write File
###############################################################################


def write_text(
    path: Path,
    content: str,
    encoding: str = "utf-8",
) -> None:
    """
    Write text to file.
    """

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        content,
        encoding=encoding,
    )

    logger.debug("Written file: %s", path)


###############################################################################
# Append File
###############################################################################


def append_text(
    path: Path,
    content: str,
    encoding: str = "utf-8",
) -> None:
    """
    Append text to file.
    """

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "a",
        encoding=encoding,
    ) as file:

        file.write(content)

    logger.debug("Appended file: %s", path)


###############################################################################
# Copy File
###############################################################################


def copy_file(
    source: Path,
    destination: Path,
) -> None:
    """
    Copy file.
    """

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    shutil.copy2(
        source,
        destination,
    )

    logger.debug(
        "Copied file: %s -> %s",
        source,
        destination,
    )


###############################################################################
# Move File
###############################################################################


def move_file(
    source: Path,
    destination: Path,
) -> None:
    """
    Move file.
    """

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    shutil.move(
        str(source),
        str(destination),
    )

    logger.debug(
        "Moved file: %s -> %s",
        source,
        destination,
    )


###############################################################################
# Delete File
###############################################################################


def delete_file(
    path: Path,
) -> bool:
    """
    Delete a file.

    Returns:
        True if deleted.
    """

    if not path.exists():
        return False

    path.unlink()

    logger.debug(
        "Deleted file: %s",
        path,
    )

    return True


###############################################################################
# SHA256
###############################################################################


def sha256(
    path: Path,
    chunk_size: int = 8192,
) -> str:
    """
    Calculate SHA256 checksum.
    """

    digest = hashlib.sha256()

    with path.open("rb") as file:

        while chunk := file.read(chunk_size):

            digest.update(chunk)

    return digest.hexdigest()
###############################################################################
# Directory Utilities
###############################################################################


def create_directory(path: Path) -> None:
    """
    Create directory if it does not exist.
    """

    path.mkdir(
        parents=True,
        exist_ok=True,
    )

    logger.debug(
        "Created directory: %s",
        path,
    )


def delete_directory(path: Path) -> bool:
    """
    Delete directory recursively.

    Returns:
        True if directory was deleted.
    """

    if not path.exists():
        return False

    shutil.rmtree(path)

    logger.debug(
        "Deleted directory: %s",
        path,
    )

    return True


###############################################################################
# File Information
###############################################################################


def file_size(path: Path) -> int:
    """
    Return file size in bytes.
    """

    return path.stat().st_size


def file_exists(path: Path) -> bool:
    """
    Check whether a file exists.
    """

    return path.exists() and path.is_file()


def directory_exists(path: Path) -> bool:
    """
    Check whether a directory exists.
    """

    return path.exists() and path.is_dir()


###############################################################################
# Search Utilities
###############################################################################


def find_files(
    directory: Path,
    pattern: str = "*",
) -> list[Path]:
    """
    Find files recursively.
    """

    return sorted(
        file
        for file in directory.rglob(pattern)
        if file.is_file()
    )


###############################################################################
# Extension Utilities
###############################################################################


def extension(path: Path) -> str:
    """
    Return file extension.
    """

    return path.suffix.lower()


def filename(path: Path) -> str:
    """
    Return filename.
    """

    return path.name


def stem(path: Path) -> str:
    """
    Return filename without extension.
    """

    return path.stem


###############################################################################
# Exports
###############################################################################

__all__ = [
    "read_text",
    "write_text",
    "append_text",
    "copy_file",
    "move_file",
    "delete_file",
    "create_directory",
    "delete_directory",
    "file_size",
    "file_exists",
    "directory_exists",
    "find_files",
    "extension",
    "filename",
    "stem",
    "sha256",
]