"""
==============================================================================
GEETA AI Engine

File        : symbol_indexer.py
Package     : workspace
Description : Symbol Indexer

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from config.logger import get_logger

from memory.symbol_memory import SymbolMemory
from workspace.workspace_manager import workspace_manager

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Symbol Indexer
###############################################################################


class SymbolIndexer:
    """
    Builds the project symbol index.

    Responsibilities

    - Parse Python AST
    - Extract classes
    - Extract functions
    - Extract methods
    - Extract imports
    - Populate SymbolMemory
    """

    def __init__(self) -> None:

        self._memory = SymbolMemory()

        logger.info(
            "Symbol Indexer initialized."
        )

    ###########################################################################

    def build(
        self,
    ) -> None:
        """
        Build symbol index for the workspace.
        """

        logger.info(
            "Building symbol index..."
        )

        self._memory.clear()

        for file in workspace_manager.scan_files(
            "*.py",
        ):

            self.index_file(file)

        logger.info(
            "Symbol indexing completed."
        )

    ###########################################################################

    def index_file(
        self,
        file: Path,
    ) -> None:
        """
        Index a single Python source file.
        """

        try:

            source = file.read_text(
                encoding="utf-8",
            )

            tree = ast.parse(
                source,
                filename=str(file),
            )

            self._visit_tree(
                tree,
                file,
            )

        except Exception:

            logger.exception(
                "Failed to index %s",
                file,
            )

    ###########################################################################

    def _visit_tree(
        self,
        tree: ast.AST,
        file: Path,
    ) -> None:
        """
        Visit AST nodes.
        """

        for node in ast.walk(tree):

            if isinstance(
                node,
                ast.ClassDef,
            ):

                self._memory.add_symbol(
                    name=node.name,
                    symbol_type="class",
                    file=str(file),
                    line=node.lineno,
                )

            elif isinstance(
                node,
                ast.FunctionDef,
            ):

                self._memory.add_symbol(
                    name=node.name,
                    symbol_type="function",
                    file=str(file),
                    line=node.lineno,
                )
###############################################################################
# Import Extraction
###############################################################################

    def _extract_imports(
        self,
        tree: ast.AST,
        file: Path,
    ) -> None:
        """
        Extract import statements.
        """

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for alias in node.names:

                    self._memory.add_symbol(
                        name=alias.name,
                        symbol_type="import",
                        file=str(file),
                        line=node.lineno,
                    )

            elif isinstance(node, ast.ImportFrom):

                module = node.module or ""

                self._memory.add_symbol(
                    name=module,
                    symbol_type="import",
                    file=str(file),
                    line=node.lineno,
                )

###############################################################################
# Variable Extraction
###############################################################################

    def _extract_variables(
        self,
        tree: ast.AST,
        file: Path,
    ) -> None:
        """
        Extract global variables.
        """

        for node in ast.walk(tree):

            if isinstance(node, ast.Assign):

                for target in node.targets:

                    if isinstance(target, ast.Name):

                        self._memory.add_symbol(
                            name=target.id,
                            symbol_type="variable",
                            file=str(file),
                            line=node.lineno,
                        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return symbol index statistics.
        """

        return self._memory.statistics()

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return symbol indexing report.
        """

        return {
            "statistics": self.statistics(),
            "symbols": self._memory.report(),
        }

###############################################################################
# Build Override
###############################################################################

    def build(
        self,
    ) -> None:
        """
        Build complete symbol index.
        """

        self._memory.clear()

        for file in workspace_manager.scan_files("*.py"):

            try:

                source = file.read_text(
                    encoding="utf-8",
                )

                tree = ast.parse(
                    source,
                    filename=str(file),
                )

                self._visit_tree(
                    tree,
                    file,
                )

                self._extract_imports(
                    tree,
                    file,
                )

                self._extract_variables(
                    tree,
                    file,
                )

            except Exception:

                logger.exception(
                    "Failed to index %s",
                    file,
                )

###############################################################################
# Global Indexer
###############################################################################

symbol_indexer = SymbolIndexer()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "SymbolIndexer",
    "symbol_indexer",
]