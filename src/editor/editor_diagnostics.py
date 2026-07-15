"""
==============================================================================
GEETA AI Engine

File        : editor_diagnostics.py
Package     : editor
Description : Editor Diagnostics Manager

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


class Severity(str, Enum):
    """
    Diagnostic severity.
    """

    ERROR = "error"

    WARNING = "warning"

    INFO = "info"

    HINT = "hint"

###############################################################################
# Diagnostic
###############################################################################


@dataclass(slots=True)
class Diagnostic:
    """
    Represents an editor diagnostic.
    """

    file_path: str

    line: int

    column: int

    severity: Severity

    message: str

    source: str = "GEETA"

###############################################################################
# Editor Diagnostics
###############################################################################


class EditorDiagnostics:
    """
    Diagnostic aggregation engine.

    Responsibilities

    - LSP diagnostics
    - AI diagnostics
    - Workspace diagnostics
    - Filtering
    - Caching
    """

    def __init__(
        self,
    ) -> None:

        self._diagnostics: list[
            Diagnostic
        ] = []

        logger.info(
            "Editor Diagnostics initialized."
        )

###############################################################################
# Add
###############################################################################

    def add(
        self,
        diagnostic: Diagnostic,
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
        diagnostic: Diagnostic,
    ) -> bool:
        """
        Remove diagnostic.
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
        file_path: str | None = None,
    ) -> None:
        """
        Clear diagnostics.
        """

        if file_path is None:

            self._diagnostics.clear()

            return

        self._diagnostics = [
            diagnostic
            for diagnostic
            in self._diagnostics
            if diagnostic.file_path != file_path
        ]

###############################################################################
# Lookup
###############################################################################

    def diagnostics(
        self,
    ) -> list[Diagnostic]:
        """
        Return diagnostics.
        """

        return list(
            self._diagnostics
        )
###############################################################################
# Filtering
###############################################################################

    def by_severity(
        self,
        severity: Severity,
    ) -> list[Diagnostic]:
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

    def by_file(
        self,
        file_path: str,
    ) -> list[Diagnostic]:
        """
        Return diagnostics for a file.
        """

        return [
            diagnostic
            for diagnostic
            in self._diagnostics
            if diagnostic.file_path == file_path
        ]

###############################################################################
# Workspace Summary
###############################################################################

    def workspace_summary(
        self,
    ) -> dict[str, int]:
        """
        Return workspace diagnostic summary.
        """

        return {
            "files": len(
                {
                    diagnostic.file_path
                    for diagnostic
                    in self._diagnostics
                }
            ),
            "errors": len(
                self.by_severity(
                    Severity.ERROR
                )
            ),
            "warnings": len(
                self.by_severity(
                    Severity.WARNING
                )
            ),
            "infos": len(
                self.by_severity(
                    Severity.INFO
                )
            ),
            "hints": len(
                self.by_severity(
                    Severity.HINT
                )
            ),
        }

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return diagnostic statistics.
        """

        return {
            "total": len(
                self._diagnostics
            ),
            **self.workspace_summary(),
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
                    "file": diagnostic.file_path,
                    "line": diagnostic.line,
                    "column": diagnostic.column,
                    "severity": diagnostic.severity.value,
                    "message": diagnostic.message,
                    "source": diagnostic.source,
                }
                for diagnostic
                in self._diagnostics
            ],
        }

###############################################################################
# Global Diagnostics
###############################################################################

editor_diagnostics = EditorDiagnostics()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "Severity",
    "Diagnostic",
    "EditorDiagnostics",
    "editor_diagnostics",
]