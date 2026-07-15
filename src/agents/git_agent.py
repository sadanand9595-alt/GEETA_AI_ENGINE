"""
==============================================================================
GEETA AI Engine

File        : git_agent.py
Package     : agents
Description : AI Git Agent

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
# Git Agent
###############################################################################


class GitAgent(BaseAgent):
    """
    AI agent responsible for analyzing Git repositories.

    Responsibilities:

    - Commit Analysis
    - Diff Analysis
    - Branch Analysis
    - Merge Conflict Assistance
    - Commit Message Generation
    - Repository Health Review
    """

    def __init__(self) -> None:

        super().__init__(
            name="git_agent",
            description="AI Git Assistant",
        )

    ###########################################################################

    def can_handle(
        self,
        context: dict[str, Any],
    ) -> bool:
        """
        Determine whether this agent can
        process Git-related requests.
        """

        return context.get("type") in {
            "git",
            "commit",
            "diff",
            "merge",
            "repository",
            "pull_request",
        }

    ###########################################################################

    def execute(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Execute Git analysis.
        """

        logger.info(
            "Git Agent executing..."
        )

        return {
            "agent": self.name,
            "summary": self._build_summary(
                context,
            ),
            "prompt": self.build_prompt(
                context,
            ),
            "repository": context.get(
                "repository",
            ),
            "status": "ready",
        }

    ###########################################################################

    def _build_summary(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Build Git analysis summary.
        """

        operation = context.get(
            "operation",
            "repository_analysis",
        )

        repository = context.get(
            "repository",
            "Unknown Repository",
        )

        return (
            f"{operation} for "
            f"{repository}"
        )
###############################################################################
# Git Operation Detection
###############################################################################

    def detect_operation(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Determine Git operation type.
        """

        operation = str(
            context.get(
                "operation",
                "",
            )
        ).lower()

        mapping = {
            "commit": "Commit Analysis",
            "diff": "Diff Review",
            "merge": "Merge Conflict Resolution",
            "pull_request": "Pull Request Review",
            "branch": "Branch Analysis",
            "history": "Repository History",
            "repository_analysis": "Repository Health",
        }

        return mapping.get(
            operation,
            "Git Analysis",
        )


###############################################################################
# Prompt Builder
###############################################################################

    def build_prompt(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Build AI Git analysis prompt.
        """

        return f"""
You are a Senior Software Engineer and Git expert.

Repository:
{context.get("repository")}

Operation:
{context.get("operation")}

Branch:
{context.get("branch")}

Commit Message:
{context.get("commit_message")}

Git Diff:

{context.get("diff")}

Requirements:

1. Analyze repository changes.
2. Detect possible bugs.
3. Review code quality.
4. Detect merge conflicts.
5. Suggest better commit messages.
6. Recommend Git best practices.
7. Identify risky changes.
8. Summarize modifications.
9. Suggest improvements.
10. Return the response in structured Markdown.
""".strip()


###############################################################################
# Report
###############################################################################

    def create_report(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Create structured Git analysis report.
        """

        return {
            "agent": self.name,
            "operation": self.detect_operation(
                context,
            ),
            "summary": self._build_summary(
                context,
            ),
            "prompt": self.build_prompt(
                context,
            ),
            "repository": context.get(
                "repository",
            ),
            "branch": context.get(
                "branch",
            ),
            "commit": context.get(
                "commit_message",
            ),
        }


###############################################################################
# Exports
###############################################################################

__all__ = [
    "GitAgent",
]