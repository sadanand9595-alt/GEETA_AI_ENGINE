"""
==============================================================================
GEETA AI ENGINE

File        : code_guard.py
Package     : tools
Description : Enterprise AI Code Guard

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

###############################################################################
# Imports
###############################################################################

import ast
import py_compile
import tempfile

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Validation Result
###############################################################################


@dataclass(slots=True)
class ValidationResult:
    """
    Validation result.
    """

    success: bool = True

    errors: list[str] = field(
        default_factory=list,
    )

    warnings: list[str] = field(
        default_factory=list,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

###############################################################################
# Code Guard
###############################################################################


class CodeGuard:
    """
    Enterprise source validation engine.

    Responsibilities

    - Syntax validation
    - AST validation
    - Compile validation
    - Forbidden text detection
    - Duplicate header detection
    - Triple quote validation
    - Import validation
    """

    ###########################################################################

    FORBIDDEN_TEXT = (

        "After File #",

        "Next Response",

        "Continue in next message",

        "Part 1/",

        "Part 2/",

        "Part 3/",

        "Part 4/",

        "Will Implement",

    )

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        logger.info(
            "Code Guard initialized."
        )
        ###############################################################################
# Validate Source
###############################################################################

    def validate_source(
        self,
        source: str,
    ) -> ValidationResult:
        """
        Validate Python source code.
        """

        result = ValidationResult()

        #######################################################################
        # Forbidden Text
        #######################################################################

        for text in self.FORBIDDEN_TEXT:

            if text in source:

                result.success = False

                result.errors.append(
                    f"Forbidden text detected: {text}"
                )

        #######################################################################
        # AST Validation
        #######################################################################

        try:

            ast.parse(
                source,
            )

        except SyntaxError as exc:

            result.success = False

            result.errors.append(
                f"SyntaxError: {exc}"
            )

        #######################################################################
        # Metadata
        #######################################################################

        result.metadata = {

            "characters": len(
                source,
            ),

            "lines": len(
                source.splitlines(),
            ),

        }

        return result

###############################################################################
# Validate File
###############################################################################

    def validate_file(
        self,
        file_path: str | Path,
    ) -> ValidationResult:
        """
        Validate a Python source file.
        """

        path = Path(
            file_path,
        )

        if not path.exists():

            result = ValidationResult(
                success=False,
            )

            result.errors.append(
                "File does not exist."
            )

            return result

        source = path.read_text(
            encoding="utf-8",
        )

        return self.validate_source(
            source,
        )

###############################################################################
# AST Check
###############################################################################

    def check_ast(
        self,
        source: str,
    ) -> bool:
        """
        Return True if AST parsing succeeds.
        """

        try:

            ast.parse(
                source,
            )

            return True

        except SyntaxError:

            return False
            ###############################################################################
# Compile Check
###############################################################################

    def check_compile(
        self,
        source: str,
    ) -> bool:
        """
        Return True if source compiles successfully.
        """

        try:

            with tempfile.NamedTemporaryFile(
                suffix=".py",
                delete=False,
                mode="w",
                encoding="utf-8",
            ) as temp:

                temp.write(source)

                temp_path = Path(
                    temp.name,
                )

            py_compile.compile(
                str(temp_path),
                doraise=True,
            )

            temp_path.unlink(
                missing_ok=True,
            )

            return True

        except Exception:

            try:

                temp_path.unlink(
                    missing_ok=True,
                )

            except Exception:
                pass

            return False

###############################################################################
# Triple Quote Check
###############################################################################

    def check_triple_quotes(
        self,
        source: str,
    ) -> bool:
        """
        Detect unclosed triple quoted strings.
        """

        double_quotes = source.count(
            '"""'
        )

        single_quotes = source.count(
            "'''"
        )

        return (
            double_quotes % 2 == 0
            and
            single_quotes % 2 == 0
        )

###############################################################################
# Duplicate Header Check
###############################################################################

    def check_duplicate_header(
        self,
        source: str,
    ) -> bool:
        """
        Detect duplicated file headers.
        """

        return (
            source.count(
                "=============================================================================="
            )
            <= 2
        )

###############################################################################
# Indentation Check
###############################################################################

    def check_indentation(
        self,
        source: str,
    ) -> bool:
        """
        Detect indentation issues.
        """

        try:

            compile(
                source,
                "<code_guard>",
                "exec",
            )

            return True

        except IndentationError:

            return False
            ###############################################################################
# Full Validation
###############################################################################

    def validate(
        self,
        source: str,
    ) -> ValidationResult:
        """
        Perform complete source validation.
        """

        result = self.validate_source(
            source,
        )

        #######################################################################
        # Compile
        #######################################################################

        if not self.check_compile(
            source,
        ):

            result.success = False

            result.errors.append(
                "Compile validation failed."
            )

        #######################################################################
        # Triple Quotes
        #######################################################################

        if not self.check_triple_quotes(
            source,
        ):

            result.success = False

            result.errors.append(
                "Unterminated triple quoted string detected."
            )

        #######################################################################
        # Duplicate Header
        #######################################################################

        if not self.check_duplicate_header(
            source,
        ):

            result.success = False

            result.errors.append(
                "Duplicate file header detected."
            )

        #######################################################################
        # Indentation
        #######################################################################

        if not self.check_indentation(
            source,
        ):

            result.success = False

            result.errors.append(
                "Indentation validation failed."
            )

        #######################################################################
        # Summary
        #######################################################################

        result.metadata["checks"] = {

            "ast": self.check_ast(
                source,
            ),

            "compile": self.check_compile(
                source,
            ),

            "triple_quotes": self.check_triple_quotes(
                source,
            ),

            "duplicate_header": self.check_duplicate_header(
                source,
            ),

            "indentation": self.check_indentation(
                source,
            ),

        }

        return result

###############################################################################
# Report
###############################################################################

    def report(
        self,
        source: str,
    ) -> dict[str, Any]:
        """
        Return validation report.
        """

        validation = self.validate(
            source,
        )

        return {

            "success": validation.success,

            "errors": validation.errors,

            "warnings": validation.warnings,

            "metadata": validation.metadata,

        }

###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
        source: str,
    ) -> dict[str, Any]:
        """
        Return Code Guard diagnostics.
        """

        report = self.report(
            source,
        )

        return {

            "engine": "CodeGuard",

            "version": "3.2.0",

            "healthy": report["success"],

            "report": report,

        }
        ###############################################################################
# Export JSON
###############################################################################

    def export_json(
        self,
        source: str,
        file_path: str | Path,
    ) -> Path:
        """
        Export validation report to JSON.
        """

        import json

        path = Path(file_path)

        report = self.report(
            source,
        )

        path.write_text(
            json.dumps(
                report,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        logger.info(
            "Validation report exported: %s",
            path,
        )

        return path

###############################################################################
# Representation
###############################################################################

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.__class__.__name__}()"
        )

###############################################################################
# Global Instance
###############################################################################

code_guard = CodeGuard()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "ValidationResult",
    "CodeGuard",
    "code_guard",
]