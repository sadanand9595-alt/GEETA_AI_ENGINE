"""
==============================================================================
GEETA AI IDE

File        : test_agent.py
Package     : ai
Description : Enterprise Autonomous Test Agent

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
# Test Status
###############################################################################


class TestStatus(str, Enum):

    IDLE = "idle"

    GENERATING = "generating"

    RUNNING = "running"

    ANALYZING = "analyzing"

    FINISHED = "finished"

    FAILED = "failed"

###############################################################################
# Test Type
###############################################################################


class TestType(str, Enum):

    UNIT = "unit"

    INTEGRATION = "integration"

    REGRESSION = "regression"

    PERFORMANCE = "performance"

###############################################################################
# Test Case
###############################################################################


@dataclass(slots=True)
class TestCase:

    name: str

    file_path: str

    test_type: TestType

    code: str = ""

###############################################################################
# Test Result
###############################################################################


@dataclass(slots=True)
class TestResult:

    success: bool = False

    passed: int = 0

    failed: int = 0

    skipped: int = 0

    coverage: float = 0.0

    test_cases: list[
        TestCase
    ] = field(
        default_factory=list,
    )

###############################################################################
# Test Agent
###############################################################################


class TestAgent:
    """
    Enterprise Autonomous Test Agent.

    Responsibilities

    - Unit tests
    - Integration tests
    - Regression tests
    - Coverage analysis
    - Test execution
    - AI-generated tests
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
            TestStatus.IDLE
        )

        logger.info(
            "Test Agent initialized."
        )

###############################################################################
# Status
###############################################################################

    @property
    def status(
        self,
    ) -> TestStatus:

        return self._status

###############################################################################
# Generate Tests
###############################################################################

    def generate_tests(
        self,
        task: AITask,
    ) -> None:
        """
        Generate AI tests.
        """

        self._status = (
            TestStatus.GENERATING
        )

        logger.info(
            "Generating tests..."
        )

        self._task_manager.mark_running(
            task,
        )

###############################################################################
# Run Tests
###############################################################################

    def run_tests(
        self,
        result: TestResult,
    ) -> None:
        """
        Execute tests.
        """

        self._status = (
            TestStatus.RUNNING
        )

        logger.info(
            "Executing tests..."
        )

###############################################################################
# Analyze Coverage
###############################################################################

    def analyze_coverage(
        self,
        result: TestResult,
    ) -> float:
        """
        Calculate coverage.
        """

        return result.coverage
###############################################################################
# Detect Flaky Tests
###############################################################################

    def detect_flaky_tests(
        self,
        result: TestResult,
    ) -> list[TestCase]:
        """
        Detect flaky tests.
        """

        logger.info(
            "Detecting flaky tests..."
        )

        return []

###############################################################################
# Generate Mocks
###############################################################################

    def generate_mocks(
        self,
        file_path: str,
    ) -> list[str]:
        """
        Generate mock objects.
        """

        logger.info(
            "Generating mocks for %s",
            file_path,
        )

        return []

###############################################################################
# Finish Testing
###############################################################################

    def finish(
        self,
        task: AITask,
        result: TestResult,
    ) -> bool:
        """
        Finish testing.
        """

        self._status = (
            TestStatus.ANALYZING
        )

        result.success = (
            result.failed == 0
        )

        if result.success:

            self._task_manager.mark_completed(
                task,
            )

            self._status = (
                TestStatus.FINISHED
            )

            return True

        self._task_manager.mark_failed(
            task,
        )

        self._status = (
            TestStatus.FAILED
        )

        return False

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, object]:
        """
        Return Test Agent statistics.
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
        Return Test Agent report.
        """

        return {
            "agent": "TestAgent",
            "statistics": self.statistics(),
        }

###############################################################################
# Global Agent
###############################################################################

test_agent: (
    TestAgent | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "TestStatus",
    "TestType",
    "TestCase",
    "TestResult",
    "TestAgent",
    "test_agent",
]