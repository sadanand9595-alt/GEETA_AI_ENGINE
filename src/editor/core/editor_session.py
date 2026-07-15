"""
==============================================================================
GEETA AI ENGINE

File        : editor_session.py
Package     : editor.core
Description : Editor Session

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from threading import RLock

from config.logger import get_logger

from editor.buffer.text_buffer import TextBuffer
from editor.core.command_bus import CommandBus
from editor.core.cursor_engine import CursorEngine
from editor.core.document_engine import DocumentEngine
from editor.core.selection_engine import SelectionEngine
from editor.core.undo_engine import UndoEngine

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Editor Session
###############################################################################


class EditorSession:
    """
    Represents one editing session.

    One open editor tab = one EditorSession.

    Owns all editing state required by a document.
    """

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._lock = RLock()

        #######################################################################
        # Core Components
        #######################################################################

        self.text_buffer = TextBuffer()

        self.document = DocumentEngine()

        self.undo_engine = UndoEngine()

        self.command_bus = CommandBus(
            undo_engine=self.undo_engine,
        )

        self.cursor = CursorEngine()

        self.selection = SelectionEngine()

        #######################################################################
        # Wiring
        #######################################################################

        self.document.attach_buffer(
            self.text_buffer,
        )

        logger.info(
            "Editor Session initialized."
        )

###############################################################################
# File Operations
###############################################################################

    def open(
        self,
        filename: str,
    ) -> None:
        """
        Open a file.
        """

        self.document.open_file(
            filename,
        )

    ###########################################################################

    def save(
        self,
    ) -> None:
        """
        Save current file.
        """

        self.document.save()

    ###########################################################################

    def save_as(
        self,
        filename: str,
    ) -> None:
        """
        Save file as.
        """

        self.document.save_as(
            filename,
        )
        ###############################################################################
# Document Operations
###############################################################################

    def new_document(
        self,
    ) -> None:
        """
        Create a new document.
        """

        with self._lock:

            self.document.new_document()

            self.cursor.reset()

            self.selection.reset()

            self.undo_engine.reset()

            logger.info(
                "New document created."
            )

    ###########################################################################

    def reload(
        self,
    ) -> None:
        """
        Reload current document.
        """

        with self._lock:

            self.document.reload()

            self.cursor.reset()

            self.selection.reset()

            logger.info(
                "Document reloaded."
            )

###############################################################################
# Session Reset
###############################################################################

    def reset(
        self,
    ) -> None:
        """
        Reset the complete editor session.
        """

        with self._lock:

            self.document.reset()

            self.text_buffer.reset()

            self.cursor.reset()

            self.selection.reset()

            self.undo_engine.reset()

            logger.info(
                "Editor session reset."
            )

###############################################################################
# Session Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, object]:
        """
        Return session statistics.
        """

        return {
            "document": self.document.statistics(),
            "buffer": self.text_buffer.statistics(),
            "cursor": self.cursor.statistics(),
            "selection": self.selection.statistics(),
            "undo": self.undo_engine.statistics(),
        }

###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return complete session diagnostics.
        """

        return {
            "document": self.document.diagnostics(),
            "buffer": self.text_buffer.diagnostics(),
            "cursor": self.cursor.diagnostics(),
            "selection": self.selection.diagnostics(),
            "undo": self.undo_engine.diagnostics(),
            "command_bus": self.command_bus.diagnostics(),
        }

###############################################################################
# Metadata
###############################################################################

    def metadata(
        self,
    ) -> dict[str, object]:
        """
        Return session metadata.
        """

        return {
            "filename": self.document.filename(),
            "modified": self.document.modified,
            "encoding": self.document.encoding,
        }
        ###############################################################################
# Session Lifecycle
###############################################################################

    def close(
        self,
    ) -> None:
        """
        Close the editor session.

        The document is not destroyed. This method performs
        session-level cleanup only.
        """

        with self._lock:

            if self.document.modified:

                logger.warning(
                    "Closing modified session: %s",
                    self.document.filename(),
                )

            logger.info(
                "Editor session closed."
            )

###############################################################################
# Resource Cleanup
###############################################################################

    def dispose(
        self,
    ) -> None:
        """
        Release all session resources.

        Safe to call multiple times.
        """

        with self._lock:

            try:

                self.command_bus.reset()

                self.undo_engine.reset()

                self.selection.reset()

                self.cursor.reset()

                self.document.reset()

                self.text_buffer.reset()

            finally:

                logger.info(
                    "Editor session disposed."
                )

###############################################################################
# Queries
###############################################################################

    @property
    def modified(
        self,
    ) -> bool:
        """
        Return True if the document has unsaved changes.
        """

        return self.document.modified

    ###########################################################################

    @property
    def filename(
        self,
    ) -> str:
        """
        Return the current filename.
        """

        return self.document.filename()

###############################################################################
# Representation
###############################################################################

    def __repr__(
        self,
    ) -> str:
        """
        Developer-friendly representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"file='{self.filename}', "
            f"modified={self.modified})"
        )

###############################################################################
# Exports
###############################################################################

__all__ = [
    "EditorSession",
]