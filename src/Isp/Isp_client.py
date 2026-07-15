"""
==============================================================================
GEETA AI IDE

File        : lsp_client.py
Package     : lsp
Description : Language Server Protocol Client

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import json
import subprocess
import threading
from itertools import count
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# LSP Client
###############################################################################


class LSPClient:
    """
    Enterprise Language Server Protocol Client.

    Responsibilities

    - JSON RPC
    - Process management
    - Initialize
    - Shutdown
    - Notifications
    - Requests
    """

    ###########################################################################

    def __init__(
        self,
        command: list[str],
    ) -> None:

        self._command = command

        self._process: subprocess.Popen[
            bytes
        ] | None = None

        self._request_ids = count(1)

        self._running = False

        self._reader_thread: threading.Thread | None = None

        logger.info(
            "LSP Client initialized."
        )

###############################################################################
# Process
###############################################################################

    def start(
        self,
    ) -> None:
        """
        Start language server.
        """

        if self._running:

            return

        self._process = subprocess.Popen(
            self._command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self._running = True

        logger.info(
            "Language Server started."
        )

###############################################################################
# Stop
###############################################################################

    def stop(
        self,
    ) -> None:
        """
        Stop language server.
        """

        if not self._running:

            return

        assert self._process is not None

        self._process.terminate()

        self._process.wait()

        self._running = False

        logger.info(
            "Language Server stopped."
        )

###############################################################################
# JSON RPC
###############################################################################

    def send_request(
        self,
        method: str,
        params: dict[str, Any],
    ) -> int:
        """
        Send JSON RPC request.
        """

        if (
            not self._running
            or self._process is None
        ):

            raise RuntimeError(
                "LSP server is not running."
            )

        request_id = next(
            self._request_ids
        )

        payload = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": params,
        }

        body = json.dumps(
            payload
        ).encode(
            "utf-8"
        )

        header = (
            f"Content-Length: {len(body)}\r\n\r\n"
        ).encode(
            "ascii"
        )

        assert self._process.stdin is not None

        self._process.stdin.write(
            header + body
        )

        self._process.stdin.flush()

        return request_id

###############################################################################
# Notification
###############################################################################

    def send_notification(
        self,
        method: str,
        params: dict[str, Any],
    ) -> None:
        """
        Send JSON RPC notification.
        """

        if (
            not self._running
            or self._process is None
        ):

            return

        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
        }

        body = json.dumps(
            payload
        ).encode(
            "utf-8"
        )

        header = (
            f"Content-Length: {len(body)}\r\n\r\n"
        ).encode(
            "ascii"
        )

        assert self._process.stdin is not None

        self._process.stdin.write(
            header + body
        )

        self._process.stdin.flush()
###############################################################################
# Reader
###############################################################################

    def read_message(
        self,
    ) -> dict[str, Any] | None:
        """
        Read a JSON-RPC message.
        """

        if (
            not self._running
            or self._process is None
        ):

            return None

        assert self._process.stdout is not None

        content_length = 0

        while True:

            line = self._process.stdout.readline()

            if not line:

                return None

            line = line.decode(
                "ascii"
            ).strip()

            if not line:

                break

            if line.lower().startswith(
                "content-length:"
            ):

                content_length = int(
                    line.split(":")[1].strip()
                )

        if content_length <= 0:

            return None

        body = self._process.stdout.read(
            content_length
        )

        return json.loads(
            body.decode(
                "utf-8"
            )
        )

###############################################################################
# Initialize
###############################################################################

    def initialize(
        self,
        root_uri: str,
    ) -> int:
        """
        Send initialize request.
        """

        return self.send_request(
            "initialize",
            {
                "processId": None,
                "rootUri": root_uri,
                "capabilities": {},
            },
        )

###############################################################################
# Shutdown
###############################################################################

    def shutdown(
        self,
    ) -> int:
        """
        Send shutdown request.
        """

        return self.send_request(
            "shutdown",
            {},
        )

###############################################################################
# Exit
###############################################################################

    def exit(
        self,
    ) -> None:
        """
        Notify server to exit.
        """

        self.send_notification(
            "exit",
            {},
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return client statistics.
        """

        return {
            "running": self._running,
            "command": self._command,
            "next_request_id": next(
                self._request_ids
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return LSP client report.
        """

        return {
            "statistics": self.statistics(),
        }

###############################################################################
# Exports
###############################################################################

__all__ = [
    "LSPClient",
]