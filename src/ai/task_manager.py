"""
==============================================================================
GEETA AI IDE

File        : task_manager.py
Package     : ai
Description : Autonomous AI Task Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from datetime import datetime

from config.logger import get_logger

from ai.planner import (
    AITask,
    AIPlanner,
    TaskPriority,
    TaskStatus,
)

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Queue Item
###############################################################################


_PRIORITY = {
    TaskPriority.CRITICAL: 0,
    TaskPriority.HIGH: 1,
    TaskPriority.NORMAL: 2,
    TaskPriority.LOW: 3,
}


@dataclass(order=True, slots=True)
class QueueItem:
    """
    Priority queue item.
    """

    priority: int

    created: float

    task_id: str = field(compare=False)

###############################################################################
# AI Task Manager
###############################################################################


class AITaskManager:
    """
    Enterprise AI Task Manager.

    Responsibilities

    - Task Queue
    - Priority Scheduling
    - Dependency Resolution
    - Retry Logic
    - Background Execution
    """

    ###########################################################################

    def __init__(
        self,
        planner: AIPlanner,
    ) -> None:

        self._planner = planner

        self._queue: list[
            QueueItem
        ] = []

        self._running: set[str] = set()

        self._completed: set[str] = set()

        self._failed: set[str] = set()

        logger.info(
            "AI Task Manager initialized."
        )

###############################################################################
# Queue Task
###############################################################################

    def enqueue(
        self,
        task: AITask,
    ) -> None:
        """
        Add task to scheduler.
        """

        heapq.heappush(
            self._queue,
            QueueItem(
                priority=_PRIORITY[
                    task.priority
                ],
                created=datetime.now().timestamp(),
                task_id=task.id,
            ),
        )

###############################################################################
# Next Task
###############################################################################

    def next_task(
        self,
    ) -> AITask | None:
        """
        Return highest priority task.
        """

        while self._queue:

            item = heapq.heappop(
                self._queue,
            )

            task = self._planner.task(
                item.task_id,
            )

            if task is None:

                continue

            if (
                task.status
                != TaskStatus.PENDING
            ):

                continue

            return task

        return None

###############################################################################
# Running
###############################################################################

    def mark_running(
        self,
        task: AITask,
    ) -> None:
        """
        Mark task as running.
        """

        task.status = TaskStatus.RUNNING

        self._running.add(
            task.id,
        )
###############################################################################
# Complete Task
###############################################################################

    def mark_completed(
        self,
        task: AITask,
    ) -> None:
        """
        Mark task as completed.
        """

        task.status = TaskStatus.COMPLETED

        self._running.discard(
            task.id,
        )

        self._completed.add(
            task.id,
        )

###############################################################################
# Fail Task
###############################################################################

    def mark_failed(
        self,
        task: AITask,
    ) -> None:
        """
        Mark task as failed.
        """

        task.status = TaskStatus.FAILED

        self._running.discard(
            task.id,
        )

        self._failed.add(
            task.id,
        )

###############################################################################
# Retry Task
###############################################################################

    def retry(
        self,
        task: AITask,
    ) -> None:
        """
        Retry a failed task.
        """

        if task.id in self._failed:

            self._failed.remove(
                task.id,
            )

        task.status = TaskStatus.PENDING

        self.enqueue(
            task,
        )

###############################################################################
# Queue Ready Tasks
###############################################################################

    def schedule_ready_tasks(
        self,
    ) -> int:
        """
        Schedule all ready tasks from planner.
        """

        count = 0

        for task in self._planner.ready_tasks():

            self.enqueue(
                task,
            )

            count += 1

        return count

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return task manager statistics.
        """

        return {
            "queued": len(
                self._queue,
            ),
            "running": len(
                self._running,
            ),
            "completed": len(
                self._completed,
            ),
            "failed": len(
                self._failed,
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return task manager report.
        """

        return {
            "statistics": self.statistics(),
            "queue_size": len(
                self._queue,
            ),
            "running": sorted(
                self._running,
            ),
            "completed": sorted(
                self._completed,
            ),
            "failed": sorted(
                self._failed,
            ),
        }

###############################################################################
# Global Task Manager
###############################################################################

task_manager: (
    AITaskManager | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "QueueItem",
    "AITaskManager",
    "task_manager",
]