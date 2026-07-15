"""
==============================================================================
GEETA AI Engine

File        : string_utils.py
Package     : utils
Description : String Utility Functions

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import re
import string

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Basic Operations
###############################################################################


def is_empty(text: str | None) -> bool:
    """
    Check whether a string is empty.
    """

    return text is None or text.strip() == ""


def is_not_empty(text: str | None) -> bool:
    """
    Check whether a string contains characters.
    """

    return not is_empty(text)


def trim(text: str) -> str:
    """
    Remove leading and trailing whitespace.
    """

    return text.strip()


###############################################################################
# Case Conversion
###############################################################################


def to_upper(text: str) -> str:
    """
    Convert string to uppercase.
    """

    return text.upper()


def to_lower(text: str) -> str:
    """
    Convert string to lowercase.
    """

    return text.lower()


def capitalize(text: str) -> str:
    """
    Capitalize first character.
    """

    return text.capitalize()


def title(text: str) -> str:
    """
    Convert string to title case.
    """

    return text.title()


###############################################################################
# Replace
###############################################################################


def replace(
    text: str,
    old: str,
    new: str,
) -> str:
    """
    Replace text.
    """

    return text.replace(old, new)


###############################################################################
# Remove Whitespace
###############################################################################


def remove_spaces(text: str) -> str:
    """
    Remove all spaces.
    """

    return text.replace(" ", "")


def normalize_spaces(text: str) -> str:
    """
    Replace multiple spaces with one.
    """

    return re.sub(r"\s+", " ", text).strip()


###############################################################################
# Validation
###############################################################################


def is_numeric(text: str) -> bool:
    """
    Check if string contains only digits.
    """

    return text.isdigit()


def is_alpha(text: str) -> bool:
    """
    Check if string contains only letters.
    """

    return text.isalpha()


def is_alphanumeric(text: str) -> bool:
    """
    Check if string contains letters and digits only.
    """

    return text.isalnum()


###############################################################################
# Character Counts
###############################################################################


def length(text: str) -> int:
    """
    Return string length.
    """

    return len(text)


def word_count(text: str) -> int:
    """
    Return number of words.
    """

    return len(text.split())


def line_count(text: str) -> int:
    """
    Return number of lines.
    """

    return len(text.splitlines())


###############################################################################
# Character Filtering
###############################################################################


def remove_punctuation(text: str) -> str:
    """
    Remove punctuation characters.
    """

    return text.translate(
        str.maketrans(
            "",
            "",
            string.punctuation,
        )
    )
###############################################################################
# Search Utilities
###############################################################################


def contains(
    text: str,
    value: str,
    ignore_case: bool = False,
) -> bool:
    """
    Check whether text contains a value.
    """

    if ignore_case:
        text = text.lower()
        value = value.lower()

    return value in text


def starts_with(
    text: str,
    prefix: str,
) -> bool:
    """
    Check whether text starts with prefix.
    """

    return text.startswith(prefix)


def ends_with(
    text: str,
    suffix: str,
) -> bool:
    """
    Check whether text ends with suffix.
    """

    return text.endswith(suffix)


###############################################################################
# String Manipulation
###############################################################################


def reverse(text: str) -> str:
    """
    Reverse a string.
    """

    return text[::-1]


def truncate(
    text: str,
    max_length: int,
    suffix: str = "...",
) -> str:
    """
    Truncate string if it exceeds max_length.
    """

    if len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)] + suffix


###############################################################################
# Slug
###############################################################################


def slugify(text: str) -> str:
    """
    Convert text into URL-friendly slug.
    """

    text = normalize_spaces(text)

    text = text.lower()

    text = remove_punctuation(text)

    text = re.sub(r"\s+", "-", text)

    return text


###############################################################################
# Miscellaneous
###############################################################################


def repeat(
    text: str,
    count: int,
) -> str:
    """
    Repeat string.
    """

    return text * count


def join(
    items: list[str],
    separator: str = ", ",
) -> str:
    """
    Join list of strings.
    """

    return separator.join(items)


###############################################################################
# Exports
###############################################################################

__all__ = [
    "is_empty",
    "is_not_empty",
    "trim",
    "to_upper",
    "to_lower",
    "capitalize",
    "title",
    "replace",
    "remove_spaces",
    "normalize_spaces",
    "is_numeric",
    "is_alpha",
    "is_alphanumeric",
    "length",
    "word_count",
    "line_count",
    "remove_punctuation",
    "contains",
    "starts_with",
    "ends_with",
    "reverse",
    "truncate",
    "slugify",
    "repeat",
    "join",
]