"""
==============================================================================
GEETA AI Engine

File        : debug_adapter.py
Package     : runtime
Description : Debug Adapter Protocol (DAP) Client

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import json
import socket
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Debug Adapter
###############################################################################


class DebugAdapter:
    """
    Debug Adapter Protocol client.

    Responsibilities

    - DAP communication
    - Launch requests
    - Attach requests
    - Breakpoint synchronization
    - Variable inspection
    - Stack traces
    """

    def __init__(self) -> None:

        self._socket: socket.socket | None = None

        self._connected = False

        self._sequence = 1

        logger.info(
            "Debug Adapter initialized."
        )

    ###########################################################################

    def connect(
        self,
        host: str = "127.0.0.1",
        port: int = 5678,
    ) -> bool:
        """
        Connect to a DAP server.
        """

        try:

            self._socket = socket.create_connection(
                (
                    host,
                    port,
                )
            )

            self._connected = True

            logger.info(
                "Connected to DAP server."
            )

            return True

        except OSError:

            logger.exception(
                "Unable to connect to DAP server."
            )

            return False

    ###########################################################################

    def disconnect(
        self,
    ) -> None:
        """
        Disconnect from DAP server.
        """

        if self._socket:

            self._socket.close()

            self._socket = None

        self._connected = False

    ###########################################################################

    def send_request(
        self,
        command: str,
        arguments: dict[str, Any] | None = None,
    ) -> None:
        """
        Send a DAP request.
        """

        if not self._connected:

            raise RuntimeError(
                "Debug adapter is not connected."
            )

        message = {
            "seq": self._sequence,
            "type": "request",
            "command": command,
            "arguments": arguments or {},
        }

        payload = json.dumps(
            message,
        ).encode(
            "utf-8",
        )

        header = (
            f"Content-Length: {len(payload)}\r\n\r\n"
        ).encode(
            "utf-8",
        )

        assert self._socket is not None

        self._socket.sendall(
            header + payload,
        )

        self._sequence += 1

    ###########################################################################

    def launch(
        self,
        program: str,
    ) -> None:
        """
        Launch a debug target.
        """

        self.send_request(
            "launch",
            {
                "program": program,
            },
        )

    ###########################################################################

    def attach(
        self,
        process_id: int,
    ) -> None:
        """
        Attach to an existing process.
        """

        self.send_request(
            "attach",
            {
                "processId": process_id,
            },
        )
###############################################################################
# Debug Commands
###############################################################################

    def continue_execution(
        self,
        thread_id: int,
    ) -> None:
        """
        Continue execution.
        """

        self.send_request(
            "continue",
            {
                "threadId": thread_id,
            },
        )

    ###########################################################################

    def pause(
        self,
        thread_id: int,
    ) -> None:
        """
        Pause execution.
        """

        self.send_request(
            "pause",
            {
                "threadId": thread_id,
            },
        )

    ###########################################################################

    def step_over(
        self,
        thread_id: int,
    ) -> None:
        """
        Step over.
        """

        self.send_request(
            "next",
            {
                "threadId": thread_id,
            },
        )

    ###########################################################################

    def step_into(
        self,
        thread_id: int,
    ) -> None:
        """
        Step into.
        """

        self.send_request(
            "stepIn",
            {
                "threadId": thread_id,
            },
        )

    ###########################################################################

    def step_out(
        self,
        thread_id: int,
    ) -> None:
        """
        Step out.
        """

        self.send_request(
            "stepOut",
            {
                "threadId": thread_id,
            },
        )

###############################################################################
# Breakpoints
###############################################################################

    def set_breakpoints(
        self,
        source: str,
        lines: list[int],
    ) -> None:
        """
        Synchronize breakpoints.
        """

        self.send_request(
            "setBreakpoints",
            {
                "source": {
                    "path": source,
                },
                "breakpoints": [
                    {"line": line}
                    for line in lines
                ],
            },
        )

###############################################################################
# Inspection
###############################################################################

    def stack_trace(
        self,
        thread_id: int,
    ) -> None:
        """
        Request stack trace.
        """

        self.send_request(
            "stackTrace",
            {
                "threadId": thread_id,
            },
        )

    ###########################################################################

    def variables(
        self,
        variables_reference: int,
    ) -> None:
        """
        Request variables.
        """

        self.send_request(
            "variables",
            {
                "variablesReference":
                    variables_reference,
            },
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return adapter statistics.
        """

        return {
            "connected": self._connected,
            "sequence": self._sequence,
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return adapter report.
        """

        return {
            "statistics": self.statistics(),
        }

###############################################################################
# Global Adapter
###############################################################################

debug_adapter = DebugAdapter()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "DebugAdapter",
    "debug_adapter",
]