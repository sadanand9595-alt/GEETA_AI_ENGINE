"""
==============================================================================
GEETA AI Engine

File        : prompt_engine.py
Package     : ai
Description : Intelligent Prompt Builder

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from config.logger import get_logger
from dataclasses import dataclass, field
from enum import Enum

from src.ai.ai_session_manager import AISessionManager
###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)
###############################################################################
# Prompt Intent
###############################################################################


class PromptIntent(str, Enum):
    """
    Supported prompt intents.
    """

    CREATE = "create"

    MODIFY = "modify"

    DEBUG = "debug"

    REFACTOR = "refactor"

    REVIEW = "review"

    EXPLAIN = "explain"

    TEST = "test"

    DOCUMENT = "document"

    UNKNOWN = "unknown"
###############################################################################
# Prompt Context
###############################################################################


@dataclass(slots=True)
class PromptContext:
    """
    Complete prompt context.
    """

    instruction: str = ""

    project_context: str = ""

    workspace_context: str = ""

    selected_code: str = ""

    active_file: str = ""

    diagnostics: str = ""

    conversation: list[str] = field(
        default_factory=list,
    )

    memory: str = ""

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )
###############################################################################
# Execution Plan
###############################################################################


@dataclass(slots=True)
class ExecutionPlan:
    """
    AI execution plan.
    """

    intent: PromptIntent = PromptIntent.UNKNOWN

    priority: str = "normal"

    affected_files: list[str] = field(
        default_factory=list,
    )

    expected_output: str = ""

    constraints: list[str] = field(
        default_factory=list,
    )
###############################################################################
# Prompt Engine
###############################################################################


class PromptEngine:
    """
    Enterprise Prompt Builder.
    """
    ###############################################################################
# Prompt Summary
###############################################################################

    def summary(
        self,
        context: PromptContext,
    ) -> dict[str, Any]:
        """
        Return prompt summary.
        """

        return {

            "instruction": context.instruction,

            "active_file": context.active_file,

            "conversation_messages": len(
                context.conversation,
            ),

            "metadata_entries": len(
                context.metadata,
            ),

        }
###############################################################################
# Validation
###############################################################################

    def validate(
        self,
        context: PromptContext,
    ) -> bool:
        """
        Validate prompt context.
        """

        if not context.instruction.strip():

            logger.warning(
                "Prompt instruction is empty."
            )

            return False

        return True
    ###############################################################################
# Provider Prompt
###############################################################################

    def build_provider_prompt(
        self,
        provider: str,
        prompt: str,
    ) -> str:
        """
        Build provider-specific prompt.
        """

        provider = provider.lower()

        if provider == "openai":

            return (
                "You are an enterprise software engineer.\n\n"
                + prompt
            )

        if provider == "claude":

            return (
                "You are a senior software architect.\n\n"
                + prompt
            )

        if provider == "gemini":

            return (
                "You are an expert AI developer.\n\n"
                + prompt
            )

        if provider == "ollama":

            return (
                "You are a local coding assistant.\n\n"
                + prompt
            )

        return prompt
        ###############################################################################
# Token Estimation
###############################################################################

    def estimate_tokens(
        self,
        prompt: str,
    ) -> int:
        """
        Estimate prompt tokens.
        """

        return max(
            1,
            len(prompt) // 4,
        )
        ###############################################################################
# Smart Compression
###############################################################################

    def compress(
        self,
        prompt: str,
        max_tokens: int = 30000,
    ) -> str:
        """
        Compress prompt if necessary.
        """

        estimated = self.estimate_tokens(
            prompt,
        )

        if estimated <= max_tokens:

            return prompt

        logger.warning(
            "Prompt compressed "
            "(estimated tokens=%d).",
            estimated,
        )

        target_length = max_tokens * 4

        return prompt[:target_length]
        ###############################################################################
# Provider Metadata
###############################################################################

    def provider_metadata(
        self,
        provider: str,
    ) -> dict[str, str]:
        """
        Return provider information.
        """

        return {

            "provider": provider,

            "prompt_version": "3.2",

            "engine": "GEETA Prompt Engine",

        }
    ###############################################################################
# Intent Detection
###############################################################################

    def detect_intent(
        self,
        instruction: str,
    ) -> PromptIntent:
        """
        Detect the user's coding intent.
        """

        text = instruction.lower()

        if any(
            word in text
            for word in (
                "create",
                "build",
                "generate",
                "make",
            )
        ):
            return PromptIntent.CREATE

        if any(
            word in text
            for word in (
                "modify",
                "change",
                "update",
                "edit",
            )
        ):
            return PromptIntent.MODIFY

        if any(
            word in text
            for word in (
                "fix",
                "bug",
                "error",
                "debug",
            )
        ):
            return PromptIntent.DEBUG

        if any(
            word in text
            for word in (
                "refactor",
                "optimize",
                "cleanup",
            )
        ):
            return PromptIntent.REFACTOR

        if any(
            word in text
            for word in (
                "review",
                "inspect",
                "audit",
            )
        ):
            return PromptIntent.REVIEW

        if any(
            word in text
            for word in (
                "explain",
                "describe",
            )
        ):
            return PromptIntent.EXPLAIN

        if any(
            word in text
            for word in (
                "test",
                "pytest",
                "unit test",
            )
        ):
            return PromptIntent.TEST

        if any(
            word in text
            for word in (
                "document",
                "documentation",
                "comment",
            )
        ):
            return PromptIntent.DOCUMENT

        return PromptIntent.UNKNOWN
        ###############################################################################
# Priority Detection
###############################################################################

    def detect_priority(
        self,
        instruction: str,
    ) -> str:
        """
        Detect execution priority.
        """

        text = instruction.lower()

        if any(
            word in text
            for word in (
                "urgent",
                "critical",
                "immediately",
            )
        ):
            return "high"

        if any(
            word in text
            for word in (
                "later",
                "eventually",
            )
        ):
            return "low"

        return "normal"
        logger.info(
            "Execution plan created "
            "(intent=%s, priority=%s)",
            plan.intent.value,
            plan.priority,
        )
        ###############################################################################
# Execution Plan
###############################################################################

    def build_execution_plan(
        self,
        context: PromptContext,
    ) -> ExecutionPlan:
        """
        Build an execution plan from the prompt context.
        """

        plan = ExecutionPlan()

        plan.intent = self.detect_intent(
            context.instruction,
        )

        plan.priority = self.detect_priority(
            context.instruction,
        )

        if context.active_file:

            plan.affected_files.append(
                context.active_file,
            )

        plan.expected_output = (
            "Production-ready implementation"
        )

        return plan
###############################################################################
# Build From Session
###############################################################################

    def build_from_session(
        self,
        session: AISessionManager,
    ) -> PromptContext:
        """
        Build prompt context from an AI session.
        """

        snapshot = session.build_context()

        return PromptContext(

            project_context=str(
                snapshot.get(
                    "project",
                    "",
                )
            ),

            active_file=snapshot.get(
                "current_file",
                "",
            ),

            metadata=snapshot,
        )
    def __init__(self) -> None:

        logger.info(
            "Prompt Engine initialized."
        )

    ###########################################################################

    def build(
        self,
        context: PromptContext,
    ) -> str:
        """
        Build optimized AI prompt.
        """

        sections: list[str] = []

        if context.project_context:

            sections.append(
                "# Project Context\n"
                + context.project_context
            )

        if context.workspace_context:

            sections.append(
                "# Workspace Context\n"
                + context.workspace_context
            )

        if context.active_file:

            sections.append(
                "# Active File\n"
                + context.active_file
            )

        if context.selected_code:

            sections.append(
                "# Selected Code\n"
                + context.selected_code
            )
            #######################################################################
        # Conversation
        #######################################################################

        if context.conversation:

            sections.append(
                "# Conversation History\n"
                + "\n".join(
                    context.conversation
                )
            )

        #######################################################################
        # Memory
        #######################################################################

        if context.memory:

            sections.append(
                "# AI Memory\n"
                + context.memory
            )

        #######################################################################
        # Diagnostics
        #######################################################################

        if context.diagnostics:

            sections.append(
                "# Diagnostics\n"
                + context.diagnostics
            )

        #######################################################################
        # User Instruction
        #######################################################################

        if context.instruction:

            sections.append(
                "# User Request\n"
                + context.instruction
            )

        prompt = "\n\n".join(
            sections
        )

        logger.debug(
            "Prompt built (%d characters).",
            len(prompt),
        )

        return prompt

###############################################################################
# Prompt Optimization
###############################################################################

    def optimize(
        self,
        prompt: str,
        max_length: int = 120000,
    ) -> str:
        """
        Optimize prompt length.

        Future versions can add:
        - Token estimation
        - Smart compression
        - Semantic summarization
        """

        if len(prompt) <= max_length:

            return prompt

        logger.warning(
            "Prompt exceeds limit (%d). Truncating.",
            max_length,
        )

        return prompt[:max_length]

###############################################################################
# Prompt Statistics
###############################################################################

    def statistics(
        self,
        prompt: str,
    ) -> dict[str, int]:
        """
        Return prompt statistics.
        """

        return {
            "characters": len(prompt),
            "lines": len(
                prompt.splitlines()
            ),
            "words": len(
                prompt.split()
            ),
        }
        ###############################################################################
# System Prompt
###############################################################################

    def build_system_prompt(
        self,
        role: str,
        context: str = "",
    ) -> str:
        """
        Build a system prompt.
        """

        sections = [
            f"Role: {role}",
        ]

        if context:

            sections.append(
                context,
            )

        return "\n\n".join(
            sections,
        )

###############################################################################
# Metadata
###############################################################################

    def inject_metadata(
        self,
        prompt: str,
        metadata: dict[str, Any],
    ) -> str:
        """
        Inject metadata into prompt.
        """

        if not metadata:

            return prompt

        metadata_lines = [
            "# Metadata",
        ]

        for key, value in metadata.items():

            metadata_lines.append(
                f"{key}: {value}",
            )

        return (
            "\n".join(metadata_lines)
            + "\n\n"
            + prompt
        )

###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
        prompt: str,
    ) -> dict[str, Any]:
        """
        Return prompt diagnostics.
        """

        return {

            **self.statistics(
                prompt,
            ),

            "estimated_tokens": self.estimate_tokens(
                prompt,
            ),

            "providers": [
                "openai",
                "claude",
                "gemini",
                "ollama",
            ],

            "optimized": True,

            "engine_version": "3.2.0",

        }
###############################################################################
# Global Instance
###############################################################################

prompt_engine = PromptEngine()

###############################################################################
# Helper Functions
###############################################################################


def build_prompt(
    context: PromptContext,
) -> str:
    """
    Build AI prompt.
    """

    return prompt_engine.build(
        context,
    )


def optimize_prompt(
    prompt: str,
    max_length: int = 120000,
) -> str:
    """
    Optimize prompt.
    """

    return prompt_engine.optimize(
        prompt,
        max_length=max_length,
    )


def prompt_statistics(
    prompt: str,
) -> dict[str, int]:
    """
    Return prompt statistics.
    """

    return prompt_engine.statistics(
        prompt,
    )

###############################################################################
# Exports
###############################################################################

__all__ = [

    "PromptIntent",

    "ExecutionPlan",

    "PromptContext",

    "PromptEngine",

    "prompt_engine",

    "build_prompt",

    "optimize_prompt",

    "prompt_statistics",

]