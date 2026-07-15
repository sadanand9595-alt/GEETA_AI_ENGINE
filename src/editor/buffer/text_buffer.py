"""
==============================================================================
GEETA AI ENGINE

File        : text_buffer.py
Package     : editor.buffer
Description : Text Buffer Abstraction

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from threading import RLock

from config.logger import get_logger
from editor.buffer.piece_table import PieceTable

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Text Buffer
###############################################################################


class TextBuffer:
    """
    High-level document buffer.

    Responsibilities
    ----------------
    • Buffer abstraction
    • PieceTable management
    • Thread safety
    • Public editing API

    The editor interacts only with TextBuffer.
    The underlying storage implementation
    remains hidden.
    """

    ###########################################################################

    def __init__(
        self,
        text: str = "",
    ) -> None:

        self._lock = RLock()

        self._piece_table = PieceTable(
            text,
        )

        logger.info(
            "Text Buffer initialized."
        )

###############################################################################
# Text
###############################################################################

    def text(
        self,
    ) -> str:
        """
        Return document text.
        """

        return self._piece_table.text()

###############################################################################
# Length
###############################################################################

    def length(
        self,
    ) -> int:
        """
        Return document length.
        """

        return self._piece_table.length()

###############################################################################
# Buffer Management
###############################################################################

    def clear(
        self,
    ) -> None:
        """
        Clear the document.
        """

        with self._lock:

            self._piece_table.clear()

###############################################################################
# Loading
###############################################################################

    def set_text(
        self,
        text: str,
    ) -> None:
        """
        Replace the document contents.
        """

        with self._lock:

            self._piece_table.set_text(
                text,
            )
            ###############################################################################
# Editing
###############################################################################

    def insert(
        self,
        offset: int,
        text: str,
    ) -> None:
        """
        Insert text into the document.
        """

        if not text:

            return

        with self._lock:

            self._piece_table.insert(
                offset,
                text,
            )

    ###########################################################################

    def delete(
        self,
        offset: int,
        length: int,
    ) -> None:
        """
        Delete a range of text.
        """

        if length <= 0:

            return

        with self._lock:

            self._piece_table.delete(
                offset,
                length,
            )

    ###########################################################################

    def replace(
        self,
        offset: int,
        length: int,
        text: str,
    ) -> None:
        """
        Replace a range of text.
        """

        with self._lock:

            self._piece_table.replace(
                offset,
                length,
                text,
            )

###############################################################################
# Convenience
###############################################################################

    def append(
        self,
        text: str,
    ) -> None:
        """
        Append text to the end of the document.
        """

        if not text:

            return

        self.insert(
            self.length(),
            text,
        )

###############################################################################
# Queries
###############################################################################

    def empty(
        self,
    ) -> bool:
        """
        Return True if the document is empty.
        """

        return self.length() == 0

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return buffer statistics.
        """

        stats = self._piece_table.statistics()

        return {
            "length": self.length(),
            "pieces": stats["pieces"],
            "original_buffer": stats["original_buffer"],
            "add_buffer": stats["add_buffer"],
        }

###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return buffer diagnostics.
        """

        return {
            **self.statistics(),
            "empty": self.empty(),
        }
        ###############################################################################
# Text Queries
###############################################################################

    def substring(
        self,
        start: int,
        end: int,
    ) -> str:
        """
        Return a substring.
        """

        text = self.text()

        start = max(0, start)
        end = max(start, end)

        return text[start:end]

    ###########################################################################

    def character_at(
        self,
        offset: int,
    ) -> str:
        """
        Return a single character.
        """

        text = self.text()

        if offset < 0:

            raise ValueError(
                "Negative offset."
            )

        if offset >= len(text):

            raise IndexError(
                "Offset out of range."
            )

        return text[offset]

###############################################################################
# Line Information
###############################################################################

    def line_count(
        self,
    ) -> int:
        """
        Return the number of lines.
        """

        text = self.text()

        if not text:

            return 1

        return text.count("\n") + 1

###############################################################################
# Reset
###############################################################################

    def reset(
        self,
    ) -> None:
        """
        Reset the buffer.
        """

        with self._lock:

            self.clear()

        logger.info(
            "Text Buffer reset."
        )

###############################################################################
# Representation
###############################################################################

    def __repr__(
        self,
    ) -> str:
        """
        Developer-friendly representation.
        """

        stats = self.statistics()

        return (
            f"{self.__class__.__name__}"
            f"(length={stats['length']}, "
            f"pieces={stats['pieces']})"
        )

###############################################################################
# Global Buffer
###############################################################################

text_buffer = TextBuffer()

###############################################################################
# Helper Functions
###############################################################################

def current_text(
) -> str:
    """
    Return the current document text.
    """

    return text_buffer.text()


def