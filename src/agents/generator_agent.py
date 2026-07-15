"""
==============================================================================
GEETA AI Engine

File        : project_generator_agent.py
Package     : agents
Description : AI Project Generator Agent

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
# Project Generator Agent
###############################################################################


class ProjectGeneratorAgent(BaseAgent):
    """
    AI agent responsible for generating
    complete software projects.

    Responsibilities:

    - Project Architecture
    - Folder Structure
    - Source Code Generation
    - Configuration Files
    - Documentation
    - Build Scripts
    """

    def __init__(self) -> None:

        super().__init__(
            name="project_generator_agent",
            description="AI Project Generator",
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
            "project",
            "generate_project",
            "scaffold",
            "boilerplate",
        }

    ###########################################################################

    def execute(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Execute project generation analysis.
        """

        logger.info(
            "Project Generator Agent executing..."
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
                "framework",
            ),
            "status": "ready",
        }

    ###########################################################################

    def _build_summary(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Build project generation summary.
        """

        project_name = context.get(
            "project_name",
            "New Project",
        )

        language = context.get(
            "language",
            "Unknown",
        )

        framework = context.get(
            "framework",
            "None",
        )

        return (
            f"Generate '{project_name}' "
            f"using {language}"
            f" ({framework})"
        )
###############################################################################
# Project Type Detection
###############################################################################

    def detect_project_type(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Determine the type of project to generate.
        """

        framework = str(
            context.get(
                "framework",
                "",
            )
        ).lower()

        if framework in {
            "fastapi",
            "flask",
            "django",
        }:
            return "Backend"

        if framework in {
            "react",
            "vue",
            "angular",
            "nextjs",
            "next",
        }:
            return "Frontend"

        if framework in {
            "electron",
            "pyside6",
            "pyqt6",
            "qt",
        }:
            return "Desktop"

        return "General"

###############################################################################
# Prompt Builder
###############################################################################

    def build_prompt(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Build AI project generation prompt.
        """

        return f"""
You are a Principal Software Architect.

Generate a complete production-ready software project.

Project Name:
{context.get("project_name")}

Language:
{context.get("language")}

Framework:
{context.get("framework")}

Requirements:

{context.get("requirements")}

Generate:

1. Recommended architecture
2. Folder structure
3. Configuration files
4. Source code
5. Dependency list
6. README
7. Build instructions
8. Deployment instructions
9. Best practices
10. Scalability recommendations

Follow SOLID principles and enterprise architecture.

Return the result in structured Markdown.
""".strip()

###############################################################################
# Report
###############################################################################

    def create_report(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Create structured project generation report.
        """

        return {
            "agent": self.name,
            "project_type": self.detect_project_type(
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
                "framework",
            ),
            "project_name": context.get(
                "project_name",
            ),
        }


###############################################################################
# Exports
###############################################################################

__all__ = [
    "ProjectGeneratorAgent",
]