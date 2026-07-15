"""
==============================================================================
GEETA AI Engine

File        : python_traceback_listener.py
Package     : listeners
Description : Python Traceback Listener

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import re
from pathlib import Path

from config.logger import get_logger
from core.event_bus import publish

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Traceback Patterns
###############################################################################

TRACEBACK_START = "Traceback (most recent call last):"

FILE_PATTERN = re.compile(
    r'File "(.+?)", line (\d+)'
)

ERROR_PATTERN = re.compile(
    r"([A-Za-z_]+Error):\s*(.+)"
)

###############################################################################
# Traceback Listener
###############################################################################


class PythonTracebackListener:
    """
    Detects and parses Python tracebacks.
    """

    def __init__(self) -> None:

        self._collecting = False

        self._buffer: list[str] = []

    ###########################################################################

    def reset(self) -> None:
        """
        Reset internal state.
        """

        self._collecting = False

        self._buffer.clear()

    ###########################################################################

    def process_line(
        self,
        line: str,
    ) -> None:
        """
        Process one line of terminal output.
        """

        line = line.rstrip()

        #######################################################################
        # Start Traceback
        #######################################################################

        if TRACEBACK_START in line:

            logger.info(
                "Python traceback detected."
            )

            self.reset()

            self._collecting = True

            self._buffer.append(line)

            return

        #######################################################################
        # Collect
        #######################################################################

        if self._collecting:

            self._buffer.append(line)

            if ERROR_PATTERN.match(line):

                self._finish()

    ###########################################################################

    def _finish(self) -> None:
        """
        Finish traceback collection.
        """

        traceback_text = "\n".join(
            self._buffer
        )

        file_match = None

        line_number = None

        for item in self._buffer:

            match = FILE_PATTERN.search(item)

            if match:

                file_match = Path(
                    match.group(1)
                )

                line_number = int(
                    match.group(2)
                )

        error_name = "UnknownError"

        error_message = ""

        last_line = self._buffer[-1]

        match = ERROR_PATTERN.match(
            last_line
        )

        if match:

            error_name = match.group(1)

            error_message = match.group(2)

        logger.error(
            "%s : %s",
            error_name,
            error_message,
        )

        publish(
            "python.traceback",
            file=file_match,
            line=line_number,
            error=error_name,
            message=error_message,
            traceback=traceback_text,
        )

        self.reset()
###############################################################################
# Public API
###############################################################################


    def process_lines(
        self,
        lines: list[str],
    ) -> None:
        """
        Process multiple terminal output lines.
        """

        for line in lines:

            self.process_line(line)

    ###########################################################################

    @property
    def collecting(self) -> bool:
        """
        Return current traceback collection state.
        """

        return self._collecting

    ###########################################################################

    @property
    def buffered_lines(self) -> int:
        """
        Return number of buffered traceback lines.
        """

        return len(self._buffer)

###############################################################################
# Helper Functions
###############################################################################


def parse_traceback(
    traceback_text: str,
) -> None:
    """
    Parse a complete traceback string.
    """

    listener = PythonTracebackListener()

    listener.process_lines(
        traceback_text.splitlines()
    )


def parse_terminal_line(
    listener: PythonTracebackListener,
    line: str,
) -> None:
    """
    Feed one terminal line into the listener.
    """

    listener.process_line(line)


###############################################################################
# Global Instance
###############################################################################

traceback_listener = PythonTracebackListener()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "PythonTracebackListener",
    "traceback_listener",
    "parse_traceback",
    "parse_terminal_line",
]