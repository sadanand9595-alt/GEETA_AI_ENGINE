"""
==============================================================================
GEETA AI Engine

File        : code_generation_engine.py
Package     : engine
Description : AI Code Generation Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Any

from agents.agent_orchestrator import agent_orchestrator
from config.logger import get_logger
from providers.provider_manager import provider_manager
from workspace.context_builder import context_builder

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Code Generation Engine
###############################################################################


class CodeGenerationEngine:
    """
    Central AI code generation engine.

    Responsibilities

    - Code generation
    - Code completion
    - Prompt assembly
    - Multi-file generation
    - Provider routing
    - Context injection
    """

    def __init__(self) -> None:

        logger.info(
            "Code Generation Engine initialized."
        )

    ###########################################################################

    def generate(
        self,
        request: str,
        agent: str = "code_generator",
        **kwargs: Any,
    ) -> str:
        """
        Generate source code.
        """

        logger.info(
            "Generating code..."
        )

        return agent_orchestrator.execute(
            agent_name=agent,
            request=request,
            **kwargs,
        )

    ###########################################################################

    def completion(
        self,
        prefix: str,
    ) -> str:
        """
        Generate code completion.
        """

        provider = (
            provider_manager.active_provider()
        )

        prompt = (
            "Continue the following code.\n\n"
            f"{prefix}"
        )

        return provider.generate(
            prompt,
        )

    ###########################################################################

    def build_prompt(
        self,
        request: str,
    ) -> str:
        """
        Build AI prompt with project context.
        """

        return context_builder.build_prompt_context(
            request,
        )
###############################################################################
# Streaming Generation
###############################################################################

    def stream(
        self,
        request: str,
        agent: str = "code_generator",
        **kwargs: Any,
    ):
        """
        Stream generated code.

        This default implementation yields a single
        response. Providers supporting native streaming
        should override this behavior.
        """

        yield self.generate(
            request=request,
            agent=agent,
            **kwargs,
        )

###############################################################################
# Patch Generation
###############################################################################

    def generate_patch(
        self,
        original: str,
        modified: str,
    ) -> dict[str, str]:
        """
        Generate a structured patch.
        """

        return {
            "original": original,
            "modified": modified,
        }

###############################################################################
# Diff Generation
###############################################################################

    def generate_diff(
        self,
        original: str,
        modified: str,
    ) -> str:
        """
        Generate a unified diff.
        """

        import difflib

        return "".join(
            difflib.unified_diff(
                original.splitlines(
                    keepends=True,
                ),
                modified.splitlines(
                    keepends=True,
                ),
                fromfile="original",
                tofile="modified",
            )
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return engine statistics.
        """

        return {
            "active_provider": (
                provider_manager.active_provider().name
            ),
            "registered_agents": len(
                agent_orchestrator.statistics()[
                    "agents"
                ]
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
            "provider": (
                provider_manager.active_provider().metadata()
            ),
        }

###############################################################################
# Global Engine
###############################################################################

code_generation_engine = CodeGenerationEngine()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "CodeGenerationEngine",
    "code_generation_engine",
]