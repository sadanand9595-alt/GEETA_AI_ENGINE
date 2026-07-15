"""
==============================================================================
GEETA AI Engine

File        : refactoring_engine.py
Package     : engine
Description : AI Refactoring Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Any

from config.logger import get_logger

from providers.provider_manager import provider_manager

from workspace.context_builder import context_builder
from workspace.dependency_graph import dependency_graph
from workspace.project_intelligence import (
    project_intelligence,
)

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Refactoring Engine
###############################################################################


class RefactoringEngine:
    """
    AI-powered refactoring engine.

    Responsibilities

    - Code refactoring
    - Symbol rename
    - Function extraction
    - Method inlining
    - Import optimization
    - Cross-file refactoring
    """

    def __init__(self) -> None:

        logger.info(
            "Refactoring Engine initialized."
        )

    ###########################################################################

    def refactor(
        self,
        request: str,
        source: str,
        language: str = "python",
        **kwargs: Any,
    ) -> str:
        """
        Perform AI-assisted refactoring.
        """

        logger.info(
            "Starting refactoring..."
        )

        provider = (
            provider_manager.active_provider()
        )

        prompt = self.build_prompt(
            request=request,
            source=source,
            language=language,
        )

        return provider.generate(
            prompt,
            **kwargs,
        )

    ###########################################################################

    def build_prompt(
        self,
        request: str,
        source: str,
        language: str,
    ) -> str:
        """
        Build refactoring prompt.
        """

        context = (
            context_builder.build_prompt_context(
                request,
            )
        )

        return f"""
{context}

Task:
{request}

Language:
{language}

Code:

```{language}
{source}
###############################################################################
# Multi-file Refactoring
###############################################################################

    def refactor_files(
        self,
        files: dict[str, str],
        request: str,
        language: str = "python",
    ) -> dict[str, str]:
        """
        Refactor multiple files.
        """

        results: dict[str, str] = {}

        for filename, source in files.items():

            results[filename] = self.refactor(
                request=request,
                source=source,
                language=language,
            )

        return results

###############################################################################
# Symbol Rename
###############################################################################

    def rename_symbol(
        self,
        symbol: str,
        new_name: str,
    ) -> dict[str, Any]:
        """
        Build rename plan.
        """

        return {
            "symbol": symbol,
            "new_name": new_name,
            "impact": self.impact_analysis(
                symbol,
            ),
        }

###############################################################################
# Patch Generation
###############################################################################

    def generate_patch(
        self,
        original: str,
        modified: str,
    ) -> dict[str, str]:
        """
        Generate structured patch.
        """

        return {
            "original": original,
            "modified": modified,
        }

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return refactoring statistics.
        """

        provider = (
            provider_manager.active_provider()
        )

        return {
            "provider": provider.name,
            "model": provider.model,
            "project_health": (
                self.project_health()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return engine report.
        """

        return {
            "statistics": self.statistics(),
            "provider": (
                provider_manager
                .active_provider()
                .metadata()
            ),
        }

###############################################################################
# Global Engine
###############################################################################

refactoring_engine = RefactoringEngine()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "RefactoringEngine",
    "refactoring_engine",
]