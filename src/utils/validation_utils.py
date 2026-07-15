"""
==============================================================================
GEETA AI Engine

File        : validation_utils.py
Package     : utils
Description : Validation Utility Functions

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import re
from pathlib import Path

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Regular Expressions
###############################################################################

EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

URL_PATTERN = re.compile(
    r"^https?://.+"
)

PYTHON_IDENTIFIER_PATTERN = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_]*$"
)

###############################################################################
# Empty Validation
###############################################################################


def is_empty(value: str | None) -> bool:
    """
    Return True if value is empty.
    """

    return value is None or value.strip() == ""


def is_not_empty(value: str | None) -> bool:
    """
    Return True if value is not empty.
    """

    return not is_empty(value)


###############################################################################
# Email
###############################################################################


def is_email(value: str) -> bool:
    """
    Validate email address.
    """

    return EMAIL_PATTERN.fullmatch(value) is not None


###############################################################################
# URL
###############################################################################


def is_url(value: str) -> bool:
    """
    Validate URL.
    """

    return URL_PATTERN.fullmatch(value) is not None


###############################################################################
# Python Identifier
###############################################################################


def is_python_identifier(
    value: str,
) -> bool:
    """
    Validate Python identifier.
    """

    return (
        PYTHON_IDENTIFIER_PATTERN.fullmatch(value)
        is not None
    )


###############################################################################
# Numeric Validation
###############################################################################


def is_integer(value: str) -> bool:
    """
    Check whether string represents an integer.
    """

    try:

        int(value)

        return True

    except ValueError:

        return False


def is_float(value: str) -> bool:
    """
    Check whether string represents a float.
    """

    try:

        float(value)

        return True

    except ValueError:

        return False


###############################################################################
# Path Validation
###############################################################################


def file_exists(path: Path) -> bool:
    """
    Check whether file exists.
    """

    return path.exists() and path.is_file()


def directory_exists(path: Path) -> bool:
    """
    Check whether directory exists.
    """

    return path.exists() and path.is_dir()
###############################################################################
# Length Validation
###############################################################################


def has_min_length(
    value: str,
    minimum: int,
) -> bool:
    """
    Check whether string satisfies minimum length.
    """

    return len(value) >= minimum


def has_max_length(
    value: str,
    maximum: int,
) -> bool:
    """
    Check whether string satisfies maximum length.
    """

    return len(value) <= maximum


def is_length_between(
    value: str,
    minimum: int,
    maximum: int,
) -> bool:
    """
    Check whether string length is within range.
    """

    return minimum <= len(value) <= maximum


###############################################################################
# Numeric Range Validation
###############################################################################


def is_between(
    value: int | float,
    minimum: int | float,
    maximum: int | float,
) -> bool:
    """
    Check whether numeric value is within range.
    """

    return minimum <= value <= maximum


def is_positive(
    value: int | float,
) -> bool:
    """
    Check whether value is positive.
    """

    return value > 0


def is_negative(
    value: int | float,
) -> bool:
    """
    Check whether value is negative.
    """

    return value < 0


###############################################################################
# Extension Validation
###############################################################################


def has_extension(
    path: Path,
    extension: str,
) -> bool:
    """
    Check file extension.
    """

    return path.suffix.lower() == extension.lower()


def has_extensions(
    path: Path,
    extensions: list[str],
) -> bool:
    """
    Check file extension against a list.
    """

    suffix = path.suffix.lower()

    return suffix in {
        ext.lower()
        for ext in extensions
    }


###############################################################################
# Required Value
###############################################################################


def is_required(
    value: object,
) -> bool:
    """
    Check whether value is present.
    """

    if value is None:
        return False

    if isinstance(value, str):
        return value.strip() != ""

    return True


###############################################################################
# Exports
###############################################################################

__all__ = [
    "is_empty",
    "is_not_empty",
    "is_email",
    "is_url",
    "is_python_identifier",
    "is_integer",
    "is_float",
    "file_exists",
    "directory_exists",
    "has_min_length",
    "has_max_length",
    "is_length_between",
    "is_between",
    "is_positive",
    "is_negative",
    "has_extension",
    "has_extensions",
    "is_required",
]