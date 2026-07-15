"""
==============================================================================
GEETA AI Engine

File        : search_engine.py
Package     : editor
Description : Workspace Search Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Search Result
###############################################################################


@dataclass(slots=True)
class SearchResult:
    """
    Workspace search result.
    """

    file: Path

    line: int

    column: int

    text: str

###############################################################################
# Search Engine
###############################################################################


class SearchEngine:
    """
    Workspace search engine.

    Responsibilities

    - Workspace search
    - Regex search
    - Multi-file search
    - File filtering
    - Incremental search
    """

    def __init__(
        self,
    ) -> None:

        logger.info(
            "Search Engine initialized."
        )

###############################################################################
# Workspace Files
###############################################################################

    def iter_files(
        self,
        workspace: str | Path,
        pattern: str = "*",
    ) -> Iterator[Path]:
        """
        Iterate workspace files.
        """

        root = Path(
            workspace,
        )

        yield from root.rglob(
            pattern,
        )

###############################################################################
# Search
###############################################################################

    def search(
        self,
        workspace: str | Path,
        query: str,
        *,
        pattern: str = "*.py",
        case_sensitive: bool = False,
    ) -> list[SearchResult]:
        """
        Search workspace.
        """

        results: list[
            SearchResult
        ] = []

        flags = 0

        if not case_sensitive:

            flags = re.IGNORECASE

        regex = re.compile(
            re.escape(query),
            flags,
        )

        for file in self.iter_files(
            workspace,
            pattern,
        ):

            try:

                text = file.read_text(
                    encoding="utf-8",
                )

            except Exception:

                continue

            for line_number, line in enumerate(
                text.splitlines(),
                start=1,
            ):

                match = regex.search(
                    line,
                )

                if match:

                    results.append(
                        SearchResult(
                            file=file,
                            line=line_number,
                            column=match.start(),
                            text=line.strip(),
                        )
                    )

        return results
###############################################################################
# Regular Expression Search
###############################################################################

    def regex_search(
        self,
        workspace: str | Path,
        expression: str,
        *,
        pattern: str = "*.py",
    ) -> list[SearchResult]:
        """
        Search using a regular expression.
        """

        results: list[
            SearchResult
        ] = []

        regex = re.compile(
            expression,
        )

        for file in self.iter_files(
            workspace,
            pattern,
        ):

            try:

                text = file.read_text(
                    encoding="utf-8",
                )

            except Exception:

                continue

            for line_number, line in enumerate(
                text.splitlines(),
                start=1,
            ):

                match = regex.search(
                    line,
                )

                if match:

                    results.append(
                        SearchResult(
                            file=file,
                            line=line_number,
                            column=match.start(),
                            text=line.strip(),
                        )
                    )

        return results

###############################################################################
# File Filters
###############################################################################

    def filter_files(
        self,
        files: list[Path],
        *,
        include: str | None = None,
        exclude: str | None = None,
    ) -> list[Path]:
        """
        Filter workspace files.
        """

        filtered = files

        if include:

            filtered = [
                file
                for file in filtered
                if include in str(file)
            ]

        if exclude:

            filtered = [
                file
                for file in filtered
                if exclude not in str(file)
            ]

        return filtered

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
        results: list[SearchResult],
    ) -> dict[str, int]:
        """
        Return search statistics.
        """

        return {
            "matches": len(
                results
            ),
            "files": len(
                {
                    result.file
                    for result
                    in results
                }
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
        results: list[SearchResult],
    ) -> dict[str, object]:
        """
        Return search report.
        """

        return {
            "statistics": (
                self.statistics(
                    results,
                )
            ),
            "results": [
                {
                    "file": str(result.file),
                    "line": result.line,
                    "column": result.column,
                    "text": result.text,
                }
                for result
                in results
            ],
        }

###############################################################################
# Global Search Engine
###############################################################################

search_engine = SearchEngine()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "SearchResult",
    "SearchEngine",
    "search_engine",
]