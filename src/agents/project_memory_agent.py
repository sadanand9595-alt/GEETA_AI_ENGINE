"""
==============================================================================
GEETA AI Engine

File        : project_memory_agent.py
Package     : agents
Description : AI Project Memory Agent

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
# Project Memory Agent
###############################################################################


class ProjectMemoryAgent(BaseAgent):
    """
    AI agent responsible for maintaining
    long-term project memory.

    Responsibilities:

    - Project Knowledge
    - Symbol Memory
    - Architecture Memory
    - AI Decision History
    - Coding Pattern Tracking
    - Project Context
    """

    def __init__(self) -> None:

        super().__init__(
            name="project_memory_agent",
            description="AI Project Memory",
        )

    ###########################################################################

    def can_handle(
        self,
        context: dict[str, Any],
    ) -> bool:
        """
        Determine whether this agent
        can process project memory requests.
        """

        return context.get("type") in {
            "memory",
            "project_memory",
            "knowledge",
            "context",
            "workspace_memory",
        }

    ###########################################################################

    def execute(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Execute project memory request.
        """

        logger.info(
            "Project Memory Agent executing..."
        )

        return {
            "agent": self.name,
            "summary": self._build_summary(
                context,
            ),
            "prompt": self.build_prompt(
                context,
            ),
            "workspace": context.get(
                "workspace",
            ),
            "status": "ready",
        }

    ###########################################################################

    def _build_summary(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Build project memory summary.
        """

        workspace = context.get(
            "workspace",
            "Unknown Workspace",
        )

        return (
            f"Project memory analysis for "
            f"{workspace}"
        )
###############################################################################
# Memory Category
###############################################################################

    def detect_memory_category(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Determine the category of project memory.
        """

        request_type = str(
            context.get(
                "type",
                "",
            )
        ).lower()

        mapping = {
            "memory": "General Memory",
            "project_memory": "Project Knowledge",
            "knowledge": "Knowledge Base",
            "context": "Context Retrieval",
            "workspace_memory": "Workspace Memory",
        }

        return mapping.get(
            request_type,
            "General Memory",
        )


###############################################################################
# Prompt Builder
###############################################################################

    def build_prompt(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Build AI project memory prompt.
        """

        return f"""
You are GEETA AI's long-term project memory engine.

Workspace:
{context.get("workspace")}

Current File:
{context.get("file")}

Current Request:
{context.get("request")}

Project Symbols:
{context.get("symbols")}

Architecture Context:
{context.get("architecture")}

Previous Decisions:
{context.get("history")}

Requirements:

1. Retrieve relevant project knowledge.
2. Preserve architectural consistency.
3. Reuse existing symbols.
4. Avoid duplicate implementations.
5. Respect project coding patterns.
6. Consider previous AI decisions.
7. Maintain long-term project consistency.
8. Return structured Markdown.
""".strip()


###############################################################################
# Report
###############################################################################

    def create_report(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Create structured project memory report.
        """

        return {
            "agent": self.name,
            "memory_category": (
                self.detect_memory_category(
                    context,
                )
            ),
            "summary": self._build_summary(
                context,
            ),
            "prompt": self.build_prompt(
                context,
            ),
            "workspace": context.get(
                "workspace",
            ),
            "file": context.get(
                "file",
            ),
        }


###############################################################################
# Exports
###############################################################################

__all__ = [
    "ProjectMemoryAgent",
]