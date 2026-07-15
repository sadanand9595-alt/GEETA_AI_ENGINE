"""
==============================================================================
GEETA AI IDE

File        : workspace_diagnostics.py
Package     : lsp
Description : Workspace Diagnostics Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Diagnostic Severity
###############################################################################


class DiagnosticSeverity(int, Enum):
    """
    LSP Diagnostic Severity
    """

    ERROR = 1

    WARNING = 2

    INFORMATION = 3

    HINT = 4

###############################################################################
# Workspace Diagnostic
###############################################################################


@dataclass(slots=True)
class WorkspaceDiagnostic:
    """
    Represents a workspace diagnostic.
    """

    uri: str

    message: str

    severity: DiagnosticSeverity

    line: int

    character: int

    source: str = ""

    code: str = ""

###############################################################################
# Workspace Diagnostics
###############################################################################


class WorkspaceDiagnostics:
    """
    Enterprise Workspace Diagnostics.

    Responsibilities

    - Workspace Problems
    - Diagnostics cache
    - Background refresh
    - Severity filtering
    - Problems Panel
    """

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._cache: dict[
            str,
            list[WorkspaceDiagnostic],
        ] = {}

        logger.info(
            "Workspace Diagnostics initialized."
        )

###############################################################################
# Cache
###############################################################################

    def update(
        self,
        uri: str,
        diagnostics: list[
            WorkspaceDiagnostic
        ],
    ) -> None:
        """
        Update diagnostics for a document.
        """

        self._cache[
            uri
        ] = diagnostics

###############################################################################
# Lookup
###############################################################################

    def diagnostics(
        self,
        uri: str,
    ) -> list[
        WorkspaceDiagnostic
    ]:
        """
        Return diagnostics for a document.
        """

        return list(
            self._cache.get(
                uri,
                [],
            )
        )

###############################################################################
# Clear
###############################################################################

    def clear_document(
        self,
        uri: str,
    ) -> None:
        """
        Clear document diagnostics.
        """

        self._cache.pop(
            uri,
            None,
        )

###############################################################################
# Clear Workspace
###############################################################################

    def clear(
        self,
    ) -> None:
        """
        Clear workspace diagnostics.
        """

        self._cache.clear()
###############################################################################
# Filter By Severity
###############################################################################

    def by_severity(
        self,
        severity: DiagnosticSeverity,
    ) -> list[
        WorkspaceDiagnostic
    ]:
        """
        Return diagnostics filtered by severity.
        """

        result: list[
            WorkspaceDiagnostic
        ] = []

        for diagnostics in self._cache.values():

            for diagnostic in diagnostics:

                if diagnostic.severity == severity:

                    result.append(
                        diagnostic,
                    )

        return result

###############################################################################
# Workspace Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return workspace diagnostic statistics.
        """

        total = sum(
            len(items)
            for items
            in self._cache.values()
        )

        return {
            "documents": len(
                self._cache
            ),
            "diagnostics": total,
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
            "information": len(
                self.by_severity(
                    DiagnosticSeverity.INFORMATION
                )
            ),
            "hints": len(
                self.by_severity(
                    DiagnosticSeverity.HINT
                )
            ),
        }

###############################################################################
# Problems Summary
###############################################################################

    def problems_summary(
        self,
    ) -> dict[str, list[str]]:
        """
        Return workspace problems grouped by file.
        """

        return {
            uri: [
                diagnostic.message
                for diagnostic
                in diagnostics
            ]
            for uri, diagnostics
            in self._cache.items()
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return workspace diagnostics report.
        """

        return {
            "statistics": self.statistics(),
            "documents": {
                uri: len(
                    diagnostics
                )
                for uri, diagnostics
                in self._cache.items()
            },
        }

###############################################################################
# Global Workspace Diagnostics
###############################################################################

workspace_diagnostics: (
    WorkspaceDiagnostics | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "DiagnosticSeverity",
    "WorkspaceDiagnostic",
    "WorkspaceDiagnostics",
    "workspace_diagnostics",
]