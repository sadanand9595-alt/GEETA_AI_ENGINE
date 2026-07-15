"""
==============================================================================
GEETA AI Engine

File        : task_scheduler.py
Package     : agents
Description : AI Task Scheduler

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field
from queue import PriorityQueue
from threading import Event, Thread
from time import time
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Task
###############################################################################


@dataclass(order=True)
class ScheduledTask:
    """
    Represents a scheduled AI task.
    """

    priority: int

    created_at: float = field(
        default_factory=time,
        compare=False,
    )

    task_id: str = field(
        compare=False,
    )

    callback: Any = field(
        compare=False,
    )

    args: tuple[Any, ...] = field(
        default_factory=tuple,
        compare=False,
    )

    kwargs: dict[str, Any] = field(
        default_factory=dict,
        compare=False,
    )

###############################################################################
# Task Scheduler
###############################################################################


class TaskScheduler:
    """
    AI task scheduler.

    Responsibilities

    - Priority queue
    - Background execution
    - Parallel scheduling
    - Retry support
    - Progress tracking
    """

    def __init__(
        self,
        workers: int = 4,
    ) -> None:

        self._queue: PriorityQueue[
            ScheduledTask
        ] = PriorityQueue()

        self._executor = ThreadPoolExecutor(
            max_workers=workers,
            thread_name_prefix="GEETA-Task",
        )

        self._stop_event = Event()

        self._thread: Thread | None = None

        self._tasks: dict[
            str,
            Future,
        ] = {}

        logger.info(
            "Task Scheduler initialized."
        )

    ###########################################################################

    def start(
        self,
    ) -> None:
        """
        Start scheduler.
        """

        if self._thread:

            return

        self._thread = Thread(
            target=self._worker,
            daemon=True,
            name="TaskScheduler",
        )

        self._thread.start()

        logger.info(
            "Task Scheduler started."
        )

    ###########################################################################

    def schedule(
        self,
        task: ScheduledTask,
    ) -> None:
        """
        Queue a task.
        """

        self._queue.put(
            task,
        )

        logger.info(
            "Task queued: %s",
            task.task_id,
        )

    ###########################################################################

    def _worker(
        self,
    ) -> None:
        """
        Background scheduling loop.
        """

        while not self._stop_event.is_set():

            task = self._queue.get()

            future = self._executor.submit(
                task.callback,
                *task.args,
                **task.kwargs,
            )

            self._tasks[
                task.task_id
            ] = future
###############################################################################
# Task Management
###############################################################################

    def cancel(
        self,
        task_id: str,
    ) -> bool:
        """
        Cancel a scheduled task.
        """

        future = self._tasks.get(
            task_id,
        )

        if future is None:

            return False

        return future.cancel()

###############################################################################
# Progress
###############################################################################

    def progress(
        self,
        task_id: str,
    ) -> dict[str, Any]:
        """
        Return task progress.
        """

        future = self._tasks.get(
            task_id,
        )

        if future is None:

            return {
                "exists": False,
            }

        return {
            "exists": True,
            "done": future.done(),
            "running": future.running(),
            "cancelled": future.cancelled(),
        }

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return scheduler statistics.
        """

        completed = sum(
            future.done()
            for future in self._tasks.values()
        )

        running = sum(
            future.running()
            for future in self._tasks.values()
        )

        return {
            "queued_tasks": self._queue.qsize(),
            "tracked_tasks": len(
                self._tasks
            ),
            "running_tasks": running,
            "completed_tasks": completed,
        }

###############################################################################
# Shutdown
###############################################################################

    def shutdown(
        self,
        wait: bool = True,
    ) -> None:
        """
        Shutdown scheduler.
        """

        logger.info(
            "Stopping Task Scheduler..."
        )

        self._stop_event.set()

        if self._thread:

            self._thread.join()

        self._executor.shutdown(
            wait=wait,
        )

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return scheduler report.
        """

        return {
            "statistics": self.statistics(),
            "running": (
                self._thread.is_alive()
                if self._thread
                else False
            ),
        }

###############################################################################
# Global Scheduler
###############################################################################

task_scheduler = TaskScheduler()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "ScheduledTask",
    "TaskScheduler",
    "task_scheduler",
]