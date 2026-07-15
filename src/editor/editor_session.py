"""
==============================================================================
GEETA AI Engine

File        : editor_session.py
Package     : editor
Description : Editor Session Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Session Document
###############################################################################


@dataclass(slots=True)
class SessionDocument:
    """
    Represents an opened document.
    """

    file_path: str

    cursor_line: int = 0

    cursor_column: int = 0

    scroll_line: int = 0

    folded_lines: list[int] = field(
        default_factory=list,
    )

###############################################################################
# Editor Session
###############################################################################


class EditorSession:
    """
    Editor session manager.

    Responsibilities

    - Open documents
    - Cursor restoration
    - Scroll restoration
    - Fold restoration
    - Session persistence
    """

    def __init__(
        self,
    ) -> None:

        self._documents: dict[
            str,
            SessionDocument,
        ] = {}

        self._workspace: str | None = None

        logger.info(
            "Editor Session initialized."
        )

###############################################################################
# Workspace
###############################################################################

    def set_workspace(
        self,
        workspace: str | Path,
    ) -> None:
        """
        Set current workspace.
        """

        self._workspace = str(
            Path(workspace).resolve()
        )

###############################################################################
# Documents
###############################################################################

    def open_document(
        self,
        document: SessionDocument,
    ) -> None:
        """
        Register an opened document.
        """

        self._documents[
            document.file_path
        ] = document

    ###########################################################################

    def close_document(
        self,
        file_path: str,
    ) -> bool:
        """
        Close a document.
        """

        if file_path not in self._documents:

            return False

        del self._documents[
            file_path
        ]

        return True

###############################################################################
# Lookup
###############################################################################

    def document(
        self,
        file_path: str,
    ) -> SessionDocument | None:
        """
        Return a session document.
        """

        return self._documents.get(
            file_path,
        )

###############################################################################
# Open Documents
###############################################################################

    def documents(
        self,
    ) -> list[SessionDocument]:
        """
        Return all open documents.
        """

        return list(
            self._documents.values()
        )
###############################################################################
# Session Serialization
###############################################################################

    def serialize(
        self,
    ) -> dict[str, Any]:
        """
        Serialize editor session.
        """

        return {
            "workspace": self._workspace,
            "documents": [
                {
                    "file_path": document.file_path,
                    "cursor_line": document.cursor_line,
                    "cursor_column": document.cursor_column,
                    "scroll_line": document.scroll_line,
                    "folded_lines": list(
                        document.folded_lines
                    ),
                }
                for document
                in self._documents.values()
            ],
        }

###############################################################################
# Restore
###############################################################################

    def restore(
        self,
        data: dict[str, Any],
    ) -> None:
        """
        Restore a serialized session.
        """

        self._workspace = data.get(
            "workspace",
        )

        self._documents.clear()

        for item in data.get(
            "documents",
            [],
        ):

            document = SessionDocument(
                file_path=item["file_path"],
                cursor_line=item.get(
                    "cursor_line",
                    0,
                ),
                cursor_column=item.get(
                    "cursor_column",
                    0,
                ),
                scroll_line=item.get(
                    "scroll_line",
                    0,
                ),
                folded_lines=item.get(
                    "folded_lines",
                    [],
                ),
            )

            self.open_document(
                document,
            )

###############################################################################
# Recent Files
###############################################################################

    def recent_files(
        self,
    ) -> list[str]:
        """
        Return recently opened files.
        """

        return list(
            self._documents.keys()
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return session statistics.
        """

        return {
            "workspace": self._workspace,
            "open_documents": len(
                self._documents
            ),
            "recent_files": len(
                self.recent_files()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return editor session report.
        """

        return {
            "statistics": self.statistics(),
            "documents": [
                document.file_path
                for document
                in self.documents()
            ],
        }

###############################################################################
# Global Editor Session
###############################################################################

editor_session = EditorSession()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "SessionDocument",
    "EditorSession",
    "editor_session",
]