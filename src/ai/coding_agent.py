"""
==============================================================================
GEETA AI IDE

File        : coding_agent.py
Package     : ai
Description : Enterprise Autonomous Coding Agent

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from config.logger import get_logger

from ai.context_manager import ContextManager
from ai.planner import AITask
from ai.task_manager import AITaskManager

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Agent Status
###############################################################################


class CodingAgentStatus(str, Enum):

    IDLE = "idle"

    PLANNING = "planning"

    GENERATING = "generating"

    APPLYING = "applying"

    FINISHED = "finished"

    FAILED = "failed"

###############################################################################
# Code Patch
###############################################################################


@dataclass(slots=True)
class CodePatch:
    """
    Represents a generated code patch.
    """

    file_path: str

    original_code: str = ""

    generated_code: str = ""

    diff: str = ""

###############################################################################
# Coding Result
###############################################################################


@dataclass(slots=True)
class CodingResult:
    """
    Result produced by Coding Agent.
    """

    success: bool = False

    message: str = ""

    patches: list[
        CodePatch
    ] = field(
        default_factory=list,
    )

###############################################################################
# Autonomous Coding Agent
###############################################################################


class CodingAgent:
    """
    Enterprise Autonomous Coding Agent.

    Responsibilities

    - Project-aware code generation
    - Multi-file editing
    - Prompt generation
    - Patch generation
    - Diff generation
    - AI provider execution
    """

    ###########################################################################

    def __init__(
        self,
        context: ContextManager,
        task_manager: AITaskManager,
    ) -> None:

        self._context = context

        self._task_manager = task_manager

        self._status = (
            CodingAgentStatus.IDLE
        )

        logger.info(
            "Coding Agent initialized."
        )

###############################################################################
# Status
###############################################################################

    @property
    def status(
        self,
    ) -> CodingAgentStatus:

        return self._status

###############################################################################
# Start Task
###############################################################################

    def start(
        self,
        task: AITask,
    ) -> None:
        """
        Start autonomous coding task.
        """

        logger.info(
            "Starting task: %s",
            task.title,
        )

        self._status = (
            CodingAgentStatus.PLANNING
        )

        self._task_manager.mark_running(
            task,
        )

###############################################################################
# Prompt
###############################################################################

    def build_prompt(
        self,
        task: AITask,
    ) -> str:
        """
        Build AI prompt.
        """

        context = self._context.context

        return f"""
Project:
{context.project_name}

Language:
{context.language}

Current File:
{context.current_file}

Task:
{task.title}

Description:
{task.description}
""".strip()
###############################################################################
# Generate Code
###############################################################################

    def generate(
        self,
        task: AITask,
    ) -> CodingResult:
        """
        Generate code for the supplied task.

        NOTE:
        Actual AI provider integration is implemented by the
        Provider Layer (OpenAI / Claude / Gemini / Ollama).
        """

        self._status = (
            CodingAgentStatus.GENERATING
        )

        prompt = self.build_prompt(
            task,
        )

        logger.info(
            "Generating code..."
        )

        # Provider Layer Hook
        generated_code = ""

        patch = CodePatch(
            file_path=(
                self._context.context.current_file
            ),
            generated_code=generated_code,
        )

        return CodingResult(
            success=True,
            message="Generation completed.",
            patches=[patch],
        )

###############################################################################
# Generate Diff
###############################################################################

    def generate_diff(
        self,
        patch: CodePatch,
    ) -> str:
        """
        Generate unified diff.
        """

        self._status = (
            CodingAgentStatus.APPLYING
        )

        diff = (
            "--- original\n"
            "+++ modified\n"
            "@@\n"
            f"{patch.generated_code}"
        )

        patch.diff = diff

        return diff

###############################################################################
# Validate
###############################################################################

    def validate(
        self,
        result: CodingResult,
    ) -> bool:
        """
        Validate generated patches.
        """

        if not result.success:

            return False

        if not result.patches:

            return False

        return True

###############################################################################
# Apply
###############################################################################

    def apply(
        self,
        task: AITask,
        result: CodingResult,
    ) -> bool:
        """
        Apply generated patches.
        """

        if not self.validate(
            result,
        ):

            self._status = (
                CodingAgentStatus.FAILED
            )

            self._task_manager.mark_failed(
                task,
            )

            return False

        for patch in result.patches:

            logger.info(
                "Applying patch: %s",
                patch.file_path,
            )

        self._task_manager.mark_completed(
            task,
        )

        self._status = (
            CodingAgentStatus.FINISHED
        )

        return True

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, object]:
        """
        Return Coding Agent statistics.
        """

        return {
            "status": self._status.value,
            "project": (
                self._context.context.project_name
            ),
            "current_file": (
                self._context.context.current_file
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return Coding Agent report.
        """

        return {
            "agent": "CodingAgent",
            "statistics": self.statistics(),
        }

###############################################################################
# Global Agent
###############################################################################

coding_agent: (
    CodingAgent | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "CodingAgentStatus",
    "CodePatch",
    "CodingResult",
    "CodingAgent",
    "coding_agent",
]