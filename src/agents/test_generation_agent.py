"""
==============================================================================
GEETA AI Engine

File        : test_generation_agent.py
Package     : agents
Description : AI Test Generation Agent

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
# Test Generation Agent
###############################################################################


class TestGenerationAgent(BaseAgent):
    """
    AI agent responsible for generating production-quality tests.

    Responsibilities:

    - Unit Tests
    - Integration Tests
    - Functional Tests
    - Edge Case Tests
    - Mock Generation
    - Fixture Generation
    """

    def __init__(self) -> None:

        super().__init__(
            name="test_generation_agent",
            description="AI Test Generation Assistant",
        )

    ###########################################################################

    def can_handle(
        self,
        context: dict[str, Any],
    ) -> bool:
        """
        Determine whether this agent can
        generate tests for the supplied request.
        """

        return context.get("type") in {
            "generate_tests",
            "test_generation",
            "unit_test",
            "integration_test",
            "testing",
        }

    ###########################################################################

    def execute(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Execute test generation request.
        """

        logger.info(
            "Test Generation Agent executing..."
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
            "framework": context.get(
                "test_framework",
            ),
            "status": "ready",
        }

    ###########################################################################

    def _build_summary(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Build test generation summary.
        """

        file = context.get(
            "file",
            "Unknown File",
        )

        framework = context.get(
            "test_framework",
            "Default",
        )

        return (
            f"Generate tests for "
            f"{file} using {framework}"
        )
###############################################################################
# Test Type Detection
###############################################################################


    def detect_test_type(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Determine the type of test to generate.
        """

        request_type = str(
            context.get(
                "type",
                "",
            )
        ).lower()

        mapping = {
            "unit_test": "Unit Test",
            "integration_test": "Integration Test",
            "generate_tests": "Test Suite",
            "test_generation": "Test Suite",
            "testing": "General Testing",
        }

        return mapping.get(
            request_type,
            "General Test",
        )


###############################################################################
# Prompt Builder
###############################################################################


    def build_prompt(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Build AI test generation prompt.
        """

        return f"""
You are a Senior Software Test Engineer.

Generate production-quality automated tests.

Language:
{context.get("language")}

Source File:
{context.get("file")}

Testing Framework:
{context.get("test_framework")}

Source Code:

{context.get("code")}

Requirements:

1. Generate complete unit tests.
2. Include integration tests where appropriate.
3. Cover edge cases.
4. Cover error handling.
5. Generate mocks and fixtures.
6. Maximize test coverage.
7. Follow testing best practices.
8. Ensure tests are deterministic.
9. Add descriptive test names.
10. Return executable test code only.
""".strip()


###############################################################################
# Report
###############################################################################


    def create_report(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Create structured test generation report.
        """

        return {
            "agent": self.name,
            "test_type": self.detect_test_type(
                context,
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
            "framework": context.get(
                "test_framework",
            ),
            "file": context.get(
                "file",
            ),
        }


###############################################################################
# Exports
###############################################################################

__all__ = [
    "TestGenerationAgent",
]