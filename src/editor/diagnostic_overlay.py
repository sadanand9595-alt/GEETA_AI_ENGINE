"""
==============================================================================
GEETA AI Engine

File        : diagnostic_overlay.py
Package     : editor
Description : Diagnostic Overlay

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
# Diagnostic Severity
###############################################################################


class DiagnosticSeverity(str, Enum):
    """
    Diagnostic severity.
    """

    ERROR = "error"

    WARNING = "warning"

    INFO = "info"

    HINT = "hint"

###############################################################################
# Diagnostic Item
###############################################################################


@dataclass(slots=True)
class DiagnosticItem:
    """
    Represents a diagnostic entry.
    """

    line: int

    column: int

    end_line: int

    end_column: int

    severity: DiagnosticSeverity

    message: str

    source: str = "GEETA"

###############################################################################
# Diagnostic Overlay
###############################################################################


class DiagnosticOverlay:
    """
    Visual diagnostics manager.

    Responsibilities

    - Error overlays
    - Warning overlays
    - Hint overlays
    - Hover diagnostics
    - AI annotations
    """

    def __init__(
        self,
    ) -> None:

        self._diagnostics: list[
            DiagnosticItem
        ] = []

        logger.info(
            "Diagnostic Overlay initialized."
        )

###############################################################################
# Add
###############################################################################

    def add(
        self,
        diagnostic: DiagnosticItem,
    ) -> None:
        """
        Add a diagnostic.
        """

        self._diagnostics.append(
            diagnostic,
        )

###############################################################################
# Remove
###############################################################################

    def remove(
        self,
        diagnostic: DiagnosticItem,
    ) -> bool:
        """
        Remove a diagnostic.
        """

        if diagnostic not in self._diagnostics:

            return False

        self._diagnostics.remove(
            diagnostic,
        )

        return True

###############################################################################
# Clear
###############################################################################

    def clear(
        self,
    ) -> None:
        """
        Remove all diagnostics.
        """

        self._diagnostics.clear()

###############################################################################
# Lookup
###############################################################################

    def diagnostics(
        self,
    ) -> list[DiagnosticItem]:
        """
        Return all diagnostics.
        """

        return list(
            self._diagnostics
        )
###############################################################################
# Filtering
###############################################################################

    def by_severity(
        self,
        severity: DiagnosticSeverity,
    ) -> list[DiagnosticItem]:
        """
        Return diagnostics by severity.
        """

        return [
            diagnostic
            for diagnostic
            in self._diagnostics
            if diagnostic.severity == severity
        ]

    ###########################################################################

    def by_line(
        self,
        line: int,
    ) -> list[DiagnosticItem]:
        """
        Return diagnostics for a line.
        """

        return [
            diagnostic
            for diagnostic
            in self._diagnostics
            if diagnostic.line == line
        ]

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return diagnostic statistics.
        """

        return {
            "total": len(
                self._diagnostics
            ),
            "errors": len(
                self.by_severity(
                    DiagnosticSeverity.ERROR
                )
            ),
            "warnings": len(
                self.by_severity(
                    DiagnosticSeverity.WARNING
                )
            ),
            "infos": len(
                self.by_severity(
                    DiagnosticSeverity.INFO
                )
            ),
            "hints": len(
                self.by_severity(
                    DiagnosticSeverity.HINT
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
        Return diagnostics report.
        """

        return {
            "statistics": self.statistics(),
            "diagnostics": [
                {
                    "line": diagnostic.line,
                    "column": diagnostic.column,
                    "end_line": diagnostic.end_line,
                    "end_column": diagnostic.end_column,
                    "severity": diagnostic.severity.value,
                    "message": diagnostic.message,
                    "source": diagnostic.source,
                }
                for diagnostic
                in self._diagnostics
            ],
        }

###############################################################################
# Global Diagnostic Overlay
###############################################################################

diagnostic_overlay = DiagnosticOverlay()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "DiagnosticSeverity",
    "DiagnosticItem",
    "DiagnosticOverlay",
    "diagnostic_overlay",
]