"""
==============================================================================
GEETA AI Engine

File        : chat_agent.py
Package     : agents
Description : AI Chat Agent

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Any

from agents.base_agent import BaseAgent
from agents.agent_manager import agent_manager
from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Chat Agent
###############################################################################


class ChatAgent(BaseAgent):
    """
    Primary conversational AI agent.

    Responsibilities:

    - Natural language understanding
    - Intent detection
    - Multi-agent orchestration
    - Conversation context
    - AI request routing
    - Response generation
    """

    def __init__(self) -> None:

        super().__init__(
            name="chat_agent",
            description="Primary AI Conversation Agent",
        )

    ###########################################################################

    def can_handle(
        self,
        context: dict[str, Any],
    ) -> bool:
        """
        Chat agent accepts any chat request.
        """

        return context.get("type") in {
            "chat",
            "conversation",
            "assistant",
            "question",
            "request",
        }

    ###########################################################################

    def execute(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Execute conversational request.
        """

        logger.info(
            "Chat Agent executing..."
        )

        intent = self.detect_intent(
            context,
        )

        return {
            "agent": self.name,
            "intent": intent,
            "summary": self._build_summary(
                intent,
            ),
            "target_agent": self.select_agent(
                intent,
            ),
            "prompt": self.build_prompt(
                context,
            ),
            "status": "ready",
        }

    ###########################################################################

    def detect_intent(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Detect high-level user intent.
        """

        text = str(
            context.get(
                "message",
                "",
            )
        ).lower()

        if "debug" in text or "error" in text:
            return "debug"

        if "review" in text:
            return "review"

        if "refactor" in text:
            return "refactor"

        if "generate" in text:
            return "generate"

        if "test" in text:
            return "test"

        if "document" in text:
            return "documentation"

        if "git" in text:
            return "git"

        return "general"

    ###########################################################################

    def _build_summary(
        self,
        intent: str,
    ) -> str:
        """
        Build chat summary.
        """

        return (
            f"Detected user intent: {intent}"
        )
###############################################################################
# Agent Selection
###############################################################################

    def select_agent(
        self,
        intent: str,
    ) -> str:
        """
        Select the most appropriate agent.
        """

        mapping = {
            "debug": "debug_agent",
            "review": "code_review_agent",
            "refactor": "refactor_agent",
            "generate": "code_generation_agent",
            "test": "test_generation_agent",
            "documentation": "documentation_agent",
            "git": "git_agent",
        }

        return mapping.get(
            intent,
            "chat_agent",
        )

###############################################################################
# Prompt Builder
###############################################################################

    def build_prompt(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Build conversation prompt.
        """

        return f"""
You are GEETA AI, an enterprise software engineering assistant.

User Request:

{context.get("message")}

Project Context:

{context.get("project_context")}

Workspace:

{context.get("workspace")}

Conversation History:

{context.get("history")}

Requirements:

1. Understand the user's intent.
2. Choose the most suitable specialized agent.
3. Produce an accurate response.
4. Follow the project architecture.
5. Preserve coding standards.
6. Minimize unnecessary code changes.
7. Explain important decisions.
8. Return structured Markdown.
""".strip()

###############################################################################
# Routing
###############################################################################

    def route(
        self,
        context: dict[str, Any],
    ) -> Any:
        """
        Route request to the selected agent.
        """

        intent = self.detect_intent(
            context,
        )

        agent_name = self.select_agent(
            intent,
        )

        if (
            agent_name == self.name
            or not agent_manager.exists(agent_name)
        ):
            return self.execute(context)

        return agent_manager.execute(
            agent_name,
            context,
        )

###############################################################################
# Report
###############################################################################

    def create_report(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Build structured chat report.
        """

        intent = self.detect_intent(
            context,
        )

        return {
            "agent": self.name,
            "intent": intent,
            "selected_agent": self.select_agent(
                intent,
            ),
            "summary": self._build_summary(
                intent,
            ),
            "prompt": self.build_prompt(
                context,
            ),
        }


###############################################################################
# Exports
###############################################################################

__all__ = [
    "ChatAgent",
]