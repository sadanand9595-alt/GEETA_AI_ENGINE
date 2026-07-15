"""
==============================================================================
GEETA AI Engine

File        : json_utils.py
Package     : utils
Description : JSON Utility Functions

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Read JSON
###############################################################################


def read_json(
    path: Path,
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """
    Read JSON file.
    """

    logger.debug(
        "Reading JSON: %s",
        path,
    )

    with path.open(
        "r",
        encoding=encoding,
    ) as file:

        return json.load(file)


###############################################################################
# Write JSON
###############################################################################


def write_json(
    path: Path,
    data: dict[str, Any],
    indent: int = 4,
    encoding: str = "utf-8",
) -> None:
    """
    Write JSON file.
    """

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding=encoding,
    ) as file:

        json.dump(
            data,
            file,
            indent=indent,
            ensure_ascii=False,
        )

    logger.debug(
        "Written JSON: %s",
        path,
    )


###############################################################################
# Pretty JSON
###############################################################################


def dumps(
    data: Any,
    indent: int = 4,
) -> str:
    """
    Convert object to formatted JSON string.
    """

    return json.dumps(
        data,
        indent=indent,
        ensure_ascii=False,
    )


###############################################################################
# Parse JSON
###############################################################################


def loads(
    text: str,
) -> Any:
    """
    Parse JSON string.
    """

    return json.loads(text)


###############################################################################
# Validation
###############################################################################


def is_valid_json(
    text: str,
) -> bool:
    """
    Validate JSON string.
    """

    try:

        json.loads(text)

        return True

    except json.JSONDecodeError:

        return False
###############################################################################
# Safe Operations
###############################################################################


def safe_read_json(
    path: Path,
    default: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Safely read a JSON file.

    Returns:
        Parsed JSON or default value.
    """

    if default is None:
        default = {}

    try:

        return read_json(path)

    except (
        FileNotFoundError,
        json.JSONDecodeError,
        OSError,
    ):

        logger.exception(
            "Failed to read JSON: %s",
            path,
        )

        return default


def safe_write_json(
    path: Path,
    data: dict[str, Any],
) -> bool:
    """
    Safely write JSON file.

    Returns:
        True on success.
    """

    try:

        write_json(path, data)

        return True

    except OSError:

        logger.exception(
            "Failed to write JSON: %s",
            path,
        )

        return False


###############################################################################
# Merge
###############################################################################


def merge(
    base: dict[str, Any],
    update: dict[str, Any],
) -> dict[str, Any]:
    """
    Merge two dictionaries.

    Values from 'update' override values from 'base'.
    """

    merged = base.copy()

    merged.update(update)

    return merged


###############################################################################
# Pretty Save
###############################################################################


def pretty_save(
    path: Path,
    data: dict[str, Any],
) -> None:
    """
    Save formatted JSON.
    """

    write_json(
        path=path,
        data=data,
        indent=4,
    )


###############################################################################
# Exports
###############################################################################

__all__ = [
    "read_json",
    "write_json",
    "safe_read_json",
    "safe_write_json",
    "dumps",
    "loads",
    "merge",
    "pretty_save",
    "is_valid_json",
]