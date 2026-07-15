"""
==============================================================================
GEETA AI Engine

File        : bookmarks.py
Package     : editor
Description : Editor Bookmarks

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Bookmark
###############################################################################


@dataclass(slots=True)
class Bookmark:
    """
    Represents an editor bookmark.
    """

    file_path: str

    line: int

    column: int = 0

    name: str = ""

###############################################################################
# Bookmark Manager
###############################################################################


class Bookmarks:
    """
    Bookmark manager.

    Responsibilities

    - Create bookmarks
    - Remove bookmarks
    - Navigate bookmarks
    - Numbered bookmarks
    - Persistent bookmarks
    """

    def __init__(
        self,
    ) -> None:

        self._bookmarks: list[
            Bookmark
        ] = []

        self._numbered: dict[
            int,
            Bookmark
        ] = {}

        logger.info(
            "Bookmarks initialized."
        )

###############################################################################
# Add
###############################################################################

    def add(
        self,
        bookmark: Bookmark,
    ) -> None:
        """
        Add bookmark.
        """

        self._bookmarks.append(
            bookmark,
        )

###############################################################################
# Remove
###############################################################################

    def remove(
        self,
        bookmark: Bookmark,
    ) -> bool:
        """
        Remove bookmark.
        """

        if bookmark not in self._bookmarks:

            return False

        self._bookmarks.remove(
            bookmark,
        )

        return True

###############################################################################
# Numbered Bookmarks
###############################################################################

    def set_number(
        self,
        number: int,
        bookmark: Bookmark,
    ) -> None:
        """
        Assign numbered bookmark.
        """

        if not (
            0 <= number <= 9
        ):

            raise ValueError(
                "Bookmark number must be between 0 and 9."
            )

        self._numbered[
            number
        ] = bookmark

###############################################################################
# Lookup
###############################################################################

    def bookmark(
        self,
        number: int,
    ) -> Bookmark | None:
        """
        Return numbered bookmark.
        """

        return self._numbered.get(
            number,
        )

###############################################################################
# List
###############################################################################

    def bookmarks(
        self,
    ) -> list[Bookmark]:
        """
        Return all bookmarks.
        """

        return list(
            self._bookmarks
        )
###############################################################################
# Navigation
###############################################################################

    def next_bookmark(
        self,
        current_line: int,
    ) -> Bookmark | None:
        """
        Return the next bookmark after the given line.
        """

        candidates = sorted(
            self._bookmarks,
            key=lambda bookmark: bookmark.line,
        )

        for bookmark in candidates:

            if bookmark.line > current_line:

                return bookmark

        return candidates[0] if candidates else None

    ###########################################################################

    def previous_bookmark(
        self,
        current_line: int,
    ) -> Bookmark | None:
        """
        Return the previous bookmark before the given line.
        """

        candidates = sorted(
            self._bookmarks,
            key=lambda bookmark: bookmark.line,
        )

        for bookmark in reversed(candidates):

            if bookmark.line < current_line:

                return bookmark

        return candidates[-1] if candidates else None

###############################################################################
# Search
###############################################################################

    def search(
        self,
        query: str,
    ) -> list[Bookmark]:
        """
        Search bookmarks by name or file path.
        """

        query = query.lower()

        return [
            bookmark
            for bookmark
            in self._bookmarks
            if (
                query in bookmark.name.lower()
                or query in bookmark.file_path.lower()
            )
        ]

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return bookmark statistics.
        """

        return {
            "bookmarks": len(
                self._bookmarks
            ),
            "numbered": len(
                self._numbered
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return bookmark report.
        """

        return {
            "statistics": self.statistics(),
            "bookmarks": [
                {
                    "file": bookmark.file_path,
                    "line": bookmark.line,
                    "column": bookmark.column,
                    "name": bookmark.name,
                }
                for bookmark
                in self._bookmarks
            ],
            "numbered": {
                number: {
                    "file": bookmark.file_path,
                    "line": bookmark.line,
                }
                for number, bookmark
                in self._numbered.items()
            },
        }

###############################################################################
# Global Bookmarks
###############################################################################

bookmarks = Bookmarks()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "Bookmark",
    "Bookmarks",
    "bookmarks",
]