"""
==============================================================================
GEETA AI Engine

File        : find_replace.py
Package     : editor
Description : Find & Replace Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Find Result
###############################################################################


@dataclass(slots=True)
class FindResult:
    """
    Represents a search match.
    """

    start: int

    end: int

    line: int

    column: int

    text: str

###############################################################################
# Find & Replace
###############################################################################


class FindReplace:
    """
    Find and Replace engine.

    Responsibilities

    - Find
    - Replace
    - Replace All
    - Regex Search
    - Match Collection
    """

    def __init__(
        self,
    ) -> None:

        self._find_history: list[str] = []

        self._replace_history: list[str] = []

        logger.info(
            "Find & Replace initialized."
        )

###############################################################################
# Find
###############################################################################

    def find(
        self,
        text: str,
        pattern: str,
        *,
        case_sensitive: bool = False,
    ) -> list[FindResult]:
        """
        Find all occurrences.
        """

        results: list[
            FindResult
        ] = []

        flags = 0

        if not case_sensitive:

            flags = re.IGNORECASE

        regex = re.compile(
            re.escape(pattern),
            flags,
        )

        self._find_history.append(
            pattern,
        )

        for match in regex.finditer(
            text,
        ):

            before = text[
                : match.start()
            ]

            line = before.count(
                "\n"
            )

            column = len(
                before.split("\n")[-1]
            )

            results.append(
                FindResult(
                    start=match.start(),
                    end=match.end(),
                    line=line,
                    column=column,
                    text=match.group(),
                )
            )

        return results

###############################################################################
# Replace
###############################################################################

    def replace(
        self,
        text: str,
        pattern: str,
        replacement: str,
        *,
        case_sensitive: bool = False,
    ) -> str:
        """
        Replace first occurrence.
        """

        self._replace_history.append(
            replacement,
        )

        flags = 0

        if not case_sensitive:

            flags = re.IGNORECASE

        return re.sub(
            re.escape(pattern),
            replacement,
            text,
            count=1,
            flags=flags,
        )
###############################################################################
# Replace All
###############################################################################

    def replace_all(
        self,
        text: str,
        pattern: str,
        replacement: str,
        *,
        case_sensitive: bool = False,
    ) -> tuple[str, int]:
        """
        Replace all occurrences.
        """

        self._replace_history.append(
            replacement,
        )

        flags = 0

        if not case_sensitive:

            flags = re.IGNORECASE

        updated, count = re.subn(
            re.escape(pattern),
            replacement,
            text,
            flags=flags,
        )

        return (
            updated,
            count,
        )

###############################################################################
# Regular Expression Search
###############################################################################

    def regex_find(
        self,
        text: str,
        expression: str,
    ) -> list[FindResult]:
        """
        Search using a regular expression.
        """

        results: list[FindResult] = []

        for match in re.finditer(
            expression,
            text,
        ):

            before = text[:match.start()]

            line = before.count("\n")

            column = len(
                before.split("\n")[-1]
            )

            results.append(
                FindResult(
                    start=match.start(),
                    end=match.end(),
                    line=line,
                    column=column,
                    text=match.group(),
                )
            )

        return results

###############################################################################
# History
###############################################################################

    def find_history(
        self,
    ) -> list[str]:
        """
        Return find history.
        """

        return list(
            self._find_history
        )

    ###########################################################################

    def replace_history(
        self,
    ) -> list[str]:
        """
        Return replace history.
        """

        return list(
            self._replace_history
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return find/replace statistics.
        """

        return {
            "find_history": len(
                self._find_history
            ),
            "replace_history": len(
                self._replace_history
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return find/replace report.
        """

        return {
            "statistics": self.statistics(),
            "find_history": self.find_history(),
            "replace_history": self.replace_history(),
        }

###############################################################################
# Global Find & Replace
###############################################################################

find_replace = FindReplace()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "FindResult",
    "FindReplace",
    "find_replace",
]