"""
==============================================================================
GEETA AI Engine

File        : code_generation_agent.py
Package     : agents
Description : AI Code Generation Agent

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
# Code Generation Agent
###############################################################################


class CodeGenerationAgent(BaseAgent):
    """
    AI agent responsible for generating production-ready code.

    Responsibilities:

    - Function Generation
    - Class Generation
    - Module Generation
    - Unit Test Generation
    - API Generation
    - Boilerplate Generation
    """

    def __init__(self) -> None:

        super().__init__(
            name="code_generation_agent",
            description="AI Code Generation Assistant",
        )

    ###########################################################################

    def can_handle(
        self,
        context: dict[str, Any],
    ) -> bool:
        """
        Determine whether this agent can
        generate code for the supplied request.
        """

        return context.get("type") in {
            "generate_code",
            "code_generation",
            "generate",
            "implement",
            "create_code",
        }

    ###########################################################################

    def execute(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Execute code generation request.
        """

        logger.info(
            "Code Generation Agent executing..."
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
        Build generation summary.
        """

        task = context.get(
            "task",
            "Generate source code",
        )

        language = context.get(
            "language",
            "Unknown",
        )

        return (
            f"{task} ({language})"
        )
###############################################################################
# Generation Type
###############################################################################


    def detect_generation_type(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Determine the type of code to generate.
        """

        task = str(
            context.get(
                "task",
                "",
            )
        ).lower()

        if "function" in task:
            return "Function"

        if "class" in task:
            return "Class"

        if "module" in task:
            return "Module"

        if "api" in task:
            return "API"

        if "test" in task:
            return "Unit Test"

        if "script" in task:
            return "Script"

        return "General Code"


###############################################################################
# Prompt Builder
###############################################################################


    def build_prompt(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Build AI code generation prompt.
        """

        return f"""
You are a Principal Software Engineer.

Generate production-ready code.

Language:
{context.get("language")}

Task:
{context.get("task")}

Requirements:

{context.get("requirements")}

Coding Standards:

1. Production-ready implementation.
2. SOLID principles.
3. Type hints.
4. Proper error handling.
5. Logging where appropriate.
6. Clean architecture.
7. Complete implementation.
8. No placeholders.
9. Add documentation.
10. Include usage example if applicable.

Return only the generated code unless documentation is requested.
""".strip()


###############################################################################
# Report
###############################################################################


    def create_report(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Create structured generation report.
        """

        return {
            "agent": self.name,
            "generation_type": (
                self.detect_generation_type(
                    context,
                )
            ),
            "summary": self._build_summary(
                context,
            ),
            "prompt": self.build_prompt(
                context,
            ),
            "language": context.get(
                "language",
            ),
            "task": context.get(
                "task",
            ),
        }


###############################################################################
# Exports
###############################################################################

__all__ = [
    "CodeGenerationAgent",
]