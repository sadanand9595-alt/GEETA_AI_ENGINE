"""
==============================================================================
GEETA AI IDE

File        : refactor_agent.py
Package     : ai
Description : Enterprise Autonomous Refactor Agent

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
# Refactor Status
###############################################################################


class RefactorStatus(str, Enum):

    IDLE = "idle"

    ANALYZING = "analyzing"

    REFACTORING = "refactoring"

    VALIDATING = "validating"

    FINISHED = "finished"

    FAILED = "failed"


###############################################################################
# Refactor Action
###############################################################################


class RefactorAction(str, Enum):

    RENAME_SYMBOL = "rename_symbol"

    EXTRACT_METHOD = "extract_method"

    EXTRACT_CLASS = "extract_class"

    INLINE_VARIABLE = "inline_variable"

    REMOVE_DEAD_CODE = "remove_dead_code"

    FORMAT_CODE = "format_code"

###############################################################################
# Refactor Change
###############################################################################


@dataclass(slots=True)
class RefactorChange:
    """
    Represents one refactoring change.
    """

    file_path: str

    action: RefactorAction

    description: str

    original_code: str = ""

    updated_code: str = ""

###############################################################################
# Refactor Result
###############################################################################


@dataclass(slots=True)
class RefactorResult:
    """
    Refactoring result.
    """

    success: bool = False

    message: str = ""

    changes: list[
        RefactorChange
    ] = field(
        default_factory=list,
    )

###############################################################################
# Refactor Agent
###############################################################################


class RefactorAgent:
    """
    Enterprise Autonomous Refactor Agent.

    Responsibilities

    - Code smell detection
    - Safe refactoring
    - Multi-file updates
    - Rename propagation
    - Preview generation
    - Rollback support
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
            RefactorStatus.IDLE
        )

        logger.info(
            "Refactor Agent initialized."
        )

###############################################################################
# Status
###############################################################################

    @property
    def status(
        self,
    ) -> RefactorStatus:

        return self._status

###############################################################################
# Analyze
###############################################################################

    def analyze(
        self,
        task: AITask,
    ) -> None:
        """
        Analyze project before refactoring.
        """

        self._status = (
            RefactorStatus.ANALYZING
        )

        logger.info(
            "Analyzing project..."
        )

        self._task_manager.mark_running(
            task,
        )

###############################################################################
# Detect Smells
###############################################################################

    def detect_code_smells(
        self,
        file_path: str,
    ) -> list[str]:
        """
        Detect code smells.
        """

        logger.info(
            "Scanning %s",
            file_path,
        )

        return []

###############################################################################
# Preview
###############################################################################

    def preview(
        self,
        result: RefactorResult,
    ) -> list[RefactorChange]:
        """
        Preview refactoring changes.
        """

        return list(
            result.changes
        )
###############################################################################
# Refactor
###############################################################################

    def refactor(
        self,
        task: AITask,
        result: RefactorResult,
    ) -> bool:
        """
        Execute AI refactoring.
        """

        self._status = (
            RefactorStatus.REFACTORING
        )

        logger.info(
            "Executing refactoring..."
        )

        if not self.validate(
            result,
        ):

            self._status = (
                RefactorStatus.FAILED
            )

            self._task_manager.mark_failed(
                task,
            )

            return False

        self.apply_changes(
            result,
        )

        self._task_manager.mark_completed(
            task,
        )

        self._status = (
            RefactorStatus.FINISHED
        )

        return True

###############################################################################
# Validation
###############################################################################

    def validate(
        self,
        result: RefactorResult,
    ) -> bool:
        """
        Validate refactoring result.
        """

        self._status = (
            RefactorStatus.VALIDATING
        )

        return (
            result.success
            and bool(result.changes)
        )

###############################################################################
# Apply Changes
###############################################################################

    def apply_changes(
        self,
        result: RefactorResult,
    ) -> None:
        """
        Apply refactoring changes.
        """

        for change in result.changes:

            logger.info(
                "Applying %s -> %s",
                change.action.value,
                change.file_path,
            )

###############################################################################
# Rollback
###############################################################################

    def rollback(
        self,
        result: RefactorResult,
    ) -> None:
        """
        Rollback refactoring.
        """

        logger.warning(
            "Rollback started."
        )

        for change in reversed(
            result.changes
        ):

            logger.info(
                "Rollback %s",
                change.file_path,
            )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, object]:
        """
        Return Refactor Agent statistics.
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
        Return Refactor Agent report.
        """

        return {
            "agent": "RefactorAgent",
            "statistics": self.statistics(),
        }

###############################################################################
# Global Agent
###############################################################################

refactor_agent: (
    RefactorAgent | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "RefactorStatus",
    "RefactorAction",
    "RefactorChange",
    "RefactorResult",
    "RefactorAgent",
    "refactor_agent",
]