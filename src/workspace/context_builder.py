"""
==============================================================================
GEETA AI Engine

File        : context_builder.py
Package     : workspace
Description : AI Context Builder

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Any

from config.logger import get_logger

from memory.conversation_memory import ConversationMemory
from memory.project_memory import ProjectMemory
from memory.semantic_memory import SemanticMemory
from memory.session_memory import SessionMemory
from memory.symbol_memory import SymbolMemory

from workspace.project_analyzer import project_analyzer
from workspace.workspace_manager import workspace_manager

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Context Builder
###############################################################################


class ContextBuilder:
    """
    Builds AI-ready context from the workspace.

    Sources:

    - Workspace
    - Project Analysis
    - Conversation Memory
    - Project Memory
    - Semantic Memory
    - Symbol Memory
    - Session Memory
    """

    def __init__(self) -> None:

        self._conversation = ConversationMemory()

        self._project = ProjectMemory()

        self._semantic = SemanticMemory()

        self._session = SessionMemory()

        self._symbols = SymbolMemory()

        logger.info(
            "Context Builder initialized."
        )

    ###########################################################################

    def build(
        self,
        request: str,
    ) -> dict[str, Any]:
        """
        Build complete AI context.
        """

        logger.info(
            "Building AI context."
        )

        return {
            "request": request,
            "workspace": self.workspace_context(),
            "project": self.project_context(),
            "conversation": self.conversation_context(),
            "session": self.session_context(),
            "symbols": self.symbol_context(),
            "semantic": self.semantic_context(),
        }

    ###########################################################################

    def workspace_context(
        self,
    ) -> dict[str, Any]:
        """
        Workspace information.
        """

        return workspace_manager.report()

    ###########################################################################

    def project_context(
        self,
    ) -> dict[str, Any]:
        """
        Project analysis.
        """

        return project_analyzer.report()

    ###########################################################################

    def conversation_context(
        self,
    ) -> dict[str, Any]:
        """
        Conversation context.
        """

        return {
            "summary": self._conversation.summarize(),
            "recent": self._conversation.recent(10),
        }

    ###########################################################################

    def session_context(
        self,
    ) -> dict[str, Any]:
        """
        Session context.
        """

        return self._session.report()
###############################################################################
# Symbol Context
###############################################################################

    def symbol_context(
        self,
    ) -> dict[str, Any]:
        """
        Build symbol context.
        """

        return self._symbols.report()

###############################################################################
# Semantic Context
###############################################################################

    def semantic_context(
        self,
    ) -> dict[str, Any]:
        """
        Build semantic context.
        """

        return self._semantic.report()

###############################################################################
# AI Prompt Context
###############################################################################

    def build_prompt_context(
        self,
        request: str,
    ) -> str:
        """
        Build compact prompt context for the LLM.
        """

        context = self.build(
            request,
        )

        return f"""
User Request:
{context["request"]}

Workspace:
{context["workspace"]}

Project:
{context["project"]}

Conversation:
{context["conversation"]}

Session:
{context["session"]}

Symbols:
{context["symbols"]}

Semantic Memory:
{context["semantic"]}
""".strip()

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return context statistics.
        """

        return {
            "conversation_messages": len(
                self._conversation.messages()
            ),
            "project_entries": len(
                self._project.keys()
            ),
            "symbols": len(
                self._symbols.all_symbols()
            ),
            "semantic_documents": len(
                self._semantic.keys()
            ),
        }

###############################################################################
# Global Context Builder
###############################################################################

context_builder = ContextBuilder()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "ContextBuilder",
    "context_builder",
]