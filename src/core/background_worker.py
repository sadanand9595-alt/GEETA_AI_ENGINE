"""
==============================================================================
GEETA AI IDE

File        : background_worker.py
Package     : core
Description : Enterprise Background Worker

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import asyncio

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from itertools import count
from typing import Awaitable
from typing import Callable
from typing import Any
from uuid import uuid4

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Worker Status
###############################################################################


class WorkerStatus(str, Enum):

    STOPPED = "stopped"

    STARTING = "starting"

    RUNNING = "running"

    PAUSED = "paused"

    STOPPING = "stopping"

###############################################################################
# Task Priority
###############################################################################


class TaskPriority(int, Enum):

    CRITICAL = 0

    HIGH = 1

    NORMAL = 2

    LOW = 3

###############################################################################
# Background Task
###############################################################################


@dataclass(slots=True)
class BackgroundTask:

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    name: str = ""

    priority: TaskPriority = (
        TaskPriority.NORMAL
    )

    coroutine: (
        Callable[
            [],
            Awaitable[Any]
        ]
        | None
    ) = None

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

###############################################################################
# Background Worker
###############################################################################


class BackgroundWorker:
    """
    Enterprise Background Worker.

    Responsibilities

    - Async scheduling
    - Worker pool
    - Priority queue
    - Retry manager
    - Background AI jobs
    - Diagnostics jobs
    """

    ###########################################################################

    def __init__(
        self,
        workers: int = 4,
    ) -> None:

        self._workers = workers

        self._status = (
            WorkerStatus.STOPPED
        )

        self._queue = (
            asyncio.PriorityQueue()
        )

        self._counter = count()

        self._running: dict[
            str,
            asyncio.Task
        ] = {}

        logger.info(
            "Background Worker initialized."
        )

###############################################################################
# Status
###############################################################################

    @property
    def status(
        self,
    ) -> WorkerStatus:

        return self._status

###############################################################################
# Start
###############################################################################

    async def start(
        self,
    ) -> None:
        """
        Start worker pool.
        """

        self._status = (
            WorkerStatus.STARTING
        )

        for index in range(
            self._workers,
        ):

            task = asyncio.create_task(
                self.worker_loop(
                    index,
                )
            )

            self._running[
                f"worker-{index}"
            ] = task

        self._status = (
            WorkerStatus.RUNNING
        )

        logger.info(
            "%d workers started.",
            self._workers,
        )

###############################################################################
# Stop
###############################################################################

    async def stop(
        self,
    ) -> None:
        """
        Stop all workers.
        """

        self._status = (
            WorkerStatus.STOPPING
        )

        for task in (
            self._running.values()
        ):

            task.cancel()

        self._running.clear()

        self._status = (
            WorkerStatus.STOPPED
        )

        logger.info(
            "Background Worker stopped."
        )
###############################################################################
# Submit Task
###############################################################################

    async def submit(
        self,
        task: BackgroundTask,
    ) -> None:
        """
        Submit a task to the priority queue.
        """

        await self._queue.put(
            (
                task.priority.value,
                next(self._counter),
                task,
            )
        )

        logger.info(
            "Task submitted: %s",
            task.name,
        )

###############################################################################
# Worker Loop
###############################################################################

    async def worker_loop(
        self,
        worker_id: int,
    ) -> None:
        """
        Background worker execution loop.
        """

        logger.info(
            "Worker-%d started.",
            worker_id,
        )

        while (
            self._status
            == WorkerStatus.RUNNING
        ):

            try:

                (
                    _,
                    _,
                    task,
                ) = await self._queue.get()

                await self.execute(
                    task,
                )

                self._queue.task_done()

            except asyncio.CancelledError:

                logger.info(
                    "Worker-%d cancelled.",
                    worker_id,
                )

                raise

            except Exception:

                logger.exception(
                    "Worker-%d failed.",
                    worker_id,
                )

###############################################################################
# Execute Task
###############################################################################

    async def execute(
        self,
        task: BackgroundTask,
    ) -> None:
        """
        Execute background task.
        """

        logger.info(
            "Executing task: %s",
            task.name,
        )

        if task.coroutine is None:

            return

        await task.coroutine()

###############################################################################
# Cancel Task
###############################################################################

    async def cancel(
        self,
        task_id: str,
    ) -> bool:
        """
        Cancel running task.
        """

        task = self._running.get(
            task_id,
        )

        if task is None:

            return False

        task.cancel()

        logger.info(
            "Cancelled task: %s",
            task_id,
        )

        return True

###############################################################################
# Retry Task
###############################################################################

    async def retry(
        self,
        task: BackgroundTask,
        attempts: int = 3,
    ) -> bool:
        """
        Retry failed task.
        """

        for attempt in range(
            attempts,
        ):

            try:

                await self.execute(
                    task,
                )

                return True

            except Exception:

                logger.exception(
                    "Retry %d failed.",
                    attempt + 1,
                )

        return False

###############################################################################
# Queue Size
###############################################################################

    def queue_size(
        self,
    ) -> int:
        """
        Return queue size.
        """

        return self._queue.qsize()

###############################################################################
# Running Workers
###############################################################################

    def running_workers(
        self,
    ) -> int:
        """
        Return active worker count.
        """

        return len(
            self._running,
        )
###############################################################################
# AI Job
###############################################################################

    async def submit_ai_job(
        self,
        task: BackgroundTask,
    ) -> None:
        """
        Submit AI job.
        """

        logger.info(
            "Queue AI Job: %s",
            task.name,
        )

        await self.submit(
            task,
        )

###############################################################################
# Indexing Job
###############################################################################

    async def submit_index_job(
        self,
        task: BackgroundTask,
    ) -> None:
        """
        Submit workspace indexing job.
        """

        logger.info(
            "Queue Index Job: %s",
            task.name,
        )

        await self.submit(
            task,
        )

###############################################################################
# Diagnostics Job
###############################################################################

    async def submit_diagnostics_job(
        self,
        task: BackgroundTask,
    ) -> None:
        """
        Submit diagnostics job.
        """

        logger.info(
            "Queue Diagnostics Job: %s",
            task.name,
        )

        await self.submit(
            task,
        )

###############################################################################
# Git Job
###############################################################################

    async def submit_git_job(
        self,
        task: BackgroundTask,
    ) -> None:
        """
        Submit Git job.
        """

        logger.info(
            "Queue Git Job: %s",
            task.name,
        )

        await self.submit(
            task,
        )

###############################################################################
# Test Job
###############################################################################

    async def submit_test_job(
        self,
        task: BackgroundTask,
    ) -> None:
        """
        Submit testing job.
        """

        logger.info(
            "Queue Test Job: %s",
            task.name,
        )

        await self.submit(
            task,
        )

###############################################################################
# Progress
###############################################################################

    def progress(
        self,
    ) -> dict[str, int]:
        """
        Background worker progress.
        """

        return {

            "workers": self.running_workers(),

            "queued": self.queue_size(),
        }

###############################################################################
# Worker Event
###############################################################################

    def emit(
        self,
        event: str,
        task: BackgroundTask,
    ) -> None:
        """
        Emit worker event.
        """

        logger.info(
            "[%s] %s",
            event,
            task.name,
        )

###############################################################################
# Task Started
###############################################################################

    def task_started(
        self,
        task: BackgroundTask,
    ) -> None:
        """
        Notify task started.
        """

        self.emit(
            "started",
            task,
        )

###############################################################################
# Task Finished
###############################################################################

    def task_finished(
        self,
        task: BackgroundTask,
    ) -> None:
        """
        Notify task finished.
        """

        self.emit(
            "finished",
            task,
        )

###############################################################################
# Task Failed
###############################################################################

    def task_failed(
        self,
        task: BackgroundTask,
    ) -> None:
        """
        Notify task failure.
        """

        self.emit(
            "failed",
            task,
        )
###############################################################################
# Pause
###############################################################################

    async def pause(
        self,
    ) -> None:
        """
        Pause all workers.
        """

        self._status = (
            WorkerStatus.PAUSED
        )

        logger.info(
            "Background Worker paused."
        )

###############################################################################
# Resume
###############################################################################

    async def resume(
        self,
    ) -> None:
        """
        Resume workers.
        """

        self._status = (
            WorkerStatus.RUNNING
        )

        logger.info(
            "Background Worker resumed."
        )

###############################################################################
# Periodic Task
###############################################################################

    async def schedule_periodic(
        self,
        task: BackgroundTask,
        interval: float,
    ) -> None:
        """
        Execute task periodically.
        """

        while (
            self._status
            == WorkerStatus.RUNNING
        ):

            try:

                await self.execute(
                    task,
                )

            except Exception:

                logger.exception(
                    "Periodic task failed."
                )

            await asyncio.sleep(
                interval,
            )

###############################################################################
# Worker Health
###############################################################################

    def health(
        self,
    ) -> dict[str, str]:
        """
        Return worker health.
        """

        return {

            worker: "running"

            for worker
            in self._running.keys()
        }

###############################################################################
# Recovery
###############################################################################

    async def recover(
        self,
    ) -> None:
        """
        Recover failed workers.
        """

        if (
            self._status
            != WorkerStatus.RUNNING
        ):

            return

        for worker, task in list(
            self._running.items()
        ):

            if task.done():

                logger.warning(
                    "%s stopped unexpectedly.",
                    worker,
                )

                index = int(
                    worker.split("-")[1]
                )

                self._running[
                    worker
                ] = asyncio.create_task(
                    self.worker_loop(
                        index,
                    )
                )

###############################################################################
# Performance Metrics
###############################################################################

    def metrics(
        self,
    ) -> dict[str, int]:
        """
        Performance metrics.
        """

        return {

            "workers": len(
                self._running
            ),

            "queued": self.queue_size(),

            "running": sum(
                1
                for task
                in self._running.values()
                if not task.done()
            ),
        }

###############################################################################
# Resource Monitor
###############################################################################

    def resources(
        self,
    ) -> dict[str, object]:
        """
        Return worker resources.
        """

        return {

            "status": self._status.value,

            "workers": self.running_workers(),

            "queue": self.queue_size(),
        }

###############################################################################
# Heartbeat
###############################################################################

    async def heartbeat(
        self,
    ) -> None:
        """
        Background heartbeat.
        """

        logger.debug(
            "Worker heartbeat."
        )
###############################################################################
# Pause
###############################################################################

    async def pause(
        self,
    ) -> None:
        """
        Pause all workers.
        """

        self._status = (
            WorkerStatus.PAUSED
        )

        logger.info(
            "Background Worker paused."
        )

###############################################################################
# Resume
###############################################################################

    async def resume(
        self,
    ) -> None:
        """
        Resume workers.
        """

        self._status = (
            WorkerStatus.RUNNING
        )

        logger.info(
            "Background Worker resumed."
        )

###############################################################################
# Periodic Task
###############################################################################

    async def schedule_periodic(
        self,
        task: BackgroundTask,
        interval: float,
    ) -> None:
        """
        Execute task periodically.
        """

        while (
            self._status
            == WorkerStatus.RUNNING
        ):

            try:

                await self.execute(
                    task,
                )

            except Exception:

                logger.exception(
                    "Periodic task failed."
                )

            await asyncio.sleep(
                interval,
            )

###############################################################################
# Worker Health
###############################################################################

    def health(
        self,
    ) -> dict[str, str]:
        """
        Return worker health.
        """

        return {

            worker: "running"

            for worker
            in self._running.keys()
        }

###############################################################################
# Recovery
###############################################################################

    async def recover(
        self,
    ) -> None:
        """
        Recover failed workers.
        """

        if (
            self._status
            != WorkerStatus.RUNNING
        ):

            return

        for worker, task in list(
            self._running.items()
        ):

            if task.done():

                logger.warning(
                    "%s stopped unexpectedly.",
                    worker,
                )

                index = int(
                    worker.split("-")[1]
                )

                self._running[
                    worker
                ] = asyncio.create_task(
                    self.worker_loop(
                        index,
                    )
                )

###############################################################################
# Performance Metrics
###############################################################################

    def metrics(
        self,
    ) -> dict[str, int]:
        """
        Performance metrics.
        """

        return {

            "workers": len(
                self._running
            ),

            "queued": self.queue_size(),

            "running": sum(
                1
                for task
                in self._running.values()
                if not task.done()
            ),
        }

###############################################################################
# Resource Monitor
###############################################################################

    def resources(
        self,
    ) -> dict[str, object]:
        """
        Return worker resources.
        """

        return {

            "status": self._status.value,

            "workers": self.running_workers(),

            "queue": self.queue_size(),
        }

###############################################################################
# Heartbeat
###############################################################################

    async def heartbeat(
        self,
    ) -> None:
        """
        Background heartbeat.
        """

        logger.debug(
            "Worker heartbeat."
        )