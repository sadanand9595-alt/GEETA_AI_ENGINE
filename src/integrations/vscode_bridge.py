"""
==============================================================================
GEETA AI IDE

File        : vscode_bridge.py
Package     : integrations
Description : Enterprise VS Code Bridge

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Bridge State
###############################################################################


class BridgeState(str, Enum):

    DISCONNECTED = "disconnected"

    CONNECTING = "connecting"

    CONNECTED = "connected"

    RECONNECTING = "reconnecting"

    CLOSED = "closed"


###############################################################################
# RPC Message
###############################################################################


@dataclass(slots=True)
class RPCMessage:
    """
    JSON-RPC message.
    """

    method: str

    params: dict[str, Any] = field(
        default_factory=dict
    )

    message_id: int | None = None

###############################################################################
# VS Code Bridge
###############################################################################


class VSCodeBridge:
    """
    Enterprise VS Code Bridge.

    Responsibilities

    - VS Code communication
    - JSON RPC
    - Event routing
    - Workspace synchronization
    - Editor synchronization
    - AI communication
    """

    ###########################################################################

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8765,
    ) -> None:

        self.host = host

        self.port = port

        self.state = (
            BridgeState.DISCONNECTED
        )

        self._reader = None

        self._writer = None

        self._request_id = 0

        logger.info(
            "VS Code Bridge initialized."
        )

###############################################################################
# Connect
###############################################################################

    async def connect(
        self,
    ) -> bool:
        """
        Connect to VS Code.
        """

        if self.state == BridgeState.CONNECTED:

            return True

        self.state = (
            BridgeState.CONNECTING
        )

        try:

            self._reader, self._writer = (
                await asyncio.open_connection(
                    self.host,
                    self.port,
                )
            )

            self.state = (
                BridgeState.CONNECTED
            )

            logger.info(
                "Connected to VS Code."
            )

            return True

        except Exception:

            self.state = (
                BridgeState.DISCONNECTED
            )

            logger.exception(
                "Connection failed."
            )

            return False

###############################################################################
# Disconnect
###############################################################################

    async def disconnect(
        self,
    ) -> None:

        if self._writer is not None:

            self._writer.close()

            await self._writer.wait_closed()

        self.state = (
            BridgeState.CLOSED
        )

        logger.info(
            "Bridge closed."
        )

###############################################################################
# Next Request ID
###############################################################################

    def next_request_id(
        self,
    ) -> int:

        self._request_id += 1

        return self._request_id
###############################################################################
# JSON RPC Request
###############################################################################

    async def send_request(
        self,
        method: str,
        params: dict[str, Any] | None = None,
    ) -> int:
        """
        Send JSON-RPC request.
        """

        if self.state != BridgeState.CONNECTED:

            raise RuntimeError(
                "VS Code Bridge is not connected."
            )

        request_id = self.next_request_id()

        message = RPCMessage(
            method=method,
            params=params or {},
            message_id=request_id,
        )

        payload = {
            "jsonrpc": "2.0",
            "id": message.message_id,
            "method": message.method,
            "params": message.params,
        }

        data = (
            json.dumps(payload)
            + "\n"
        ).encode()

        self._writer.write(
            data,
        )

        await self._writer.drain()

        logger.debug(
            "RPC Request -> %s",
            payload,
        )

        return request_id

###############################################################################
# JSON RPC Notification
###############################################################################

    async def notify(
        self,
        method: str,
        params: dict[str, Any] | None = None,
    ) -> None:
        """
        Send notification.
        """

        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
        }

        self._writer.write(
            (
                json.dumps(payload)
                + "\n"
            ).encode()
        )

        await self._writer.drain()

###############################################################################
# Receive Loop
###############################################################################

    async def receive_loop(
        self,
    ) -> None:
        """
        Receive incoming messages.
        """

        while (
            self.state
            == BridgeState.CONNECTED
        ):

            try:

                line = (
                    await self._reader.readline()
                )

                if not line:

                    logger.warning(
                        "Connection closed."
                    )

                    break

                payload = json.loads(
                    line.decode()
                )

                await self.handle_message(
                    payload,
                )

            except asyncio.CancelledError:

                raise

            except Exception:

                logger.exception(
                    "Receive loop failed."
                )

                break

        self.state = (
            BridgeState.DISCONNECTED
        )

###############################################################################
# Message Handler
###############################################################################

    async def handle_message(
        self,
        message: dict[str, Any],
    ) -> None:
        """
        Handle incoming JSON-RPC message.
        """

        logger.debug(
            "RPC <- %s",
            message,
        )

        if "method" in message:

            await self.dispatch_event(
                message["method"],
                message.get(
                    "params",
                    {},
                ),
            )

###############################################################################
# Event Dispatcher
###############################################################################

    async def dispatch_event(
        self,
        event: str,
        params: dict[str, Any],
    ) -> None:
        """
        Dispatch VS Code event.
        """

        logger.info(
            "Event: %s",
            event,
        )

        if event == "workspace/opened":

            logger.info(
                "Workspace opened."
            )

        elif event == "editor/changed":

            logger.info(
                "Editor changed."
            )

        elif event == "file/saved":

            logger.info(
                "File saved."
            )

###############################################################################
# Reconnect
###############################################################################

    async def reconnect(
        self,
        delay: float = 3.0,
    ) -> None:
        """
        Attempt automatic reconnection.
        """

        self.state = (
            BridgeState.RECONNECTING
        )

        logger.info(
            "Reconnecting..."
        )

        await asyncio.sleep(
            delay,
        )

        await self.connect()
###############################################################################
# Workspace API
###############################################################################

    async def open_workspace(
        self,
        workspace: str,
    ) -> int:
        """
        Open workspace.
        """

        return await self.send_request(
            "workspace/open",
            {
                "path": workspace,
            },
        )

###############################################################################
# Active Editor
###############################################################################

    async def active_editor(
        self,
    ) -> int:
        """
        Request active editor.
        """

        return await self.send_request(
            "editor/active",
        )

###############################################################################
# Open File
###############################################################################

    async def open_file(
        self,
        file_path: str,
    ) -> int:
        """
        Open file in VS Code.
        """

        return await self.send_request(
            "editor/openFile",
            {
                "path": file_path,
            },
        )

###############################################################################
# Save File
###############################################################################

    async def save_file(
        self,
        file_path: str,
    ) -> int:
        """
        Save file.
        """

        return await self.send_request(
            "editor/saveFile",
            {
                "path": file_path,
            },
        )

###############################################################################
# Close File
###############################################################################

    async def close_file(
        self,
        file_path: str,
    ) -> int:
        """
        Close editor.
        """

        return await self.send_request(
            "editor/closeFile",
            {
                "path": file_path,
            },
        )

###############################################################################
# Read File
###############################################################################

    async def read_file(
        self,
        file_path: str,
    ) -> int:
        """
        Read file contents.
        """

        return await self.send_request(
            "editor/readFile",
            {
                "path": file_path,
            },
        )

###############################################################################
# Replace File
###############################################################################

    async def replace_file(
        self,
        file_path: str,
        content: str,
    ) -> int:
        """
        Replace complete file.
        """

        return await self.send_request(
            "editor/replaceFile",
            {
                "path": file_path,
                "content": content,
            },
        )

###############################################################################
# Cursor Position
###############################################################################

    async def cursor_position(
        self,
    ) -> int:
        """
        Request cursor position.
        """

        return await self.send_request(
            "editor/cursor",
        )

###############################################################################
# Selection
###############################################################################

    async def selection(
        self,
    ) -> int:
        """
        Request editor selection.
        """

        return await self.send_request(
            "editor/selection",
        )

###############################################################################
# Diagnostics
###############################################################################

    async def diagnostics(
        self,
    ) -> int:
        """
        Request diagnostics.
        """

        return await self.send_request(
            "diagnostics/list",
        )

###############################################################################
# Problems Panel
###############################################################################

    async def problems(
        self,
    ) -> int:
        """
        Request Problems Panel.
        """

        return await self.send_request(
            "diagnostics/problems",
        )
###############################################################################
# Execute Terminal Command
###############################################################################

    async def execute_terminal(
        self,
        command: str,
        cwd: str | None = None,
    ) -> int:
        """
        Execute command inside VS Code terminal.
        """

        return await self.send_request(
            "terminal/execute",
            {
                "command": command,
                "cwd": cwd,
            },
        )

###############################################################################
# Run Python
###############################################################################

    async def run_python(
        self,
        script: str,
    ) -> int:
        """
        Run Python script.
        """

        return await self.execute_terminal(
            f'python "{script}"'
        )

###############################################################################
# Run Pytest
###############################################################################

    async def run_tests(
        self,
        target: str = "",
    ) -> int:
        """
        Execute pytest.
        """

        command = "pytest"

        if target:

            command += f" {target}"

        return await self.execute_terminal(
            command,
        )

###############################################################################
# Git Status
###############################################################################

    async def git_status(
        self,
    ) -> int:
        """
        Execute git status.
        """

        return await self.execute_terminal(
            "git status",
        )

###############################################################################
# Git Commit
###############################################################################

    async def git_commit(
        self,
        message: str,
    ) -> int:
        """
        Commit changes.
        """

        return await self.execute_terminal(
            f'git commit -m "{message}"'
        )

###############################################################################
# Install Package
###############################################################################

    async def install_package(
        self,
        package: str,
    ) -> int:
        """
        Install Python package.
        """

        return await self.execute_terminal(
            f"pip install {package}"
        )

###############################################################################
# Build Project
###############################################################################

    async def build_project(
        self,
    ) -> int:
        """
        Execute project build.
        """

        return await self.send_request(
            "workspace/build",
        )

###############################################################################
# Stream Output
###############################################################################

    async def stream_terminal_output(
        self,
    ) -> int:
        """
        Subscribe terminal output.
        """

        return await self.send_request(
            "terminal/stream",
        )

###############################################################################
# Kill Terminal
###############################################################################

    async def terminate_terminal(
        self,
    ) -> int:
        """
        Stop terminal process.
        """

        return await self.send_request(
            "terminal/terminate",
        )

###############################################################################
# AI Execute
###############################################################################

    async def ai_execute(
        self,
        command: str,
    ) -> int:
        """
        Execute AI generated command.
        """

        logger.info(
            "AI Execute: %s",
            command,
        )

        return await self.execute_terminal(
            command,
        )
###############################################################################
# Execute Terminal Command
###############################################################################

    async def execute_terminal(
        self,
        command: str,
        cwd: str | None = None,
    ) -> int:
        """
        Execute command inside VS Code terminal.
        """

        return await self.send_request(
            "terminal/execute",
            {
                "command": command,
                "cwd": cwd,
            },
        )

###############################################################################
# Run Python
###############################################################################

    async def run_python(
        self,
        script: str,
    ) -> int:
        """
        Run Python script.
        """

        return await self.execute_terminal(
            f'python "{script}"'
        )

###############################################################################
# Run Pytest
###############################################################################

    async def run_tests(
        self,
        target: str = "",
    ) -> int:
        """
        Execute pytest.
        """

        command = "pytest"

        if target:

            command += f" {target}"

        return await self.execute_terminal(
            command,
        )

###############################################################################
# Git Status
###############################################################################

    async def git_status(
        self,
    ) -> int:
        """
        Execute git status.
        """

        return await self.execute_terminal(
            "git status",
        )

###############################################################################
# Git Commit
###############################################################################

    async def git_commit(
        self,
        message: str,
    ) -> int:
        """
        Commit changes.
        """

        return await self.execute_terminal(
            f'git commit -m "{message}"'
        )

###############################################################################
# Install Package
###############################################################################

    async def install_package(
        self,
        package: str,
    ) -> int:
        """
        Install Python package.
        """

        return await self.execute_terminal(
            f"pip install {package}"
        )

###############################################################################
# Build Project
###############################################################################

    async def build_project(
        self,
    ) -> int:
        """
        Execute project build.
        """

        return await self.send_request(
            "workspace/build",
        )

###############################################################################
# Stream Output
###############################################################################

    async def stream_terminal_output(
        self,
    ) -> int:
        """
        Subscribe terminal output.
        """

        return await self.send_request(
            "terminal/stream",
        )

###############################################################################
# Kill Terminal
###############################################################################

    async def terminate_terminal(
        self,
    ) -> int:
        """
        Stop terminal process.
        """

        return await self.send_request(
            "terminal/terminate",
        )

###############################################################################
# AI Execute
###############################################################################

    async def ai_execute(
        self,
        command: str,
    ) -> int:
        """
        Execute AI generated command.
        """

        logger.info(
            "AI Execute: %s",
            command,
        )

        return await self.execute_terminal(
            command,
        )