"""
==============================================================================
GEETA AI Engine

File        : code_review_agent.py
Package     : agents
Description : AI Code Review Agent

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Any

from agents.base_agent import BaseAgent
from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Code Review Agent
###############################################################################


class CodeReviewAgent(BaseAgent):
    """
    AI agent responsible for reviewing source code.

    Capabilities:

    - Code Quality Analysis
    - Bug Detection
    - Security Review
    - Performance Review
    - Style Review
    - Best Practices
    """

    def __init__(self) -> None:

        super().__init__(
            name="code_review_agent",
            description="AI Code Review Assistant",
        )

    ###########################################################################

    def can_handle(
        self,
        context: dict[str, Any],
    ) -> bool:
        """
        Determine whether this agent can
        review the supplied context.
        """

        return context.get("type") in {
            "review",
            "code_review",
            "source_code",
        }

    ###########################################################################

    def execute(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Execute code review.
        """

        logger.info(
            "Code Review Agent executing..."
        )

        return {
            "agent": self.name,
            "language": context.get("language"),
            "summary": self._build_summary(
                context
            ),
            "prompt": self.build_prompt(
                context
            ),
            "status": "ready",
        }

    ###########################################################################

    def _build_summary(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Build review summary.
        """

        file = context.get(
            "file",
            "Unknown File",
        )

        language = context.get(
            "language",
            "Unknown",
        )

        return (
            f"Review requested for "
            f"{file} ({language})"
        )
###############################################################################
# Severity
###############################################################################

    def detect_severity(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Determine review priority.
        """

        findings = context.get(
            "findings",
            [],
        )

        if len(findings) >= 10:
            return "critical"

        if len(findings) >= 5:
            return "high"

        if len(findings) >= 2:
            return "medium"

        return "low"

###############################################################################
# Prompt Builder
###############################################################################

    def build_prompt(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Build AI review prompt.
        """

        return f"""
You are a Senior Software Engineer performing a production-grade code review.

Language:
{context.get("language")}

File:
{context.get("file")}

Source Code:

{context.get("code")}

Review Requirements:

1. Detect bugs.
2. Detect security issues.
3. Detect performance problems.
4. Detect code smells.
5. Check SOLID principles.
6. Check readability.
7. Suggest improvements.
8. Give an overall quality score (0-100).

Return the review in structured Markdown.
""".strip()

###############################################################################
# Report
###############################################################################

    def create_report(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Create structured review report.
        """

        return {
            "agent": self.name,
            "summary": self._build_summary(
                context,
            ),
            "severity": self.detect_severity(
                context,
            ),
            "prompt": self.build_prompt(
                context,
            ),
            "language": context.get(
                "language",
            ),
            "file": context.get(
                "file",
            ),
        }


###############################################################################
# Exports
###############################################################################

__all__ = [
    "CodeReviewAgent",
]
