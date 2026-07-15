"""
==============================================================================
GEETA AI Engine

File        : debug_manager.py
Package     : runtime
Description : Debug Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import uuid
from typing import Any

from config.logger import get_logger
from runtime.debug_session import (
    DebugSession,
)

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Debug Manager
###############################################################################


class DebugManager:
    """
    Central debug session manager.

    Responsibilities

    - Session lifecycle
    - Multiple debug sessions
    - Breakpoint synchronization
    - Watch management
    - Session lookup
    - Debug adapter integration
    """

    def __init__(self) -> None:

        self._sessions: dict[
            str,
            DebugSession,
        ] = {}

        logger.info(
            "Debug Manager initialized."
        )

    ###########################################################################

    def create_session(
        self,
    ) -> DebugSession:
        """
        Create a new debug session.
        """

        session = DebugSession(
            session_id=str(
                uuid.uuid4(),
            ),
        )

        self._sessions[
            session.session_id
        ] = session

        logger.info(
            "Created debug session: %s",
            session.session_id,
        )

        return session

    ###########################################################################

    def session(
        self,
        session_id: str,
    ) -> DebugSession:
        """
        Return a debug session.
        """

        return self._sessions[
            session_id
        ]

    ###########################################################################

    def exists(
        self,
        session_id: str,
    ) -> bool:
        """
        Check session existence.
        """

        return (
            session_id
            in self._sessions
        )

    ###########################################################################

    def remove_session(
        self,
        session_id: str,
    ) -> bool:
        """
        Remove a debug session.
        """

        if session_id not in self._sessions:

            return False

        del self._sessions[
            session_id
        ]

        logger.info(
            "Removed debug session: %s",
            session_id,
        )

        return True

    ###########################################################################

    def start(
        self,
        session_id: str,
    ) -> None:
        """
        Start a debug session.
        """

        self.session(
            session_id,
        ).start()
###############################################################################
# Session Control
###############################################################################

    def pause(
        self,
        session_id: str,
    ) -> None:
        """
        Pause a debug session.
        """

        self.session(
            session_id,
        ).pause()

    ###########################################################################

    def resume(
        self,
        session_id: str,
    ) -> None:
        """
        Resume a debug session.
        """

        self.session(
            session_id,
        ).resume()

    ###########################################################################

    def stop(
        self,
        session_id: str,
    ) -> None:
        """
        Stop a debug session.
        """

        self.session(
            session_id,
        ).stop()

###############################################################################
# Breakpoint Synchronization
###############################################################################

    def synchronize_breakpoints(
        self,
    ) -> dict[str, int]:
        """
        Return breakpoint counts for all sessions.
        """

        return {
            session_id: len(
                session.breakpoints
            )
            for session_id, session
            in self._sessions.items()
        }

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return debug manager statistics.
        """

        running = sum(
            session.state.value == "running"
            for session in self._sessions.values()
        )

        paused = sum(
            session.state.value == "paused"
            for session in self._sessions.values()
        )

        return {
            "sessions": len(
                self._sessions
            ),
            "running": running,
            "paused": paused,
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return debug manager report.
        """

        return {
            "statistics": self.statistics(),
            "breakpoints": (
                self.synchronize_breakpoints()
            ),
            "sessions": [
                session.report()
                for session
                in self._sessions.values()
            ],
        }

###############################################################################
# Global Debug Manager
###############################################################################

debug_manager = DebugManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "DebugManager",
    "debug_manager",
]