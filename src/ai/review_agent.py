"""
==============================================================================
GEETA AI IDE

File        : review_agent.py
Package     : ai
Description : Enterprise AI Review Agent

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
# Review Status
###############################################################################


class ReviewStatus(str, Enum):

    IDLE = "idle"

    ANALYZING = "analyzing"

    REVIEWING = "reviewing"

    FINISHED = "finished"

    FAILED = "failed"

###############################################################################
# Review Severity
###############################################################################


class ReviewSeverity(str, Enum):

    INFO = "info"

    WARNING = "warning"

    ERROR = "error"

    CRITICAL = "critical"

###############################################################################
# Review Finding
###############################################################################


@dataclass(slots=True)
class ReviewFinding:
    """
    Represents one review finding.
    """

    file_path: str

    line: int

    severity: ReviewSeverity

    title: str

    description: str

    recommendation: str = ""

###############################################################################
# Review Result
###############################################################################


@dataclass(slots=True)
class ReviewResult:
    """
    AI Review Result.
    """

    success: bool = False

    score: float = 0.0

    summary: str = ""

    findings: list[
        ReviewFinding
    ] = field(
        default_factory=list,
    )

###############################################################################
# Review Agent
###############################################################################


class ReviewAgent:
    """
    Enterprise AI Review Agent.

    Responsibilities

    - Static analysis
    - Security review
    - Performance review
    - Clean Code validation
    - SOLID validation
    - AI recommendations
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
            ReviewStatus.IDLE
        )

        logger.info(
            "Review Agent initialized."
        )

###############################################################################
# Status
###############################################################################

    @property
    def status(
        self,
    ) -> ReviewStatus:

        return self._status

###############################################################################
# Review
###############################################################################

    def review(
        self,
        task: AITask,
    ) -> None:
        """
        Start AI review.
        """

        self._status = (
            ReviewStatus.ANALYZING
        )

        logger.info(
            "Review started."
        )

        self._task_manager.mark_running(
            task,
        )

###############################################################################
# Security Review
###############################################################################

    def security_review(
        self,
        file_path: str,
    ) -> list[ReviewFinding]:
        """
        Review security issues.
        """

        logger.info(
            "Security review: %s",
            file_path,
        )

        return []

###############################################################################
# Performance Review
###############################################################################

    def performance_review(
        self,
        file_path: str,
    ) -> list[ReviewFinding]:
        """
        Review performance.
        """

        logger.info(
            "Performance review: %s",
            file_path,
        )

        return []
###############################################################################
# Maintainability Review
###############################################################################

    def maintainability_review(
        self,
        file_path: str,
    ) -> list[ReviewFinding]:
        """
        Review maintainability.
        """

        logger.info(
            "Maintainability review: %s",
            file_path,
        )

        return []

###############################################################################
# SOLID Validation
###############################################################################

    def validate_solid(
        self,
        file_path: str,
    ) -> list[ReviewFinding]:
        """
        Validate SOLID principles.
        """

        logger.info(
            "SOLID validation: %s",
            file_path,
        )

        return []

###############################################################################
# Code Quality Score
###############################################################################

    def quality_score(
        self,
        result: ReviewResult,
    ) -> float:
        """
        Calculate code quality score.
        """

        if not result.findings:

            return 100.0

        deduction = min(
            len(result.findings) * 5,
            100,
        )

        return max(
            0.0,
            100.0 - deduction,
        )

###############################################################################
# Finish Review
###############################################################################

    def finish(
        self,
        task: AITask,
        result: ReviewResult,
    ) -> bool:
        """
        Finish review task.
        """

        result.score = self.quality_score(
            result,
        )

        result.success = True

        self._task_manager.mark_completed(
            task,
        )

        self._status = (
            ReviewStatus.FINISHED
        )

        return True

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, object]:
        """
        Return Review Agent statistics.
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
        Return review report.
        """

        return {
            "agent": "ReviewAgent",
            "statistics": self.statistics(),
        }

###############################################################################
# Global Review Agent
###############################################################################

review_agent: (
    ReviewAgent | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "ReviewStatus",
    "ReviewSeverity",
    "ReviewFinding",
    "ReviewResult",
    "ReviewAgent",
    "review_agent",
]