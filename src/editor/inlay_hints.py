"""
==============================================================================
GEETA AI Engine

File        : inlay_hints.py
Package     : editor
Description : Inlay Hints

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Hint Types
###############################################################################


class HintType(str, Enum):
    """
    Inlay hint types.
    """

    PARAMETER = "parameter"

    TYPE = "type"

    RETURN = "return"

    AI = "ai"

###############################################################################
# Inlay Hint
###############################################################################


@dataclass(slots=True)
class InlayHint:
    """
    Represents an inlay hint.
    """

    line: int

    column: int

    text: str

    hint_type: HintType

    tooltip: str = ""

###############################################################################
# Inlay Hints Manager
###############################################################################


class InlayHints:
    """
    Inline hint manager.

    Responsibilities

    - Parameter hints
    - Type hints
    - Return hints
    - AI hints
    - LSP hints
    """

    def __init__(
        self,
    ) -> None:

        self._hints: list[
            InlayHint
        ] = []

        self._enabled = True

        logger.info(
            "Inlay Hints initialized."
        )

###############################################################################
# Enable / Disable
###############################################################################

    def enable(
        self,
    ) -> None:
        """
        Enable inlay hints.
        """

        self._enabled = True

    ###########################################################################

    def disable(
        self,
    ) -> None:
        """
        Disable inlay hints.
        """

        self._enabled = False

###############################################################################
# Add Hint
###############################################################################

    def add(
        self,
        hint: InlayHint,
    ) -> None:
        """
        Add an inlay hint.
        """

        self._hints.append(
            hint,
        )

###############################################################################
# Remove Hint
###############################################################################

    def remove(
        self,
        hint: InlayHint,
    ) -> bool:
        """
        Remove an inlay hint.
        """

        if hint not in self._hints:

            return False

        self._hints.remove(
            hint,
        )

        return True

###############################################################################
# Lookup
###############################################################################

    def hints(
        self,
    ) -> list[InlayHint]:
        """
        Return all hints.
        """

        if not self._enabled:

            return []

        return list(
            self._hints
        )
###############################################################################
# Filtering
###############################################################################

    def by_type(
        self,
        hint_type: HintType,
    ) -> list[InlayHint]:
        """
        Return hints by type.
        """

        return [
            hint
            for hint
            in self.hints()
            if hint.hint_type == hint_type
        ]

    ###########################################################################

    def by_line(
        self,
        line: int,
    ) -> list[InlayHint]:
        """
        Return hints for a line.
        """

        return [
            hint
            for hint
            in self.hints()
            if hint.line == line
        ]

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return inlay hint statistics.
        """

        return {
            "enabled": self._enabled,
            "total": len(
                self.hints()
            ),
            "parameter_hints": len(
                self.by_type(
                    HintType.PARAMETER
                )
            ),
            "type_hints": len(
                self.by_type(
                    HintType.TYPE
                )
            ),
            "return_hints": len(
                self.by_type(
                    HintType.RETURN
                )
            ),
            "ai_hints": len(
                self.by_type(
                    HintType.AI
                )
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return inlay hint report.
        """

        return {
            "statistics": self.statistics(),
            "hints": [
                {
                    "line": hint.line,
                    "column": hint.column,
                    "text": hint.text,
                    "type": hint.hint_type.value,
                    "tooltip": hint.tooltip,
                }
                for hint
                in self.hints()
            ],
        }

###############################################################################
# Global Inlay Hints
###############################################################################

inlay_hints = InlayHints()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "HintType",
    "InlayHint",
    "InlayHints",
    "inlay_hints",
]