"""
==============================================================================
GEETA AI Engine

File        : breadcrumbs.py
Package     : editor
Description : Editor Breadcrumbs

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Breadcrumbs
###############################################################################


class Breadcrumbs:
    """
    Breadcrumb navigation manager.

    Responsibilities

    - File path navigation
    - Symbol navigation
    - Namespace hierarchy
    - Document navigation
    """

    def __init__(
        self,
    ) -> None:

        self._file_path: Path | None = None

        self._symbols: list[
            str
        ] = []

        logger.info(
            "Breadcrumbs initialized."
        )

###############################################################################
# File Path
###############################################################################

    def set_file(
        self,
        file_path: str | Path,
    ) -> None:
        """
        Set current file.
        """

        self._file_path = Path(
            file_path
        ).resolve()

###############################################################################
# Symbols
###############################################################################

    def set_symbols(
        self,
        symbols: list[str],
    ) -> None:
        """
        Set breadcrumb symbols.
        """

        self._symbols = list(
            symbols,
        )

###############################################################################
# File Breadcrumbs
###############################################################################

    def file_breadcrumbs(
        self,
    ) -> list[str]:
        """
        Return file path breadcrumbs.
        """

        if self._file_path is None:

            return []

        return list(
            self._file_path.parts
        )

###############################################################################
# Symbol Breadcrumbs
###############################################################################

    def symbol_breadcrumbs(
        self,
    ) -> list[str]:
        """
        Return symbol breadcrumbs.
        """

        return list(
            self._symbols
        )
###############################################################################
# Clear
###############################################################################

    def clear(
        self,
    ) -> None:
        """
        Clear breadcrumb state.
        """

        self._file_path = None

        self._symbols.clear()

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return breadcrumb statistics.
        """

        return {
            "has_file": self._file_path is not None,
            "path_depth": len(
                self.file_breadcrumbs()
            ),
            "symbol_count": len(
                self._symbols
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return breadcrumb report.
        """

        return {
            "statistics": self.statistics(),
            "file": self.file_breadcrumbs(),
            "symbols": self.symbol_breadcrumbs(),
        }

###############################################################################
# Global Breadcrumbs
###############################################################################

breadcrumbs = Breadcrumbs()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "Breadcrumbs",
    "breadcrumbs",
]