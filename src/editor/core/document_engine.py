"""
==============================================================================
GEETA AI ENGINE

File        : document_engine.py
Package     : editor.core
Description : Document Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from pathlib import Path
from threading import RLock
from typing import Callable

from config.logger import get_logger

logger = get_logger(__name__)


class DocumentEngine:
    """
    Central document manager.

    Responsibilities
    ----------------
    * Document lifecycle
    * File loading
    * File saving
    * Change tracking
    * Event notifications

    The actual text storage is delegated to the
    text buffer implementation (Piece Table).
    """

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._lock = RLock()

        self._path: Path | None = None

        self._encoding = "utf-8"

        self._modified = False

        self._listeners: list[
            Callable[[], None]
        ] = []

        self._buffer = None

        logger.info(
            "Document Engine initialized."
        )

    ###########################################################################
    # Properties
    ###########################################################################

    @property
    def path(
        self,
    ) -> Path | None:

        return self._path

    ###########################################################################

    @property
    def modified(
        self,
    ) -> bool:

        return self._modified

    ###########################################################################

    @property
    def encoding(
        self,
    ) -> str:

        return self._encoding

    ###########################################################################
    # Listener Management
    ###########################################################################

    def add_listener(
        self,
        callback: Callable[[], None],
    ) -> None:

        if callback not in self._listeners:

            self._listeners.append(
                callback,
            )

    ###########################################################################

    def remove_listener(
        self,
        callback: Callable[[], None],
    ) -> None:

        if callback in self._listeners:

            self._listeners.remove(
                callback,
            )

    ###########################################################################

    def _notify(
        self,
    ) -> None:

        for callback in self._listeners:

            try:

                callback()

            except Exception:

                logger.exception(
                    "Document listener failed."
                )

    ###########################################################################
    # Buffer
    ###########################################################################

    def attach_buffer(
        self,
        buffer,
    ) -> None:
        """
        Attach Piece Table / Text Buffer.
        """

        self._buffer = buffer
        ###############################################################################
# Document Management
###############################################################################

    def new_document(
        self,
    ) -> None:
        """
        Create a new empty document.
        """

        with self._lock:

            self._path = None

            self._modified = False

            if self._buffer is not None:

                self._buffer.clear()

            self._notify()

            logger.info(
                "New document created.",
            )

###############################################################################
# File Loading
###############################################################################

    def open_file(
        self,
        path: str | Path,
    ) -> None:
        """
        Open a document from disk.
        """

        file_path = Path(path)

        text = file_path.read_text(
            encoding=self._encoding,
        )

        with self._lock:

            self._path = file_path.resolve()

            if self._buffer is None:

                raise RuntimeError(
                    "No text buffer attached."
                )

            self._buffer.set_text(
                text,
            )

            self._modified = False

            self._notify()

        logger.info(
            "Opened document: %s",
            self._path,
        )

###############################################################################
# Save
###############################################################################

    def save(
        self,
    ) -> None:
        """
        Save current document.
        """

        if self._path is None:

            raise RuntimeError(
                "Document has no file path."
            )

        if self._buffer is None:

            raise RuntimeError(
                "No text buffer attached."
            )

        self._path.write_text(
            self._buffer.text(),
            encoding=self._encoding,
        )

        self._modified = False

        self._notify()

        logger.info(
            "Saved document: %s",
            self._path,
        )

###############################################################################
# Save As
###############################################################################

    def save_as(
        self,
        path: str | Path,
    ) -> None:
        """
        Save document to another path.
        """

        self._path = Path(path).resolve()

        self.save()

###############################################################################
# Reload
###############################################################################

    def reload(
        self,
    ) -> None:
        """
        Reload document from disk.
        """

        if self._path is None:

            return

        self.open_file(
            self._path,
        )

###############################################################################
# Modified State
###############################################################################

    def set_modified(
        self,
        modified: bool = True,
    ) -> None:
        """
        Update modification state.
        """

        self._modified = modified

        self._notify()
        ###############################################################################
# Queries
###############################################################################

    def exists(
        self,
    ) -> bool:
        """
        Return True if the document has a valid file path.
        """

        return self._path is not None

    ###########################################################################

    def filename(
        self,
    ) -> str:
        """
        Return document filename.
        """

        if self._path is None:

            return "Untitled"

        return self._path.name

    ###########################################################################

    def directory(
        self,
    ) -> Path | None:
        """
        Return parent directory.
        """

        if self._path is None:

            return None

        return self._path.parent

###############################################################################
# Metadata
###############################################################################

    def metadata(
        self,
    ) -> dict[str, object]:
        """
        Return document metadata.
        """

        return {
            "filename": self.filename(),
            "path": (
                str(self._path)
                if self._path
                else None
            ),
            "encoding": self._encoding,
            "modified": self._modified,
        }

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return document statistics.
        """

        if self._buffer is None:

            return {
                "characters": 0,
                "lines": 0,
            }

        text = self._buffer.text()

        return {
            "characters": len(text),
            "lines": text.count("\n") + 1 if text else 0,
        }

###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return document diagnostics.
        """

        return {
            **self.metadata(),
            **self.statistics(),
            "buffer_attached": (
                self._buffer is not None
            ),
            "listener_count": len(
                self._listeners,
            ),
        }

###############################################################################
# Reset
###############################################################################

    def reset(
        self,
    ) -> None:
        """
        Reset document engine.
        """

        with self._lock:

            self._path = None

            self._modified = False

            self._listeners.clear()

            self._buffer = None

        logger.info(
            "Document Engine reset.",
        )

###############################################################################
# Representation
###############################################################################

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(file='{self.filename()}', "
            f"modified={self.modified})"
        )

###############################################################################
# Exports
###############################################################################

__all__ = [
    "DocumentEngine",
]