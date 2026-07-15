"""
==============================================================================
GEETA AI Engine

File        : process_manager.py
Package     : runtime
Description : Process Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Process Manager
###############################################################################


class ProcessManager:
    """
    Runtime process manager.

    Responsibilities

    - Process creation
    - Process termination
    - Output streaming
    - Background execution
    - Timeout handling
    - Process monitoring
    """

    def __init__(self) -> None:

        self._processes: dict[
            int,
            subprocess.Popen[str],
        ] = {}

        logger.info(
            "Process Manager initialized."
        )

    ###########################################################################

    def start(
        self,
        command: list[str],
        cwd: str | Path | None = None,
        env: dict[str, str] | None = None,
    ) -> int:
        """
        Start a background process.
        """

        logger.info(
            "Starting process: %s",
            " ".join(command),
        )

        process = subprocess.Popen(
            command,
            cwd=cwd,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self._processes[
            process.pid
        ] = process

        return process.pid

    ###########################################################################

    def process(
        self,
        pid: int,
    ) -> subprocess.Popen[str]:
        """
        Return a managed process.
        """

        return self._processes[
            pid
        ]

    ###########################################################################

    def running(
        self,
        pid: int,
    ) -> bool:
        """
        Check if a process is running.
        """

        process = self.process(
            pid,
        )

        return process.poll() is None

    ###########################################################################

    def terminate(
        self,
        pid: int,
    ) -> None:
        """
        Terminate a process.
        """

        process = self.process(
            pid,
        )

        process.terminate()

        logger.info(
            "Process terminated: %d",
            pid,
        )

    ###########################################################################

    def wait(
        self,
        pid: int,
        timeout: float | None = None,
    ) -> int:
        """
        Wait for process completion.
        """

        process = self.process(
            pid,
        )

        return process.wait(
            timeout=timeout,
        )
###############################################################################
# Output Streaming
###############################################################################

    def read_output(
        self,
        pid: int,
    ) -> tuple[str, str]:
        """
        Read stdout and stderr.
        """

        process = self.process(
            pid,
        )

        stdout, stderr = process.communicate()

        return (
            stdout or "",
            stderr or "",
        )

###############################################################################
# Cleanup
###############################################################################

    def cleanup(
        self,
    ) -> None:
        """
        Remove completed processes.
        """

        completed: list[int] = []

        for pid, process in self._processes.items():

            if process.poll() is not None:

                completed.append(
                    pid,
                )

        for pid in completed:

            self._processes.pop(
                pid,
                None,
            )

        logger.info(
            "Cleaned %d completed process(es).",
            len(completed),
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return process manager statistics.
        """

        running = sum(
            process.poll() is None
            for process in self._processes.values()
        )

        return {
            "managed_processes": len(
                self._processes
            ),
            "running_processes": running,
            "completed_processes": (
                len(self._processes)
                - running
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return process manager report.
        """

        return {
            "statistics": self.statistics(),
            "process_ids": sorted(
                self._processes.keys()
            ),
        }

###############################################################################
# Global Process Manager
###############################################################################

process_manager = ProcessManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "ProcessManager",
    "process_manager",
]