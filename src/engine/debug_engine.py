"""
==============================================================================
GEETA AI Engine

File        : debug_engine.py
Package     : engine
Description : AI Debug Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Any

from config.logger import get_logger

from providers.provider_manager import provider_manager

from workspace.context_builder import context_builder
from workspace.project_intelligence import (
    project_intelligence,
)

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Debug Engine
###############################################################################


class DebugEngine:
    """
    AI-powered debugging engine.

    Responsibilities

    - Runtime error analysis
    - Stack trace analysis
    - Root cause detection
    - AI fix generation
    - Log analysis
    - Crash diagnostics
    """

    def __init__(self) -> None:

        logger.info(
            "Debug Engine initialized."
        )

    ###########################################################################

    def debug(
        self,
        source: str,
        error: str,
        language: str = "python",
        **kwargs: Any,
    ) -> str:
        """
        Analyze and fix source code.
        """

        logger.info(
            "Starting AI debugging..."
        )

        provider = (
            provider_manager.active_provider()
        )

        prompt = self.build_prompt(
            source=source,
            error=error,
            language=language,
        )

        return provider.generate(
            prompt,
            **kwargs,
        )

    ###########################################################################

    def build_prompt(
        self,
        source: str,
        error: str,
        language: str,
    ) -> str:
        """
        Build debugging prompt.
        """

        context = (
            context_builder.build_prompt_context(
                "Debug the following code."
            )
        )

        return f"""
{context}

Task

Debug the following source code.

Language

{language}

Error

{error}

Source

```{language}
{source}
###############################################################################
# Stack Trace Analysis
###############################################################################

    def analyze_stacktrace(
        self,
        stacktrace: str,
    ) -> dict[str, Any]:
        """
        Analyze a stack trace.
        """

        lines = [
            line.strip()
            for line in stacktrace.splitlines()
            if line.strip()
        ]

        return {
            "frames": len(lines),
            "exception": (
                lines[-1]
                if lines
                else ""
            ),
        }

###############################################################################
# Log Analysis
###############################################################################

    def analyze_logs(
        self,
        logs: str,
    ) -> dict[str, Any]:
        """
        Analyze application logs.
        """

        errors = [
            line
            for line in logs.splitlines()
            if "error" in line.lower()
        ]

        warnings = [
            line
            for line in logs.splitlines()
            if "warning" in line.lower()
        ]

        return {
            "errors": len(errors),
            "warnings": len(warnings),
        }

###############################################################################
# Automatic Fix Suggestions
###############################################################################

    def suggest_fix(
        self,
        source: str,
        error: str,
    ) -> str:
        """
        Generate an AI fix suggestion.
        """

        return self.debug(
            source=source,
            error=error,
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return debug engine statistics.
        """

        provider = (
            provider_manager.active_provider()
        )

        return {
            "provider": provider.name,
            "model": provider.model,
            "workspace_health": (
                self.workspace_health()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return debug engine report.
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

debug_engine = DebugEngine()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "DebugEngine",
    "debug_engine",
]