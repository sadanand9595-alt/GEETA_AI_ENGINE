"""
==============================================================================
GEETA AI Engine

File        : code_lens.py
Package     : editor
Description : Code Lens Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Code Lens
###############################################################################


@dataclass(slots=True)
class CodeLens:
    """
    Represents a Code Lens item.
    """

    line: int

    title: str

    command: str

    tooltip: str = ""

###############################################################################
# Code Lens Manager
###############################################################################


class CodeLensManager:
    """
    Code Lens manager.

    Responsibilities

    - Code Lens registration
    - AI Code Lens
    - Reference count
    - Test runner lenses
    - Git lenses
    - LSP Code Lens support
    """

    def __init__(
        self,
    ) -> None:

        self._lenses: list[
            CodeLens
        ] = []

        self._enabled = True

        logger.info(
            "Code Lens Manager initialized."
        )

###############################################################################
# Enable / Disable
###############################################################################

    def enable(
        self,
    ) -> None:
        """
        Enable Code Lens.
        """

        self._enabled = True

    ###########################################################################

    def disable(
        self,
    ) -> None:
        """
        Disable Code Lens.
        """

        self._enabled = False

###############################################################################
# Add / Remove
###############################################################################

    def add(
        self,
        lens: CodeLens,
    ) -> None:
        """
        Add a Code Lens.
        """

        self._lenses.append(
            lens,
        )

    ###########################################################################

    def remove(
        self,
        lens: CodeLens,
    ) -> bool:
        """
        Remove a Code Lens.
        """

        if lens not in self._lenses:

            return False

        self._lenses.remove(
            lens,
        )

        return True

###############################################################################
# Lookup
###############################################################################

    def lenses(
        self,
    ) -> list[CodeLens]:
        """
        Return active Code Lenses.
        """

        if not self._enabled:

            return []

        return list(
            self._lenses
        )
###############################################################################
# Filtering
###############################################################################

    def by_line(
        self,
        line: int,
    ) -> list[CodeLens]:
        """
        Return Code Lens entries for a line.
        """

        if not self._enabled:

            return []

        return [
            lens
            for lens
            in self._lenses
            if lens.line == line
        ]

###############################################################################
# Clear
###############################################################################

    def clear(
        self,
    ) -> None:
        """
        Remove all Code Lens entries.
        """

        self._lenses.clear()

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return Code Lens statistics.
        """

        return {
            "enabled": self._enabled,
            "total_lenses": len(
                self._lenses
            ),
            "visible_lenses": len(
                self.lenses()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return Code Lens report.
        """

        return {
            "statistics": self.statistics(),
            "lenses": [
                {
                    "line": lens.line,
                    "title": lens.title,
                    "command": lens.command,
                    "tooltip": lens.tooltip,
                }
                for lens
                in self.lenses()
            ],
        }

###############################################################################
# Global Code Lens Manager
###############################################################################

code_lens_manager = CodeLensManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "CodeLens",
    "CodeLensManager",
    "code_lens_manager",
]