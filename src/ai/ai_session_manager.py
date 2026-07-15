"""
==============================================================================
GEETA AI ENGINE Enterprise

File        : ai_session_manager.py
Module      : AI Core
Description : AI Session Manager

Author      : Sadanand Vishwakarma
Version     : 3.1.0
License     : MIT
==============================================================================
"""

from __future__ import annotations

###############################################################################
# Imports
###############################################################################

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from queue import Queue
from threading import RLock
from typing import Any

from config.logger import get_logger

logger = get_logger(__name__)

###############################################################################
# Session Models
###############################################################################


@dataclass(slots=True)
class CursorState:
    """
    Current cursor information.
    """

    line: int = 1
    column: int = 1


@dataclass(slots=True)
class SelectionState:
    """
    Current text selection.
    """

    start: int = 0
    end: int = 0
    text: str = ""


@dataclass(slots=True)
class EditorState:
    """
    Active editor state.
    """

    file_path: str | None = None
    language: str = "text"
    modified: bool = False

    cursor: CursorState = field(
        default_factory=CursorState,
    )

    selection: SelectionState = field(
        default_factory=SelectionState,
    )


@dataclass(slots=True)
class ProjectState:
    """
    Active project state.
    """

    root: Path | None = None
    opened_at: datetime | None = None

    recent_files: list[str] = field(
        default_factory=list,
    )

    opened_files: list[str] = field(
        default_factory=list,
    )


###############################################################################
# AI Session Manager
###############################################################################


class AISessionManager:
    """
    Enterprise AI Session Manager.

    Responsibilities
    ----------------

    • Project State
    • Workspace State
    • Editor Tracking
    • Context Cache
    • Task Queue
    • Provider Session
    • Token Accounting
    • Diagnostics
    """

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._lock = RLock()

        self._project = ProjectState()

        self._editor = EditorState()

        self._context: dict[str, Any] = {}

        self._history: list[str] = []

        self._tasks: Queue[Any] = Queue()

        self._provider: str = "none"

        self._token_usage: int = 0

        self._created = datetime.utcnow()

        logger.info(
            "AI Session Manager initialized.",
        )

    ###########################################################################

    @property
    def created_at(
        self,
    ) -> datetime:
        """
        Session creation timestamp.
        """

        return self._created
        ###############################################################################
# Session Lifecycle
###############################################################################

    def initialize(
        self,
    ) -> None:
        """
        Initialize AI session.
        """

        with self._lock:

            self._context.clear()

            self._history.clear()

            self._token_usage = 0

            while not self._tasks.empty():

                self._tasks.get_nowait()

            logger.info(
                "AI session initialized.",
            )

    ###########################################################################

    def shutdown(
        self,
    ) -> None:
        """
        Shutdown AI session.
        """

        with self._lock:

            self.close_project()

            self._context.clear()

            self._history.clear()

            logger.info(
                "AI session shutdown.",
            )

###############################################################################
# Project Management
###############################################################################

    def open_project(
        self,
        project_root: str | Path,
    ) -> None:
        """
        Open a project.
        """

        with self._lock:

            root = Path(project_root).resolve()

            self._project.root = root

            self._project.opened_at = datetime.utcnow()

            self._project.opened_files.clear()

            self._project.recent_files.clear()

            logger.info(
                "Project opened: %s",
                root,
            )

    ###########################################################################

    def close_project(
        self,
    ) -> None:
        """
        Close current project.
        """

        with self._lock:

            logger.info(
                "Project closed: %s",
                self._project.root,
            )

            self._project = ProjectState()

###############################################################################
# Current State
###############################################################################

    def current_project(
        self,
    ) -> Path | None:
        """
        Return current project root.
        """

        return self._project.root

    ###########################################################################

    def current_file(
        self,
    ) -> str | None:
        """
        Return current file.
        """

        return self._editor.file_path

    ###########################################################################

    def current_editor(
        self,
    ) -> EditorState:
        """
        Return editor state.
        """

        return self._editor

###############################################################################
# Editor Integration
###############################################################################

    def attach_editor(
        self,
        editor: Any,
    ) -> None:
        """
        Attach an editor instance.
        """

        with self._lock:

            self._context["editor"] = editor

            logger.info(
                "Editor attached.",
            )

    ###########################################################################

    def detach_editor(
        self,
    ) -> None:
        """
        Detach editor.
        """

        with self._lock:

            self._context.pop(
                "editor",
                None,
            )

            logger.info(
                "Editor detached.",
            )

