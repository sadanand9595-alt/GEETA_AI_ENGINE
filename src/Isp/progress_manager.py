"""
==============================================================================
GEETA AI IDE

File        : progress_manager.py
Package     : lsp
Description : LSP Progress Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Progress State
###############################################################################


class ProgressState(str, Enum):
    """
    Progress state.
    """

    BEGIN = "begin"

    REPORT = "report"

    END = "end"

###############################################################################
# Progress Item
###############################################################################


@dataclass(slots=True)
class ProgressItem:
    """
    Represents a running task.
    """

    token: str

    title: str

    state: ProgressState

    percentage: int = 0

    message: str = ""

    cancellable: bool = False

###############################################################################
# Progress Manager
###############################################################################


class ProgressManager:
    """
    Enterprise Progress Manager.

    Responsibilities

    - LSP $/progress
    - Background indexing
    - Diagnostics progress
    - AI task progress
    - Status bar updates
    """

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._tasks: dict[
            str,
            ProgressItem,
        ] = {}

        logger.info(
            "Progress Manager initialized."
        )

###############################################################################
# Begin
###############################################################################

    def begin(
        self,
        token: str,
        title: str,
        cancellable: bool = False,
    ) -> None:
        """
        Begin progress.
        """

        self._tasks[token] = ProgressItem(
            token=token,
            title=title,
            state=ProgressState.BEGIN,
            cancellable=cancellable,
        )

###############################################################################
# Report
###############################################################################

    def report(
        self,
        token: str,
        percentage: int,
        message: str = "",
    ) -> None:
        """
        Update progress.
        """

        task = self._tasks.get(
            token,
        )

        if task is None:

            return

        task.state = ProgressState.REPORT

        task.percentage = max(
            0,
            min(
                percentage,
                100,
            ),
        )

        task.message = message

###############################################################################
# Finish
###############################################################################

    def finish(
        self,
        token: str,
    ) -> None:
        """
        Finish progress.
        """

        task = self._tasks.get(
            token,
        )

        if task is None:

            return

        task.state = ProgressState.END

        task.percentage = 100
###############################################################################
# Cancel Task
###############################################################################

    def cancel(
        self,
        token: str,
    ) -> bool:
        """
        Cancel a running task.
        """

        task = self._tasks.get(
            token,
        )

        if task is None:

            return False

        if not task.cancellable:

            return False

        del self._tasks[
            token
        ]

        return True

###############################################################################
# Active Tasks
###############################################################################

    def active_tasks(
        self,
    ) -> list[ProgressItem]:
        """
        Return active progress tasks.
        """

        return [
            task
            for task
            in self._tasks.values()
            if task.state
            != ProgressState.END
        ]

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return progress manager statistics.
        """

        completed = sum(
            1
            for task
            in self._tasks.values()
            if task.state
            == ProgressState.END
        )

        active = sum(
            1
            for task
            in self._tasks.values()
            if task.state
            != ProgressState.END
        )

        return {
            "total_tasks": len(
                self._tasks
            ),
            "active_tasks": active,
            "completed_tasks": completed,
        }

###############################################################################
# Report
###############################################################################

    def report_data(
        self,
    ) -> dict[str, Any]:
        """
        Return progress manager report.
        """

        return {
            "statistics": self.statistics(),
            "tasks": [
                {
                    "token": task.token,
                    "title": task.title,
                    "state": task.state.value,
                    "percentage": task.percentage,
                    "message": task.message,
                }
                for task
                in self._tasks.values()
            ],
        }

###############################################################################
# Global Progress Manager
###############################################################################

progress_manager: (
    ProgressManager | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "ProgressState",
    "ProgressItem",
    "ProgressManager",
    "progress_manager",
]