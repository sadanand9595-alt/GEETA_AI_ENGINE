"""
==============================================================================
GEETA AI ENGINE

File        : compile_recovery.py
Package     : tools
Description : Enterprise Compile Recovery Tool

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

###############################################################################
# Imports
###############################################################################

import json
import py_compile
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Compile Error
###############################################################################


@dataclass(slots=True)
class CompileError:

    file: str

    error_type: str

    message: str

    line: int | None = None

    column: int | None = None


###############################################################################
# Compile Recovery
###############################################################################


class CompileRecovery:
    """
    Enterprise compile recovery engine.

    Responsibilities

    • Scan workspace
    • Compile Python files
    • Collect errors
    • Build recovery report
    • Export JSON reports
    """

    ###########################################################################

    def __init__(
        self,
        root: str | Path = "src",
    ) -> None:

        self.root = Path(root)

        self.errors: list[CompileError] = []

        logger.info(
            "Compile Recovery initialized."
        )
        ###############################################################################
# Scan Files
###############################################################################

    def scan_files(
        self,
    ) -> list[Path]:
        """
        Return all Python source files.
        """

        logger.info(
            "Scanning workspace: %s",
            self.root,
        )

        return sorted(
            self.root.rglob("*.py"),
        )

###############################################################################
# Compile File
###############################################################################

    def compile_file(
        self,
        file_path: Path,
    ) -> bool:
        """
        Compile a single Python file.
        """

        try:

            py_compile.compile(
                str(file_path),
                doraise=True,
            )

            return True

        except py_compile.PyCompileError as exc:

            error = CompileError(

                file=str(file_path),

                error_type=type(
                    exc.exc_value,
                ).__name__,

                message=str(
                    exc.exc_value,
                ),

                line=getattr(
                    exc.exc_value,
                    "lineno",
                    None,
                ),

                column=getattr(
                    exc.exc_value,
                    "offset",
                    None,
                ),
            )

            self.errors.append(
                error,
            )

            logger.error(
                "Compile failed: %s",
                file_path,
            )

            return False

###############################################################################
# Compile Workspace
###############################################################################

    def compile_workspace(
        self,
    ) -> dict[str, int]:
        """
        Compile the complete workspace.
        """

        self.errors.clear()

        scanned = 0

        compiled = 0

        for file in self.scan_files():

            scanned += 1

            if self.compile_file(
                file,
            ):

                compiled += 1

        return {

            "files": scanned,

            "compiled": compiled,

            "failed": len(
                self.errors,
            ),

        }
        ###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return compile recovery report.
        """

        summary = self.compile_workspace()

        return {

            **summary,

            "errors": [

                asdict(error)

                for error in self.errors

            ],

        }

###############################################################################
# Summary
###############################################################################

    def summary(
        self,
    ) -> str:
        """
        Return a human-readable summary.
        """

        report = self.report()

        lines = [

            "GEETA AI ENGINE",
            "Compile Recovery Report",
            "",

            f"Files Scanned : {report['files']}",
            f"Compiled      : {report['compiled']}",
            f"Failed        : {report['failed']}",
            "",

        ]

        if self.errors:

            lines.append(
                "Broken Files:"
            )

            for error in self.errors:

                lines.append(

                    f"- {error.file} "
                    f"({error.error_type})"

                )

        else:

            lines.append(
                "No compile errors detected."
            )

        return "\n".join(
            lines,
        )

###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, Any]:
        """
        Return diagnostics.
        """

        report = self.report()

        return {

            "engine": "CompileRecovery",

            "version": "3.1.0",

            "root": str(
                self.root,
            ),

            "healthy": (
                report["failed"] == 0
            ),

            "report": report,

        }
        ###############################################################################
# Export JSON
###############################################################################

    def export_json(
        self,
        file_path: str | Path,
    ) -> Path:
        """
        Export compile report to JSON.
        """

        path = Path(file_path)

        report = self.report()

        path.write_text(

            json.dumps(

                report,

                indent=4,

                ensure_ascii=False,

            ),

            encoding="utf-8",

        )

        logger.info(
            "Compile report exported: %s",
            path,
        )

        return path

###############################################################################
# Clear Errors
###############################################################################

    def clear_errors(
        self,
    ) -> None:
        """
        Clear collected compile errors.
        """

        self.errors.clear()

###############################################################################
# Ready
###############################################################################

    def is_ready(
        self,
    ) -> bool:
        """
        Return True if recovery engine is ready.
        """

        return self.root.exists()

###############################################################################
# Representation
###############################################################################

    def __repr__(
        self,
    ) -> str:

        return (

            f"{self.__class__.__name__}("

            f"root='{self.root}', "

            f"errors={len(self.errors)})"

        )

###############################################################################
# Global Instance
###############################################################################

compile_recovery = CompileRecovery()

###############################################################################
# Exports
###############################################################################

__all__ = [

    "CompileError",

    "CompileRecovery",

    "compile_recovery",

]