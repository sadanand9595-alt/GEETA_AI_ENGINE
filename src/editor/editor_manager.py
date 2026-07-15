"""
==============================================================================
GEETA AI Engine

File        : editor_manager.py
Package     : editor
Description : Editor Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.editor.code_editor import CodeEditor

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Editor Manager
###############################################################################


class EditorManager:
    """
    Central editor manager.

    Responsibilities

    - Open documents
    - Close documents
    - Track active editor
    - Dirty state management
    - Editor session management
    """

    def __init__(
        self,
    ) -> None:

        self._documents: dict[
            str,
            dict[str, Any],
        ] = {}

        self._active: str | None = None

        logger.info(
            "Editor Manager initialized."
        )

###############################################################################
# Open
###############################################################################

    def open(
        self,
        file_path: str | Path,
    ) -> dict[str, Any]:
        """
        Open a document.
        """

        path = Path(file_path).resolve()

        document = {
            "path": str(path),
            "dirty": False,
            "opened": True,
        }

        self._documents[
            str(path)
        ] = document

        self._active = str(path)

        logger.info(
            "Opened document: %s",
            path,
        )

        return document

###############################################################################
# Close
###############################################################################

    def close(
        self,
        file_path: str | Path,
    ) -> bool:
        """
        Close a document.
        """

        path = str(
            Path(file_path).resolve()
        )

        if path not in self._documents:

            return False

        del self._documents[path]

        if self._active == path:

            self._active = (
                next(
                    iter(self._documents),
                    None,
                )
            )

        logger.info(
            "Closed document: %s",
            path,
        )

        return True

###############################################################################
# Active Editor
###############################################################################

    def active_document(
        self,
    ) -> dict[str, Any] | None:
        """
        Return active document.
        """

        if self._active is None:

            return None

        return self._documents.get(
            self._active,
        )

###############################################################################
# Activate
###############################################################################

    def activate(
        self,
        file_path: str | Path,
    ) -> bool:
        """
        Activate an opened document.
        """

        path = str(
            Path(file_path).resolve()
        )

        if path not in self._documents:

            return False

        self._active = path

        logger.info(
            "Activated document: %s",
            path,
        )

        return True
###############################################################################
# Dirty State
###############################################################################

    def set_dirty(
        self,
        file_path: str | Path,
        dirty: bool = True,
    ) -> bool:
        """
        Set document dirty state.
        """

        path = str(
            Path(file_path).resolve()
        )

        document = self._documents.get(
            path,
        )

        if document is None:

            return False

        document["dirty"] = dirty

        return True

###############################################################################
# Documents
###############################################################################

    def documents(
        self,
    ) -> list[dict[str, Any]]:
        """
        Return all opened documents.
        """

        return list(
            self._documents.values()
        )

###############################################################################
# Session
###############################################################################

    def save_session(
        self,
    ) -> dict[str, Any]:
        """
        Save editor session.
        """

        return {
            "active": self._active,
            "documents": self.documents(),
        }

    ###########################################################################

    def restore_session(
        self,
        session: dict[str, Any],
    ) -> None:
        """
        Restore editor session.
        """

        self._documents.clear()

        for document in session.get(
            "documents",
            [],
        ):

            self._documents[
                document["path"]
            ] = document

        self._active = session.get(
            "active",
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return editor statistics.
        """

        dirty = sum(
            document["dirty"]
            for document
            in self._documents.values()
        )

        return {
            "open_documents": len(
                self._documents
            ),
            "dirty_documents": dirty,
            "active_document": (
                self._active
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return editor report.
        """

        return {
            "