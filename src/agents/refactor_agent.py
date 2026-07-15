"""
==============================================================================
GEETA AI Engine

File        : refactor_agent.py
Package     : agents
Description : AI Refactor Agent

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
# Refactor Agent
###############################################################################


class RefactorAgent(BaseAgent):
    """
    AI agent responsible for improving existing code.

    Responsibilities:

    - Refactoring
    - SOLID Improvements
    - Duplicate Code Detection
    - Maintainability
    - Readability
    - Performance Improvements
    """

    def __init__(self) -> None:

        super().__init__(
            name="refactor_agent",
            description="AI Refactoring Assistant",
        )

    ###########################################################################

    def can_handle(
        self,
        context: dict[str, Any],
    ) -> bool:
        """
        Determine whether this agent can
        process the supplied context.
        """

        return context.get("type") in {
            "refactor",
            "cleanup",
            "optimize",
            "improve",
        }

    ###########################################################################

    def execute(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Execute refactoring analysis.
        """

        logger.info(
            "Refactor Agent executing..."
        )

        return {
            "agent": self.name,
            "summary": self._build_summary(
                context,
            ),
            "prompt": self.build_prompt(
                context,
            ),
            "language": context.get(
                "language",
            ),
            "status": "ready",
        }

    ###########################################################################

    def _build_summary(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Build refactoring summary.
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
            f"Refactoring analysis for "
            f"{file} ({language})"
        )
###############################################################################
# Priority Detection
###############################################################################

    def detect_priority(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Determine refactoring priority.
        """

        issues = context.get(
            "issues",
            [],
        )

        if len(issues) >= 10:
            return "critical"

        if len(issues) >= 5:
            return "high"

        if len(issues) >= 2:
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
        Build AI refactoring prompt.
        """

        return f"""
You are a Senior Software Architect.

Analyze the following source code and perform a production-grade refactoring review.

Language:
{context.get("language")}

File:
{context.get("file")}

Code:

{context.get("code")}

Tasks:

1. Improve readability.
2. Remove duplicated code.
3. Apply SOLID principles.
4. Reduce complexity.
5. Improve maintainability.
6. Improve naming.
7. Suggest suitable design patterns.
8. Preserve existing functionality.
9. Generate refactored code where appropriate.

Return the response in structured Markdown.
""".strip()


###############################################################################
# Report
###############################################################################

    def create_report(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Create structured refactoring report.
        """

        return {
            "agent": self.name,
            "summary": self._build_summary(
                context,
            ),
            "priority": self.detect_priority(
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
    "RefactorAgent",
]