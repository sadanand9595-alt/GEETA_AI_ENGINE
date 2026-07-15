"""
==============================================================================
GEETA AI IDE

File        : context_manager.py
Package     : ai
Description : Enterprise AI Context Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing impot Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# AI Context
###############################################################################


@dataclass(slots=True)
class AIContext:
    """
    Complete AI execution context.
    """

    project_name: str = ""

    workspace_path: str = ""

    current_file: str = ""

    language: str = ""

    cursor_line: int = 0

    cursor_column: int = 0

    selected_text: str = ""

    diagnostics: list[str] = field(
        default_factory=list,
    )

    open_files: list[str] = field(
        default_factory=list,
    )

    changed_files: list[str] = field(
        default_factory=list,
    )

    symbols: list[str] = field(
        default_factory=list,
    )

    imports: list[str] = field(
        default_factory=list,
    )

    dependencies: list[str] = field(
        default_factory=list,
    )

    conversation: list[str] = field(
    default_factory=list,
    )

    memory: str = ""

    project_files: list[str] = field(
        default_factory=list,
    )

    git_branch: str = ""

    git_status: str = ""

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )
    ###############################################################################
# Conversation
###############################################################################

    def set_conversation(
        self,
        conversation: list[str],
    ) -> None:
        """
        Update conversation history.
        """

        self._context.conversation = list(
            conversation,
        )

###############################################################################
# Memory
###############################################################################

    def set_memory(
        self,
        memory: str,
    ) -> None:
        """
        Update AI memory.
        """

        self._context.memory = memory

###############################################################################
# Project Files
###############################################################################

    def set_project_files(
        self,
        files: list[str],
    ) -> None:
        """
        Update project files.
        """

        self._context.project_files = list(
            files,
        )

###############################################################################
# Git
###############################################################################

    def set_git(
        self,
        branch: str,
        status: str,
    ) -> None:
        """
        Update Git information.
        """

        self._context.git_branch = branch

        self._context.git_status = status

###############################################################################
# Metadata
###############################################################################

    def set_metadata(
        self,
        metadata: dict[str, Any],
    ) -> None:
        """
        Update metadata.
        """

        self._context.metadata = dict(
            metadata,
        )
###############################################################################
# Context Manager
###############################################################################


class ContextManager:
    """
    Enterprise AI Context Manager.

    Responsibilities

    - Workspace context
    - Symbol graph
    - Git context
    - Editor context
    - AI prompt context
    - Multi-file retrieval
    """

    ###########################################################################

    def __init__(self) -> None:

        self._context = AIContext()

        logger.info(
            "AI Context Manager initialized."
        )

###############################################################################
# Context
###############################################################################

    @property
    def context(
        self,
    ) -> AIContext:

        return self._context

###############################################################################
# Workspace
###############################################################################

    def set_workspace(
        self,
        project_name: str,
        workspace_path: str,
    ) -> None:
        """
        Set workspace information.
        """

        self._context.project_name = (
            project_name
        )

        self._context.workspace_path = (
            workspace_path
        )

###############################################################################
# Current File
###############################################################################

    def set_current_file(
        self,
        file_path: str,
        language: str,
    ) -> None:
        """
        Set current editor file.
        """

        self._context.current_file = (
            file_path
        )

        self._context.language = (
            language
        )

###############################################################################
# Cursor
###############################################################################

    def update_cursor(
        self,
        line: int,
        column: int,
    ) -> None:
        """
        Update cursor position.
        """

        self._context.cursor_line = line

        self._context.cursor_column = column

###############################################################################
# Selection
###############################################################################

    def update_selection(
        self,
        text: str,
    ) -> None:
        """
        Update selected text.
        """

        self._context.selected_text = text
###############################################################################
# Diagnostics
###############################################################################

    def set_diagnostics(
        self,
        diagnostics: list[str],
    ) -> None:
        """
        Update diagnostics.
        """

        self._context.diagnostics = list(
            diagnostics
        )

###############################################################################
# Open Files
###############################################################################

    def set_open_files(
        self,
        files: list[str],
    ) -> None:
        """
        Update open editor files.
        """

        self._context.open_files = list(
            files
        )

###############################################################################
# Changed Files
###############################################################################

    def set_changed_files(
        self,
        files: list[str],
    ) -> None:
        """
        Update changed files.
        """

        self._context.changed_files = list(
            files
        )

###############################################################################
# Symbols
###############################################################################

    def set_symbols(
        self,
        symbols: list[str],
    ) -> None:
        """
        Update workspace symbols.
        """

        self._context.symbols = list(
            symbols
        )

###############################################################################
# Dependencies
###############################################################################

    def set_dependencies(
        self,
        dependencies: list[str],
    ) -> None:
        """
        Update dependency graph.
        """

        self._context.dependencies = list(
            dependencies
        )
###############################################################################
# Prompt Context
###############################################################################

    def build_prompt_context(
        self,
    ) -> dict[str, object]:
        """
        Build prompt context for Prompt Engine.
        """

        return {

            "project_name": self._context.project_name,

            "workspace_path": self._context.workspace_path,

            "current_file": self._context.current_file,

            "language": self._context.language,

            "selected_text": self._context.selected_text,

            "diagnostics": list(
                self._context.diagnostics,
            ),

            "conversation": list(
                self._context.conversation,
            ),

            "memory": self._context.memory,

            "metadata": dict(
                self._context.metadata,
            ),

        }

###############################################################################
# Token Estimation
###############################################################################

    def estimate_tokens(
        self,
    ) -> int:
        """
        Estimate prompt token usage.
        """

        context = str(
            self.build_prompt_context(),
        )

        return max(
            1,
            len(context) // 4,
        )

###############################################################################
# Context Compression
###############################################################################

    def compress_context(
        self,
        max_tokens: int = 30000,
    ) -> dict[str, object]:
        """
        Return a prompt-safe context.
        """

        context = self.build_prompt_context()

        if self.estimate_tokens() <= max_tokens:

            return context

        context["conversation"] = (
            context["conversation"][-20:]
            if context["conversation"]
            else []
        )

        return context
###############################################################################
# Reset
###############################################################################

    def reset(
        self,
    ) -> None:
        """
        Reset context.
        """

        self._context = AIContext()

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return context statistics.
        """

        return {
            "open_files": len(
                self._context.open_files
            ),
            "changed_files": len(
                self._context.changed_files
            ),
            "diagnostics": len(
                self._context.diagnostics
            ),
            "symbols": len(
                self._context.symbols
            ),
            "dependencies": len(
                self._context.dependencies
            ),
            "conversation": len(
                self._context.conversation
            ),

            "project_files": len(
                self._context.project_files
            ),

            "metadata": len(
                self._context.metadata
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return context report.
        """

        return {
            "project": (
                self._context.project_name
            ),
            "workspace": (
                self._context.workspace_path
            ),
            "current_file": (
                self._context.current_file
            ),
            "language": (
                self._context.language
            ),
            "cursor": {
                "line": (
                    self._context.cursor_line
                ),
                "column": (
                    self._context.cursor_column
                ),
            },
            "statistics": (
                self.statistics()
            ),
            "git": {

                "branch": self._context.git_branch,

                "status": self._context.git_status,

            },

                "estimated_tokens": self.estimate_tokens(),
        }
###############################################################################
# Diagnostics
###############################################################################

        def diagnostics(
            self,
        ) -> dict[str, object]:
            """
            Return enterprise diagnostics.
            """

          return {

        **self.report(),

        "compression_ready": True,

        "context_cached": True,

        "enterprise_version": "3.2.0",

        }
###############################################################################
# Global Context Manager
###############################################################################

context_manager: (
    ContextManager | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "AIContext",
    "ContextManager",
    "context_manager",
]