###############################################################################
# File Tracking
###############################################################################

    def set_current_file(
        self,
        file_path: str | Path,
    ) -> None:
        """
        Update current active file.
        """

        with self._lock:

            path = str(
                Path(file_path),
            )

            self._editor.file_path = path

            if path not in self._project.opened_files:

                self._project.opened_files.append(
                    path,
                )

            if path not in self._project.recent_files:

                self._project.recent_files.insert(
                    0,
                    path,
                )

            logger.info(
                "Current file: %s",
                path,
            )
            ###############################################################################
# Context Management
###############################################################################

    def push_context(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store a context value.
        """

        with self._lock:

            self._context[key] = value

            logger.debug(
                "Context updated: %s",
                key,
            )

    ###########################################################################

    def context(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve context value.
        """

        return self._context.get(
            key,
            default,
        )

    ###########################################################################

    def clear_context(
        self,
    ) -> None:
        """
        Clear cached context.
        """

        with self._lock:

            self._context.clear()

            logger.info(
                "Context cache cleared.",
            )

    ###########################################################################

    def build_context(
        self,
    ) -> dict[str, Any]:
        """
        Build AI context snapshot.
        """

        return {

            "project": (
                str(self._project.root)
                if self._project.root
                else None
            ),

            "current_file": self._editor.file_path,

            "language": self._editor.language,

            "modified": self._editor.modified,

            "cursor": {

                "line": self._editor.cursor.line,

                "column": self._editor.cursor.column,

            },

            "selection": {

                "start": self._editor.selection.start,

                "end": self._editor.selection.end,

                "text": self._editor.selection.text,

            },

            "provider": self._provider,

            "token_usage": self._token_usage,

        }

###############################################################################
# Prompt History
###############################################################################

    def push_prompt(
        self,
        prompt: str,
    ) -> None:
        """
        Store prompt history.
        """

        with self._lock:

            self._history.append(
                prompt,
            )

    ###########################################################################

    def prompt_history(
        self,
    ) -> list[str]:
        """
        Return prompt history.
        """

        return list(
            self._history,
        )

###############################################################################
# Provider State
###############################################################################

    def set_provider(
        self,
        provider: str,
    ) -> None:
        """
        Set active AI provider.
        """

        with self._lock:

            self._provider = provider

    ###########################################################################

    def provider(
        self,
    ) -> str:
        """
        Return active provider.
        """

        return self._provider

###############################################################################
# Token Accounting
###############################################################################

    def add_tokens(
        self,
        amount: int,
    ) -> None:
        """
        Add token usage.
        """

        with self._lock:

            self._token_usage += max(
                amount,
                0,
            )

    ###########################################################################

    def token_usage(
        self,
    ) -> int:
        """
        Return accumulated token usage.
        """

        return self._token_usage

###############################################################################
# Task Queue
###############################################################################

    def enqueue_task(
        self,
        task: Any,
    ) -> None:
        """
        Queue a task.
        """

        self._tasks.put(
            task,
        )

    ###########################################################################

    def dequeue_task(
        self,
    ) -> Any | None:
        """
        Retrieve next task.
        """

        if self._tasks.empty():

            return None

        return self._tasks.get()
        ###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return session statistics.
        """

        with self._lock:

            return {

                "project": (
                    str(self._project.root)
                    if self._project.root
                    else None
                ),

                "opened_files": len(
                    self._project.opened_files,
                ),

                "recent_files": len(
                    self._project.recent_files,
                ),

                "prompt_history": len(
                    self._history,
                ),

                "queued_tasks": self._tasks.qsize(),

                "provider": self._provider,

                "token_usage": self._token_usage,

                "created_at": self._created.isoformat(),

            }

###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, Any]:
        """
        Return diagnostic information.
        """

        with self._lock:

            return {

                **self.statistics(),

                "context_entries": len(
                    self._context,
                ),

                "editor_attached": (
                    "editor" in self._context
                ),

                "active_file": (
                    self._editor.file_path
                ),

                "modified": (
                    self._editor.modified
                ),

            }

###############################################################################
# Serialization
###############################################################################

    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Export session state.
        """

        return {

            "statistics": self.statistics(),

            "context": dict(
                self._context,
            ),

            "history": list(
                self._history,
            ),

        }

###############################################################################
# Reset
###############################################################################

    def reset(
        self,
    ) -> None:
        """
        Reset AI session.
        """

        with self._lock:

            self.shutdown()

            self.initialize()

            logger.info(
                "AI session reset.",
            )

###############################################################################
# Representation
###############################################################################

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return (

            f"{self.__class__.__name__}("

            f"project={self._project.root}, "

            f"provider='{self._provider}', "

            f"tokens={self._token_usage})"

        )

###############################################################################
# Exports
###############################################################################

__all__ = [

    "CursorState",

    "SelectionState",

    "EditorState",

    "ProjectState",

    "AISessionManager",

]