"""
==============================================================================
GEETA AI Engine

File        : code_review_engine.py
Package     : engine
Description : AI Code Review Engine

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
# Code Review Engine
###############################################################################


class CodeReviewEngine:
    """
    AI-powered code review engine.

    Responsibilities

    - Static code review
    - Security review
    - Performance review
    - Architecture review
    - Technical debt detection
    - AI review report generation
    """

    def __init__(self) -> None:

        logger.info(
            "Code Review Engine initialized."
        )

    ###########################################################################

    def review(
        self,
        source: str,
        language: str = "python",
        review_type: str = "general",
        **kwargs: Any,
    ) -> str:
        """
        Review source code.
        """

        logger.info(
            "Starting AI code review..."
        )

        provider = (
            provider_manager.active_provider()
        )

        prompt = self.build_prompt(
            source=source,
            language=language,
            review_type=review_type,
        )

        return provider.generate(
            prompt,
            **kwargs,
        )

    ###########################################################################

    def build_prompt(
        self,
        source: str,
        language: str,
        review_type: str,
    ) -> str:
        """
        Build review prompt.
        """

        context = (
            context_builder.build_prompt_context(
                "Review the following code."
            )
        )

        return f"""
{context}

Task

Perform a professional code review.

Review Type

{review_type}

Language

{language}

Code

```{language}
{source}
###############################################################################
# Security Review
###############################################################################

    def security_review(
        self,
        source: str,
        language: str = "python",
    ) -> str:
        """
        Perform a security-focused review.
        """

        return self.review(
            source=source,
            language=language,
            review_type="security",
        )

###############################################################################
# Performance Review
###############################################################################

    def performance_review(
        self,
        source: str,
        language: str = "python",
    ) -> str:
        """
        Perform a performance-focused review.
        """

        return self.review(
            source=source,
            language=language,
            review_type="performance",
        )

###############################################################################
# Quality Score
###############################################################################

    def quality_score(
        self,
        source: str,
    ) -> dict[str, Any]:
        """
        Return a basic quality score.

        This implementation is intentionally simple.
        Future versions will calculate metrics using
        AST analysis and project intelligence.
        """

        lines = len(source.splitlines())

        return {
            "score": 100,
            "lines": lines,
            "rating": "Excellent",
        }

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return engine statistics.
        """

        provider = (
            provider_manager.active_provider()
        )

        return {
            "provider": provider.name,
            "model": provider.model,
            "workspace_health": (
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
            "technical_debt": (
                self.technical_debt()
            ),
            "provider": (
                provider_manager
                .active_provider()
                .metadata()
            ),
        }

###############################################################################
# Global Engine
###############################################################################

code_review_engine = CodeReviewEngine()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "CodeReviewEngine",
    "code_review_engine",
]