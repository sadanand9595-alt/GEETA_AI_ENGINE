"""
==============================================================================
GEETA AI Engine

File        : vscode_diagnostics_listener.py
Package     : listeners
Description : VS Code Diagnostics Listener

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from config.logger import get_logger
from core.event_bus import publish

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# VS Code Diagnostics Listener
###############################################################################


class VSCodeDiagnosticsListener:
    """
    Processes VS Code diagnostics and publishes them to the event bus.
    """

    def __init__(self) -> None:

        self._diagnostics: list[dict[str, Any]] = []

    ###########################################################################

    @property
    def diagnostics(self) -> list[dict[str, Any]]:
        """
        Return collected diagnostics.
        """

        return list(self._diagnostics)

    ###########################################################################

    def clear(self) -> None:
        """
        Remove all stored diagnostics.
        """

        self._diagnostics.clear()

    ###########################################################################

    def add(
        self,
        *,
        file: str | Path,
        line: int,
        column: int,
        severity: str,
        message: str,
        code: str | None = None,
        source: str = "vscode",
    ) -> None:
        """
        Add a diagnostic entry.
        """

        diagnostic = {
            "file": str(file),
            "line": line,
            "column": column,
            "severity": severity,
            "message": message,
            "code": code,
            "source": source,
        }

        self._diagnostics.append(
            diagnostic
        )

        logger.warning(
            "[%s] %s:%d:%d %s",
            severity.upper(),
            file,
            line,
            column,
            message,
        )

        publish(
            "vscode.diagnostic",
            diagnostic=diagnostic,
        )

    ###########################################################################

    def remove(
        self,
        file: str | Path,
    ) -> None:
        """
        Remove diagnostics for a file.
        """

        file = str(file)

        self._diagnostics = [
            item
            for item in self._diagnostics
            if item["file"] != file
        ]

        logger.info(
            "Diagnostics removed: %s",
            file,
        )
###############################################################################
# Query Methods
###############################################################################


    def get_all(self) -> list[dict[str, Any]]:
        """
        Return all diagnostics.
        """

        return list(self._diagnostics)

    ###########################################################################

    def get_by_file(
        self,
        file: str | Path,
    ) -> list[dict[str, Any]]:
        """
        Return diagnostics for a specific file.
        """

        file = str(file)

        return [
            diagnostic
            for diagnostic in self._diagnostics
            if diagnostic["file"] == file
        ]

    ###########################################################################

    def count(self) -> int:
        """
        Return total number of diagnostics.
        """

        return len(self._diagnostics)

    ###########################################################################

    def has_errors(self) -> bool:
        """
        Return True if any error-level diagnostics exist.
        """

        return any(
            diagnostic["severity"].lower() == "error"
            for diagnostic in self._diagnostics
        )


###############################################################################
# Helper Functions
###############################################################################


def add_diagnostic(
    *,
    file: str | Path,
    line: int,
    column: int,
    severity: str,
    message: str,
    code: str | None = None,
) -> None:
    """
    Add a VS Code diagnostic.
    """

    vscode_diagnostics_listener.add(
        file=file,
        line=line,
        column=column,
        severity=severity,
        message=message,
        code=code,
    )


def clear_diagnostics() -> None:
    """
    Clear all stored diagnostics.
    """

    vscode_diagnostics_listener.clear()


###############################################################################
# Global Instance
###############################################################################

vscode_diagnostics_listener = VSCodeDiagnosticsListener()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "VSCodeDiagnosticsListener",
    "vscode_diagnostics_listener",
    "add_diagnostic",
    "clear_diagnostics",
]