"""
==============================================================================
GEETA AI IDE

File        : workflow_engine.py
Package     : ai
Description : Enterprise Autonomous Workflow Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4

from config.logger import get_logger

from ai.planner import AITask
from ai.task_manager import AITaskManager
from ai.coding_agent import CodingAgent
from ai.debug_agent import DebugAgent
from ai.review_agent import ReviewAgent
from ai.test_agent import TestAgent
from ai.terminal_agent import TerminalAgent

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Workflow Status
###############################################################################


class WorkflowStatus(str, Enum):

    IDLE = "idle"

    RUNNING = "running"

    PAUSED = "paused"

    COMPLETED = "completed"

    FAILED = "failed"

###############################################################################
# Workflow Stage
###############################################################################


class WorkflowStage(str, Enum):

    PLANNING = "planning"

    CODING = "coding"

    DEBUGGING = "debugging"

    REVIEWING = "reviewing"

    TESTING = "testing"

    TERMINAL = "terminal"

###############################################################################
# Workflow
###############################################################################


@dataclass(slots=True)
class Workflow:

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    name: str = ""

    task: AITask | None = None

    stage: WorkflowStage = (
        WorkflowStage.PLANNING
    )

    status: WorkflowStatus = (
        WorkflowStatus.IDLE
    )

###############################################################################
# Workflow Engine
###############################################################################


class WorkflowEngine:
    """
    Enterprise Autonomous Workflow Engine.

    Responsibilities

    - Multi-agent orchestration
    - Workflow scheduling
    - Retry
    - Rollback
    - Agent coordination
    """

    ###########################################################################

    def __init__(
        self,
        task_manager: AITaskManager,
        coding: CodingAgent,
        debugger: DebugAgent,
        reviewer: ReviewAgent,
        tester: TestAgent,
        terminal: TerminalAgent,
    ) -> None:

        self._task_manager = task_manager

        self._coding = coding

        self._debugger = debugger

        self._reviewer = reviewer

        self._tester = tester

        self._terminal = terminal

        self._workflows: dict[
            str,
            Workflow
        ] = {}

        logger.info(
            "Workflow Engine initialized."
        )

###############################################################################
# Register
###############################################################################

    def register(
        self,
        workflow: Workflow,
    ) -> None:
        """
        Register workflow.
        """

        self._workflows[
            workflow.id
        ] = workflow

###############################################################################
# Lookup
###############################################################################

    def workflow(
        self,
        workflow_id: str,
    ) -> Workflow | None:

        return self._workflows.get(
            workflow_id
        )

###############################################################################
# Start
###############################################################################

    def start(
        self,
        workflow: Workflow,
    ) -> None:
        """
        Start workflow.
        """

        workflow.status = (
            WorkflowStatus.RUNNING
        )

        logger.info(
            "Workflow started: %s",
            workflow.name,
        )
###############################################################################
# Execute Workflow
###############################################################################

    def execute(
        self,
        workflow: Workflow,
    ) -> bool:
        """
        Execute autonomous workflow.
        """

        if workflow.task is None:

            workflow.status = (
                WorkflowStatus.FAILED
            )

            return False

        logger.info(
            "Executing workflow: %s",
            workflow.name,
        )

        #######################################################################
        # Coding
        #######################################################################

        workflow.stage = (
            WorkflowStage.CODING
        )

        self._coding.start(
            workflow.task,
        )

        #######################################################################
        # Debugging
        #######################################################################

        workflow.stage = (
            WorkflowStage.DEBUGGING
        )

        #######################################################################
        # Review
        #######################################################################

        workflow.stage = (
            WorkflowStage.REVIEWING
        )

        #######################################################################
        # Testing
        #######################################################################

        workflow.stage = (
            WorkflowStage.TESTING
        )

        #######################################################################
        # Terminal
        #######################################################################

        workflow.stage = (
            WorkflowStage.TERMINAL
        )

        workflow.status = (
            WorkflowStatus.COMPLETED
        )

        return True

###############################################################################
# Retry
###############################################################################

    def retry(
        self,
        workflow: Workflow,
    ) -> None:
        """
        Retry failed workflow.
        """

        logger.info(
            "Retry workflow: %s",
            workflow.name,
        )

        workflow.status = (
            WorkflowStatus.RUNNING
        )

###############################################################################
# Rollback
###############################################################################

    def rollback(
        self,
        workflow: Workflow,
    ) -> None:
        """
        Rollback workflow.
        """

        logger.warning(
            "Rollback workflow: %s",
            workflow.name,
        )

        workflow.status = (
            WorkflowStatus.FAILED
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return workflow statistics.
        """

        completed = sum(
            1
            for workflow
            in self._workflows.values()
            if workflow.status
            == WorkflowStatus.COMPLETED
        )

        running = sum(
            1
            for workflow
            in self._workflows.values()
            if workflow.status
            == WorkflowStatus.RUNNING
        )

        failed = sum(
            1
            for workflow
            in self._workflows.values()
            if workflow.status
            == WorkflowStatus.FAILED
        )

        return {
            "workflows": len(
                self._workflows
            ),
            "running": running,
            "completed": completed,
            "failed": failed,
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return workflow report.
        """

        return {
            "statistics": self.statistics(),
            "workflows": [
                {
                    "id": workflow.id,
                    "name": workflow.name,
                    "status": workflow.status.value,
                    "stage": workflow.stage.value,
                }
                for workflow
                in self._workflows.values()
            ],
        }

###############################################################################
# Global Workflow Engine
###############################################################################

workflow_engine: (
    WorkflowEngine | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "WorkflowStatus",
    "WorkflowStage",
    "Workflow",
    "WorkflowEngine",
    "workflow_engine",
]