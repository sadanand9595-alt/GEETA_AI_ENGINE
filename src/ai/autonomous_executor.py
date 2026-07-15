"""
==============================================================================
GEETA AI IDE

File        : autonomous_executor.py
Package     : ai
Description : Enterprise Autonomous Executor

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4

from config.logger import get_logger

from ai.workflow_engine import Workflow, WorkflowEngine
from ai.multi_agent_coordinator import (
    MultiAgentCoordinator,
)
from ai.session_manager import (
    SessionManager,
)
from ai.memory_engine import (
    MemoryEngine,
)
from ai.prompt_engine import (
    PromptEngine,
)

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Execution Status
###############################################################################


class ExecutionStatus(str, Enum):

    CREATED = "created"

    RUNNING = "running"

    PAUSED = "paused"

    COMPLETED = "completed"

    FAILED = "failed"

###############################################################################
# Execution Record
###############################################################################


@dataclass(slots=True)
class ExecutionRecord:
    """
    Autonomous execution record.
    """

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    workflow_id: str = ""

    project: str = ""

    status: ExecutionStatus = (
        ExecutionStatus.CREATED
    )

    started_at: datetime = field(
        default_factory=datetime.utcnow
    )

    completed_at: datetime | None = None

###############################################################################
# Autonomous Executor
###############################################################################


class AutonomousExecutor:
    """
    Enterprise Autonomous Executor.

    Responsibilities

    - Execute workflows
    - Coordinate agents
    - Resume sessions
    - Manage execution lifecycle
    - Continuous automation
    """

    ###########################################################################

    def __init__(
        self,
        workflow_engine: WorkflowEngine,
        coordinator: MultiAgentCoordinator,
        session_manager: SessionManager,
        memory_engine: MemoryEngine,
        prompt_engine: PromptEngine,
    ) -> None:

        self._workflow_engine = workflow_engine

        self._coordinator = coordinator

        self._session_manager = session_manager

        self._memory_engine = memory_engine

        self._prompt_engine = prompt_engine

        self._executions: dict[
            str,
            ExecutionRecord
        ] = {}

        logger.info(
            "Autonomous Executor initialized."
        )

###############################################################################
# Start Execution
###############################################################################

    def start(
        self,
        workflow: Workflow,
        project: str,
    ) -> ExecutionRecord:
        """
        Start autonomous execution.
        """

        record = ExecutionRecord(
            workflow_id=workflow.id,
            project=project,
            status=ExecutionStatus.RUNNING,
        )

        self._executions[
            record.id
        ] = record

        logger.info(
            "Execution started: %s",
            workflow.name,
        )

        self._workflow_engine.start(
            workflow,
        )

        return record

###############################################################################
# Lookup
###############################################################################

    def execution(
        self,
        execution_id: str,
    ) -> ExecutionRecord | None:
        """
        Return execution record.
        """

        return self._executions.get(
            execution_id,
        )
###############################################################################
# Pause Execution
###############################################################################

    def pause(
        self,
        execution: ExecutionRecord,
    ) -> None:
        """
        Pause execution.
        """

        execution.status = (
            ExecutionStatus.PAUSED
        )

        logger.info(
            "Execution paused."
        )

###############################################################################
# Resume Execution
###############################################################################

    def resume(
        self,
        execution: ExecutionRecord,
    ) -> None:
        """
        Resume execution.
        """

        execution.status = (
            ExecutionStatus.RUNNING
        )

        logger.info(
            "Execution resumed."
        )

###############################################################################
# Finish Execution
###############################################################################

    def finish(
        self,
        execution: ExecutionRecord,
        success: bool = True,
    ) -> None:
        """
        Finish execution.
        """

        execution.completed_at = (
            datetime.utcnow()
        )

        execution.status = (
            ExecutionStatus.COMPLETED
            if success
            else ExecutionStatus.FAILED
        )

        logger.info(
            "Execution finished."
        )

###############################################################################
# Retry Execution
###############################################################################

    def retry(
        self,
        workflow: Workflow,
        execution: ExecutionRecord,
    ) -> None:
        """
        Retry failed execution.
        """

        logger.info(
            "Retry execution."
        )

        execution.status = (
            ExecutionStatus.RUNNING
        )

        self._workflow_engine.retry(
            workflow,
        )

###############################################################################
# Rollback
###############################################################################

    def rollback(
        self,
        workflow: Workflow,
        execution: ExecutionRecord,
    ) -> None:
        """
        Rollback workflow.
        """

        logger.warning(
            "Rollback execution."
        )

        self._workflow_engine.rollback(
            workflow,
        )

        execution.status = (
            ExecutionStatus.FAILED
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return execution statistics.
        """

        return {
            "executions": len(
                self._executions
            ),
            "running": sum(
                1
                for execution
                in self._executions.values()
                if execution.status
                == ExecutionStatus.RUNNING
            ),
            "completed": sum(
                1
                for execution
                in self._executions.values()
                if execution.status
                == ExecutionStatus.COMPLETED
            ),
            "failed": sum(
                1
                for execution
                in self._executions.values()
                if execution.status
                == ExecutionStatus.FAILED
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return execution report.
        """

        return {
            "statistics": self.statistics(),
            "executions": [
                {
                    "id": execution.id,
                    "workflow": execution.workflow_id,
                    "project": execution.project,
                    "status": execution.status.value,
                    "started": execution.started_at.isoformat(),
                    "completed": (
                        execution.completed_at.isoformat()
                        if execution.completed_at
                        else None
                    ),
                }
                for execution
                in self._executions.values()
            ],
        }

###############################################################################
# Global Executor
###############################################################################

autonomous_executor: (
    AutonomousExecutor | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "ExecutionStatus",
    "ExecutionRecord",
    "AutonomousExecutor",
    "autonomous_executor",
]