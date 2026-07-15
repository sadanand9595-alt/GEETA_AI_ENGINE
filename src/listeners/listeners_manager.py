"""
==============================================================================
GEETA AI Engine

File        : listener_manager.py
Package     : listeners
Description : Central Listener Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from pathlib import Path

from config.logger import get_logger

from listeners.clipboard_listener import ClipboardListener
from listeners.file_listener import FileListener
from listeners.git_listener import GitListener
from listeners.python_traceback_listener import (
    PythonTracebackListener,
)
from listeners.terminal_listener import TerminalListener
from listeners.vscode_diagnostics_listener import (
    VSCodeDiagnosticsListener,
)

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Listener Manager
###############################################################################


class ListenerManager:
    """
    Central manager for all runtime listeners.

    Responsible for:

    • File Listener
    • Git Listener
    • Clipboard Listener
    • Terminal Listener
    • Python Traceback Listener
    • VSCode Diagnostics Listener
    """

    def __init__(
        self,
        workspace: Path,
    ) -> None:

        self.workspace = workspace

        self.file_listener = FileListener(
            workspace,
        )

        self.git_listener = GitListener(
            workspace,
        )

        self.clipboard_listener = ClipboardListener()

        self.traceback_listener = (
            PythonTracebackListener()
        )

        self.vscode_listener = (
            VSCodeDiagnosticsListener()
        )

        self.terminal_listener: (
            TerminalListener | None
        ) = None

        self._running = False

    ###########################################################################

    @property
    def running(self) -> bool:
        """
        Return manager state.
        """

        return self._running

    ###########################################################################

    def start(self) -> None:
        """
        Start all background listeners.
        """

        if self._running:
            return

        logger.info(
            "Starting Listener Manager..."
        )

        self.file_listener.start()

        self.git_listener.start()

        self.clipboard_listener.start()

        self._running = True

        logger.info(
            "Background listeners started."
        )

    ###########################################################################

    def attach_terminal(
        self,
        listener: TerminalListener,
    ) -> None:
        """
        Attach terminal listener.
        """

        self.terminal_listener = listener

        logger.info(
            "Terminal listener attached."
        )
###############################################################################
# Manager Control
###############################################################################

    def stop(self) -> None:
        """
        Stop all active listeners.
        """

        if not self._running:
            return

        logger.info(
            "Stopping Listener Manager..."
        )

        if self.terminal_listener is not None:

            self.terminal_listener.stop()

        self.clipboard_listener.stop()

        self.git_listener.stop()

        self.file_listener.stop()

        self._running = False

        logger.info(
            "All listeners stopped."
        )

    ###########################################################################

    def restart(self) -> None:
        """
        Restart all listeners.
        """

        logger.info(
            "Restarting Listener Manager..."
        )

        self.stop()

        self.start()

    ###########################################################################

    def status(self) -> dict[str, bool]:
        """
        Return current listener status.
        """

        return {
            "manager": self._running,
            "file_listener": self.file_listener.running,
            "git_listener": self.git_listener.running,
            "clipboard_listener": (
                self.clipboard_listener.running
            ),
            "terminal_listener": (
                self.terminal_listener.running
                if self.terminal_listener
                else False
            ),
        }


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


def create_listener_manager(
    workspace: Path,
) -> ListenerManager:
    """
    Create a listener manager.
    """

    return ListenerManager(workspace)


def start_listener_manager(
    workspace: Path,
) -> ListenerManager:
    """
    Create and start a listener manager.
    """

    manager = ListenerManager(workspace)

    manager.start()

    return manager


###############################################################################
# Exports
###############################################################################

__all__ = [
    "ListenerManager",
    "create_listener_manager",
    "start_listener_manager",
]