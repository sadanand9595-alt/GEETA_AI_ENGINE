"""
==============================================================================
GEETA AI Engine

File        : terminal_listener.py
Package     : listeners
Description : Terminal Output Listener

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import subprocess
import threading
from pathlib import Path

from config.logger import get_logger
from core.event_bus import publish

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Terminal Listener
###############################################################################


class TerminalListener:
    """
    Monitors terminal output in real time.
    """

    def __init__(
        self,
        command: list[str],
        working_directory: Path | None = None,
    ) -> None:

        self.command = command

        self.working_directory = working_directory

        self.process: subprocess.Popen | None = None

        self._thread: threading.Thread | None = None

        self._running = False

    ###########################################################################

    @property
    def running(self) -> bool:
        """
        Return listener state.
        """

        return self._running

    ###########################################################################

    def start(self) -> None:
        """
        Start terminal monitoring.
        """

        if self._running:
            return

        logger.info(
            "Starting Terminal Listener..."
        )

        self.process = subprocess.Popen(
            self.command,
            cwd=(
                str(self.working_directory)
                if self.working_directory
                else None
            ),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        self._running = True

        self._thread = threading.Thread(
            target=self._read_output,
            daemon=True,
            name="TerminalListener",
        )

        self._thread.start()

        logger.info(
            "Terminal Listener Started."
        )

    ###########################################################################

    def stop(self) -> None:
        """
        Stop terminal monitoring.
        """

        if not self._running:
            return

        logger.info(
            "Stopping Terminal Listener..."
        )

        if self.process:

            self.process.terminate()

            self.process.wait()

        if self._thread:

            self._thread.join(timeout=2)

        self._running = False

        logger.info(
            "Terminal Listener Stopped."
        )

    ###########################################################################

    def _read_output(self) -> None:
        """
        Read terminal output continuously.
        """

        assert self.process is not None

        assert self.process.stdout is not None

        for line in self.process.stdout:

            line = line.rstrip()

            if not line:
                continue

            logger.debug(line)

            publish(
                "terminal.output",
                text=line,
            )
###############################################################################
# Process Monitoring
###############################################################################

    def wait(self) -> int:
        """
        Wait for the monitored process to finish.

        Returns:
            Process exit code.
        """

        if self.process is None:
            return -1

        return_code = self.process.wait()

        logger.info(
            "Terminal process exited with code %d",
            return_code,
        )

        publish(
            "terminal.finished",
            return_code=return_code,
        )

        return return_code

###############################################################################
# Restart
###############################################################################

    def restart(self) -> None:
        """
        Restart the terminal listener.
        """

        logger.info(
            "Restarting Terminal Listener..."
        )

        self.stop()

        self.start()

###############################################################################
# Context Manager
###############################################################################

    def __enter__(self):
        """
        Context manager entry.
        """

        self.start()

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        """
        Context manager exit.
        """

        self.stop()

###############################################################################
# Helper Functions
###############################################################################


def start_terminal_listener(
    command: list[str],
    working_directory: Path | None = None,
) -> TerminalListener:
    """
    Create and start a terminal listener.
    """

    listener = TerminalListener(
        command=command,
        working_directory=working_directory,
    )

    listener.start()

    return listener


def stop_terminal_listener(
    listener: TerminalListener,
) -> None:
    """
    Stop a running terminal listener.
    """

    listener.stop()


###############################################################################
# Exports
###############################################################################

__all__ = [
    "TerminalListener",
    "start_terminal_listener",
    "stop_terminal_listener",
]