"""
==============================================================================
GEETA AI IDE

File        : planner.py
Package     : ai
Description : Autonomous AI Planner

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Task Priority
###############################################################################


class TaskPriority(str, Enum):

    LOW = "low"

    NORMAL = "normal"

    HIGH = "high"

    CRITICAL = "critical"


###############################################################################
# Task Status
###############################################################################


class TaskStatus(str, Enum):

    PENDING = "pending"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

###############################################################################
# AI Task
###############################################################################


@dataclass(slots=True)
class AITask:
    """
    AI execution task.
    """

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    title: str = ""

    description: str = ""

    priority: TaskPriority = (
        TaskPriority.NORMAL
    )

    status: TaskStatus = (
        TaskStatus.PENDING
    )

    estimated_files: int = 0

    dependencies: list[str] = field(
        default_factory=list,
    )

###############################################################################
# Planner
###############################################################################


class AIPlanner:
    """
    Enterprise AI Planner.

    Responsibilities

    - Project planning
    - Task breakdown
    - Dependency graph
    - Execution ordering
    - Autonomous planning
    """

    ###########################################################################

    def __init__(self) -> None:

        self._tasks: dict[
            str,
            AITask,
        ] = {}

        logger.info(
            "AI Planner initialized."
        )

###############################################################################
# Add Task
###############################################################################

    def add_task(
        self,
        task: AITask,
    ) -> None:

        self._tasks[
            task.id
        ] = task

###############################################################################
# Remove Task
###############################################################################

    def remove_task(
        self,
        task_id: str,
    ) -> None:

        self._tasks.pop(
            task_id,
            None,
        )

###############################################################################
# Lookup
###############################################################################

    def task(
        self,
        task_id: str,
    ) -> AITask | None:

        return self._tasks.get(
            task_id,
        )
###############################################################################
# Task List
###############################################################################

    def tasks(
        self,
    ) -> list[AITask]:
        """
        Return all tasks.
        """

        return list(
            self._tasks.values()
        )

###############################################################################
# Ready Tasks
###############################################################################

    def ready_tasks(
        self,
    ) -> list[AITask]:
        """
        Return executable tasks.
        """

        completed = {
            task.id
            for task
            in self._tasks.values()
            if task.status
            == TaskStatus.COMPLETED
        }

        ready: list[
            AITask
        ] = []

        for task in self._tasks.values():

            if task.status != TaskStatus.PENDING:

                continue

            if all(
                dependency in completed
                for dependency
                in task.dependencies
            ):

                ready.append(
                    task
                )

        return ready

###############################################################################
# Update Status
###############################################################################

    def update_status(
        self,
        task_id: str,
        status: TaskStatus,
    ) -> bool:
        """
        Update task status.
        """

        task = self.task(
            task_id
        )

        if task is None:

            return False

        task.status = status

        return True

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return planner statistics.
        """

        return {
            "tasks": len(
                self._tasks
            ),
            "pending": sum(
                1
                for task
                in self._tasks.values()
                if task.status
                == TaskStatus.PENDING
            ),
            "running": sum(
                1
                for task
                in self._tasks.values()
                if task.status
                == TaskStatus.RUNNING
            ),
            "completed": sum(
                1
                for task
                in self._tasks.values()
                if task.status
                == TaskStatus.COMPLETED
            ),
            "failed": sum(
                1
                for task
                in self._tasks.values()
                if task.status
                == TaskStatus.FAILED
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return planner report.
        """

        return {
            "statistics": self.statistics(),
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "priority": task.priority.value,
                    "status": task.status.value,
                    "dependencies": task.dependencies,
                }
                for task
                in self._tasks.values()
            ],
        }

###############################################################################
# Global Planner
###############################################################################

planner: AIPlanner | None = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "TaskPriority",
    "TaskStatus",
    "AITask",
    "AIPlanner",
    "planner",
]