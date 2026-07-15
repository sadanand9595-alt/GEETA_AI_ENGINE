"""
==============================================================================
GEETA AI IDE

File        : session_manager.py
Package     : ai
Description : Enterprise AI Session Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Session Status
###############################################################################


class SessionStatus(str, Enum):

    CREATED = "created"

    ACTIVE = "active"

    PAUSED = "paused"

    CLOSED = "closed"

###############################################################################
# Session Checkpoint
###############################################################################


@dataclass(slots=True)
class SessionCheckpoint:
    """
    Workspace snapshot.
    """

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    description: str = ""

    current_file: str = ""

    cursor_line: int = 0

    cursor_column: int = 0

###############################################################################
# AI Session
###############################################################################


@dataclass(slots=True)
class AISession:
    """
    Persistent AI Session.
    """

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    name: str = ""

    project: str = ""

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    status: SessionStatus = (
        SessionStatus.CREATED
    )

    checkpoints: list[
        SessionCheckpoint
    ] = field(
        default_factory=list,
    )

    history: list[str] = field(
        default_factory=list,
    )

###############################################################################
# Session Manager
###############################################################################


class SessionManager:
    """
    Enterprise AI Session Manager.

    Responsibilities

    - Persistent sessions
    - Conversation history
    - Workspace snapshots
    - Checkpoints
    - Resume sessions
    - Crash recovery
    """

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._sessions: dict[
            str,
            AISession
        ] = {}

        logger.info(
            "AI Session Manager initialized."
        )

###############################################################################
# Create Session
###############################################################################

    def create(
        self,
        name: str,
        project: str,
    ) -> AISession:
        """
        Create session.
        """

        session = AISession(
            name=name,
            project=project,
        )

        self._sessions[
            session.id
        ] = session

        return session

###############################################################################
# Lookup
###############################################################################

    def session(
        self,
        session_id: str,
    ) -> AISession | None:
        """
        Return session.
        """

        return self._sessions.get(
            session_id
        )

###############################################################################
# Activate
###############################################################################

    def activate(
        self,
        session: AISession,
    ) -> None:
        """
        Activate session.
        """

        session.status = (
            SessionStatus.ACTIVE
        )

        logger.info(
            "Session activated: %s",
            session.name,
        )
###############################################################################
# Pause Session
###############################################################################

    def pause(
        self,
        session: AISession,
    ) -> None:
        """
        Pause session.
        """

        session.status = (
            SessionStatus.PAUSED
        )

        logger.info(
            "Session paused: %s",
            session.name,
        )

###############################################################################
# Resume Session
###############################################################################

    def resume(
        self,
        session: AISession,
    ) -> None:
        """
        Resume session.
        """

        session.status = (
            SessionStatus.ACTIVE
        )

        logger.info(
            "Session resumed: %s",
            session.name,
        )

###############################################################################
# Close Session
###############################################################################

    def close(
        self,
        session: AISession,
    ) -> None:
        """
        Close session.
        """

        session.status = (
            SessionStatus.CLOSED
        )

        logger.info(
            "Session closed: %s",
            session.name,
        )

###############################################################################
# Create Checkpoint
###############################################################################

    def checkpoint(
        self,
        session: AISession,
        description: str,
        current_file: str,
        line: int,
        column: int,
    ) -> SessionCheckpoint:
        """
        Create workspace checkpoint.
        """

        checkpoint = SessionCheckpoint(
            description=description,
            current_file=current_file,
            cursor_line=line,
            cursor_column=column,
        )

        session.checkpoints.append(
            checkpoint,
        )

        return checkpoint

###############################################################################
# Restore Checkpoint
###############################################################################

    def restore(
        self,
        session: AISession,
        checkpoint_id: str,
    ) -> SessionCheckpoint | None:
        """
        Restore checkpoint.
        """

        for checkpoint in session.checkpoints:

            if checkpoint.id == checkpoint_id:

                return checkpoint

        return None

###############################################################################
# History
###############################################################################

    def add_history(
        self,
        session: AISession,
        entry: str,
    ) -> None:
        """
        Add history entry.
        """

        session.history.append(
            entry,
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return session statistics.
        """

        active = sum(
            1
            for session
            in self._sessions.values()
            if session.status
            == SessionStatus.ACTIVE
        )

        paused = sum(
            1
            for session
            in self._sessions.values()
            if session.status
            == SessionStatus.PAUSED
        )

        closed = sum(
            1
            for session
            in self._sessions.values()
            if session.status
            == SessionStatus.CLOSED
        )

        return {
            "sessions": len(
                self._sessions
            ),
            "active": active,
            "paused": paused,
            "closed": closed,
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return session manager report.
        """

        return {
            "statistics": self.statistics(),
            "sessions": [
                {
                    "id": session.id,
                    "name": session.name,
                    "project": session.project,
                    "status": session.status.value,
                    "checkpoints": len(
                        session.checkpoints
                    ),
                    "history": len(
                        session.history
                    ),
                }
                for session
                in self._sessions.values()
            ],
        }

###############################################################################
# Global Session Manager
###############################################################################

session_manager: (
    SessionManager | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "SessionStatus",
    "SessionCheckpoint",
    "AISession",
    "SessionManager",
    "session_manager",
]