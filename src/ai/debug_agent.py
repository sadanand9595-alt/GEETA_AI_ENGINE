"""
==============================================================================
GEETA AI IDE

File        : debug_agent.py
Package     : ai
Description : Enterprise Autonomous Debug Agent

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from config.logger import get_logger

from ai.context_manager import ContextManager
from ai.task_manager import AITaskManager
from ai.planner import AITask

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Debug Status
###############################################################################


class DebugStatus(str, Enum):

    IDLE = "idle"

    ANALYZING = "analyzing"

    FIXING = "fixing"

    VALIDATING = "validating"

    FINISHED = "finished"

    FAILED = "failed"

###############################################################################
# Debug Issue
###############################################################################


@dataclass(slots=True)
class DebugIssue:
    """
    Represents detected issue.
    """

    file_path: str

    line: int

    message: str

    severity: str

    traceback: str = ""

###############################################################################
# Debug Result
###############################################################################


@dataclass(slots=True)
class DebugResult:
    """
    Debug execution result.
    """

    success: bool = False

    root_cause: str = ""

    suggested_fix: str = ""

    applied_files: list[str] = field(
        default_factory=list,
    )

###############################################################################
# Autonomous Debug Agent
###############################################################################


class DebugAgent:
    """
    Enterprise Debug Agent.

    Responsibilities

    - Stack trace analysis
    - Runtime error diagnosis
    - LSP diagnostics
    - Root cause analysis
    - Automatic fixing
    """

    ###########################################################################

    def __init__(
        self,
        context: ContextManager,
        task_manager: AITaskManager,
    ) -> None:

        self._context = context

        self._task_manager = task_manager

        self._status = DebugStatus.IDLE

        logger.info(
            "Debug Agent initialized."
        )

###############################################################################
# Status
###############################################################################

    @property
    def status(
        self,
    ) -> DebugStatus:

        return self._status

###############################################################################
# Analyze
###############################################################################

    def analyze(
        self,
        task: AITask,
        issue: DebugIssue,
    ) -> DebugResult:
        """
        Analyze an issue.
        """

        self._status = (
            DebugStatus.ANALYZING
        )

        logger.info(
            "Analyzing issue..."
        )

        self._task_manager.mark_running(
            task,
        )

        return DebugResult(
            success=True,
            root_cause=issue.message,
            suggested_fix="Analysis completed.",
        )

###############################################################################
# Traceback Parser
###############################################################################

    def parse_traceback(
        self,
        traceback: str,
    ) -> list[str]:
        """
        Parse Python traceback.
        """

        return [
            line.strip()
            for line
            in traceback.splitlines()
            if line.strip()
        ]
###############################################################################
# Root Cause Analysis
###############################################################################

    def root_cause(
        self,
        issue: DebugIssue,
    ) -> str:
        """
        Determine the root cause.
        """

        logger.info(
            "Determining root cause..."
        )

        return issue.message

###############################################################################
# Generate Fix
###############################################################################

    def generate_fix(
        self,
        issue: DebugIssue,
    ) -> str:
        """
        Generate an AI fix suggestion.

        Provider Layer integration will replace this
        placeholder implementation.
        """

        self._status = (
            DebugStatus.FIXING
        )

        return (
            "AI generated fix for: "
            f"{issue.message}"
        )

###############################################################################
# Validate Fix
###############################################################################

    def validate_fix(
        self,
        result: DebugResult,
    ) -> bool:
        """
        Validate generated fix.
        """

        self._status = (
            DebugStatus.VALIDATING
        )

        return (
            result.success
            and bool(result.suggested_fix)
        )

###############################################################################
# Apply Fix
###############################################################################

    def apply_fix(
        self,
        task: AITask,
        result: DebugResult,
    ) -> bool:
        """
        Apply validated fix.
        """

        if not self.validate_fix(
            result,
        ):

            self._status = (
                DebugStatus.FAILED
            )

            self._task_manager.mark_failed(
                task,
            )

            return False

        self._task_manager.mark_completed(
            task,
        )

        self._status = (
            DebugStatus.FINISHED
        )

        return True

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, object]:
        """
        Return Debug Agent statistics.
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
        Return Debug Agent report.
        """

        return {
            "agent": "DebugAgent",
            "statistics": self.statistics(),
        }

###############################################################################
# Global Debug Agent
###############################################################################

debug_agent: (
    DebugAgent | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "DebugStatus",
    "DebugIssue",
    "DebugResult",
    "DebugAgent",
    "debug_agent",
]
