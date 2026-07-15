"""
==============================================================================
GEETA AI Engine

File        : editor_document.py
Package     : editor
Description : Editor Document

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Editor Document
###############################################################################


class EditorDocument:
    """
    Represents a single editor document.

    Responsibilities

    - File loading
    - File saving
    - Text management
    - Dirty tracking
    - Encoding management
    - Metadata
    """

    def __init__(
        self,
        file_path: str | Path,
        encoding: str = "utf-8",
    ) -> None:

        self._path = Path(
            file_path
        ).resolve()

        self._encoding = encoding

        self._text = ""

        self._dirty = False

        self._readonly = False

        logger.info(
            "Editor Document created: %s",
            self._path,
        )

###############################################################################
# Load
###############################################################################

    def load(
        self,
    ) -> None:
        """
        Load document contents.
        """

        self._text = self._path.read_text(
            encoding=self._encoding,
        )

        self._dirty = False

###############################################################################
# Save
###############################################################################

    def save(
        self,
    ) -> None:
        """
        Save document.
        """

        if self._readonly:

            raise PermissionError(
                "Document is read-only."
            )

        self._path.write_text(
            self._text,
            encoding=self._encoding,
        )

        self._dirty = False

###############################################################################
# Text
###############################################################################

    @property
    def text(
        self,
    ) -> str:
        """
        Return document text.
        """

        return self._text

    ###########################################################################

    @text.setter
    def text(
        self,
        value: str,
    ) -> None:
        """
        Update document text.
        """

        self._text = value

        self._dirty = True

###############################################################################
# Path
###############################################################################

    @property
    def path(
        self,
    ) -> Path:
        """
        Return document path.
        """

        return self._path
###############################################################################
# Read-Only
###############################################################################

    @property
    def readonly(
        self,
    ) -> bool:
        """
        Return read-only state.
        """

        return self._readonly

    ###########################################################################

    @readonly.setter
    def readonly(
        self,
        value: bool,
    ) -> None:
        """
        Set read-only state.
        """

        self._readonly = value

###############################################################################
# Dirty State
###############################################################################

    @property
    def dirty(
        self,
    ) -> bool:
        """
        Return dirty state.
        """

        return self._dirty

###############################################################################
# Encoding
###############################################################################

    @property
    def encoding(
        self,
    ) -> str:
        """
        Return document encoding.
        """

        return self._encoding

###############################################################################
# Metadata
###############################################################################

    def metadata(
        self,
    ) -> dict[str, Any]:
        """
        Return document metadata.
        """

        return {
            "path": str(self._path),
            "name": self._path.name,
            "suffix": self._path.suffix,
            "encoding": self._encoding,
            "readonly": self._readonly,
            "dirty": self._dirty,
            "exists": self._path.exists(),
            "size": (
                self._path.stat().st_size
                if self._path.exists()
                else 0
            ),
        }

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return document statistics.
        """

        return {
            "characters": len(
                self._text
            ),
            "lines": len(
                self._text.splitlines()
            ),
            "words": len(
                self._text.split()
            ),
            "dirty": self._dirty,
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return complete document report.
        """

        return {
            "metadata": self.metadata(),
            "statistics": self.statistics(),
        }

###############################################################################
# Exports
###############################################################################

__all__ = [
    "EditorDocument",
]