"""
==============================================================================
GEETA AI Engine

File        : workflow_engine.py
Package     : agents
Description : AI Workflow Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from time import time
from typing import Any

from agents.agent_orchestrator import (
    agent_orchestrator,
)
from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Workflow Types
###############################################################################


class WorkflowStatus(str, Enum):
    """
    Workflow execution state.
    """

    PENDING = "pending"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

###############################################################################
# Workflow Step
###############################################################################


@dataclass
class WorkflowStep:
    """
    Represents a workflow step.
    """

    name: str

    agent: str

    request: str

    parameters: dict[str, Any] = field(
        default_factory=dict,
    )

###############################################################################
# Workflow
###############################################################################


@dataclass
class Workflow:
    """
    AI workflow definition.
    """

    workflow_id: str

    name: str

    steps: list[
        WorkflowStep
    ]

    status: WorkflowStatus = (
        WorkflowStatus.PENDING
    )

    created_at: float = field(
        default_factory=time,
    )

###############################################################################
# Workflow Engine
###############################################################################


class WorkflowEngine:
    """
    Executes autonomous AI workflows.

    Responsibilities

    - Multi-step execution
    - Agent coordination
    - Workflow persistence
    - Recovery
    - Progress tracking
    """

    def __init__(self) -> None:

        self._workflows: dict[
            str,
            Workflow,
        ] = {}

        logger.info(
            "Workflow Engine initialized."
        )

    ###########################################################################

    def register(
        self,
        workflow: Workflow,
    ) -> None:
        """
        Register workflow.
        """

        self._workflows[
            workflow.workflow_id
        ] = workflow

    ###########################################################################

    def execute(
        self,
        workflow_id: str,
    ) -> list[Any]:
        """
        Execute workflow.
        """

        workflow = self._workflows[
            workflow_id
        ]

        workflow.status = (
            WorkflowStatus.RUNNING
        )

        results: list[Any] = []

        for step in workflow.steps:

            logger.info(
                "Executing workflow step: %s",
                step.name,
            )

            result = (
                agent_orchestrator.execute(
                    agent_name=step.agent,
                    request=step.request,
                    **step.parameters,
                )
            )

            results.append(
                result,
            )

        workflow.status = (
            WorkflowStatus.COMPLETED
        )

        return results
###############################################################################
# Workflow Management
###############################################################################

    def cancel(
        self,
        workflow_id: str,
    ) -> bool:
        """
        Cancel a workflow.
        """

        workflow = self._workflows.get(
            workflow_id,
        )

        if workflow is None:

            return False

        if workflow.status == WorkflowStatus.RUNNING:

            workflow.status = (
                WorkflowStatus.FAILED
            )

            logger.info(
                "Workflow cancelled: %s",
                workflow_id,
            )

            return True

        return False

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return workflow statistics.
        """

        stats = {
            "total": len(
                self._workflows
            ),
            "pending": 0,
            "running": 0,
            "completed": 0,
            "failed": 0,
        }

        for workflow in self._workflows.values():

            if workflow.status == WorkflowStatus.PENDING:

                stats["pending"] += 1

            elif workflow.status == WorkflowStatus.RUNNING:

                stats["running"] += 1

            elif workflow.status == WorkflowStatus.COMPLETED:

                stats["completed"] += 1

            elif workflow.status == WorkflowStatus.FAILED:

                stats["failed"] += 1

        return stats

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return workflow engine report.
        """

        return {
            "statistics": self.statistics(),
            "workflows": [
                {
                    "id": workflow.workflow_id,
                    "name": workflow.name,
                    "status": workflow.status.value,
                    "steps": len(
                        workflow.steps
                    ),
                }
                for workflow in self._workflows.values()
            ],
        }

###############################################################################
# Global Workflow Engine
###############################################################################

workflow_engine = WorkflowEngine()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "WorkflowStatus",
    "WorkflowStep",
    "Workflow",
    "WorkflowEngine",
    "workflow_engine",
]