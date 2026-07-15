"""
==============================================================================
GEETA AI Engine

File        : code_completion_engine.py
Package     : engine
Description : AI Code Completion Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Any

from config.logger import get_logger

from providers.provider_manager import provider_manager
from workspace.context_builder import context_builder

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Code Completion Engine
###############################################################################


class CodeCompletionEngine:
    """
    AI-powered code completion engine.

    Responsibilities

    - Inline completion
    - Multi-line completion
    - Context-aware completion
    - Whole-project completion
    - Provider routing
    """

    def __init__(self) -> None:

        logger.info(
            "Code Completion Engine initialized."
        )

    ###########################################################################

    def complete(
        self,
        prefix: str,
        language: str = "python",
        **kwargs: Any,
    ) -> str:
        """
        Generate code completion.
        """

        logger.info(
            "Generating completion..."
        )

        provider = (
            provider_manager.active_provider()
        )

        prompt = self.build_prompt(
            prefix,
            language,
        )

        return provider.generate(
            prompt,
            **kwargs,
        )

    ###########################################################################

    def build_prompt(
        self,
        prefix: str,
        language: str,
    ) -> str:
        """
        Build completion prompt.
        """

        context = (
            context_builder.build_prompt_context(
                "Complete the following code."
            )
        )

        return f"""
{context}

Language:
{language}

Code Prefix:

```{language}
{prefix}
###############################################################################
# Streaming Completion
###############################################################################

    def stream(
        self,
        prefix: str,
        language: str = "python",
        **kwargs: Any,
    ):
        """
        Stream code completion.

        Providers with native streaming should
        override this behavior.
        """

        yield self.complete(
            prefix=prefix,
            language=language,
            **kwargs,
        )

###############################################################################
# Completion Ranking
###############################################################################

    def rank(
        self,
        suggestions: list[str],
    ) -> list[str]:
        """
        Rank completion suggestions.

        Placeholder ranking strategy based on
        suggestion length.
        """

        return sorted(
            suggestions,
            key=len,
            reverse=True,
        )

###############################################################################
# Acceptance Tracking
###############################################################################

    def record_acceptance(
        self,
        accepted: bool,
    ) -> None:
        """
        Record completion feedback.
        """

        logger.info(
            "Completion accepted: %s",
            accepted,
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return completion engine statistics.
        """

        provider = (
            provider_manager.active_provider()
        )

        return {
            "provider": provider.name,
            "model": provider.model,
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return completion engine report.
        """

        return {
            "statistics": self.statistics(),
            "provider": (
                provider_manager.active_provider().metadata()
            ),
        }

###############################################################################
# Global Engine
###############################################################################

code_completion_engine = CodeCompletionEngine()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "CodeCompletionEngine",
    "code_completion_engine",
]