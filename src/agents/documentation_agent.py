"""
==============================================================================
GEETA AI Engine

File        : documentation_agent.py
Package     : agents
Description : AI Documentation Agent

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
# Documentation Agent
###############################################################################


class DocumentationAgent(BaseAgent):
    """
    AI agent responsible for generating
    high-quality software documentation.

    Responsibilities:

    - Docstrings
    - README generation
    - API documentation
    - Module documentation
    - Class documentation
    - Function documentation
    """

    def __init__(self) -> None:

        super().__init__(
            name="documentation_agent",
            description="AI Documentation Assistant",
        )

    ###########################################################################

    def can_handle(
        self,
        context: dict[str, Any],
    ) -> bool:
        """
        Determine whether this agent
        can process the supplied request.
        """

        return context.get("type") in {
            "documentation",
            "docs",
            "docstring",
            "readme",
            "api_docs",
        }

    ###########################################################################

    def execute(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Execute documentation analysis.
        """

        logger.info(
            "Documentation Agent executing..."
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
        Build documentation summary.
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
            f"Documentation generation for "
            f"{file} ({language})"
        )
"""
==============================================================================
GEETA AI Engine

File        : documentation_agent.py
Package     : agents
Description : AI Documentation Agent

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations


from agents.base_agent import BaseAgent
from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Documentation Agent
###############################################################################


class DocumentationAgent(BaseAgent):
    """
    AI agent responsible for generating
    high-quality software documentation.

    Responsibilities:

    - Docstrings
    - README generation
    - API documentation
    - Module documentation
    - Class documentation
    - Function documentation
    """

    def __init__(self) -> None:

        super().__init__(
            name="documentation_agent",
            description="AI Documentation Assistant",
        )

    ###########################################################################

    def can_handle(
        self,
        context: dict[str, Any],
    ) -> bool:
        """
        Determine whether this agent
        can process the supplied request.
        """

        return context.get("type") in {
            "documentation",
            "docs",
            "docstring",
            "readme",
            "api_docs",
        }

    ###########################################################################

    def execute(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Execute documentation analysis.
        """

        logger.info(
            "Documentation Agent executing..."
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
        Build documentation summary.
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
            f"Documentation generation for "
            f"{file} ({language})"
        )