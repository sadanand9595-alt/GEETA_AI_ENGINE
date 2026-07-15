"""
==============================================================================
GEETA AI ENGINE

File        : piece_table.py
Package     : editor.buffer
Description : Piece Table Implementation

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from threading import RLock

from config.logger import get_logger

from editor.buffer.piece import (
    BufferType,
    Piece,
)

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Piece Table
###############################################################################


class PieceTable:
    """
    Enterprise Piece Table implementation.

    Features
    --------
    • O(1) append buffer
    • Efficient insert/delete
    • Unlimited undo support
    • Large file friendly
    """

    ###########################################################################

    def __init__(
        self,
        text: str = "",
    ) -> None:

        self._lock = RLock()

        self._original = text

        self._add = ""

        self._pieces: list[Piece] = []

        if text:

            self._pieces.append(
                Piece(
                    buffer=BufferType.ORIGINAL,
                    start=0,
                    length=len(text),
                )
            )

        logger.info(
            "PieceTable initialized."
        )

###############################################################################
# Properties
###############################################################################

    @property
    def original_buffer(
        self,
    ) -> str:

        return self._original

    ###########################################################################

    @property
    def add_buffer(
        self,
    ) -> str:

        return self._add

    ###########################################################################

    @property
    def piece_count(
        self,
    ) -> int:

        return len(
            self._pieces,
        )

###############################################################################
# Buffer Operations
###############################################################################

    def clear(
        self,
    ) -> None:
        """
        Reset table.
        """

        with self._lock:

            self._original = ""

            self._add = ""

            self._pieces.clear()

###############################################################################
# Text Loading
###############################################################################

    def set_text(
        self,
        text: str,
    ) -> None:
        """
        Replace document.
        """

        with self._lock:

            self.clear()

            self._original = text

            if text:

                self._pieces.append(
                    Piece(
                        buffer=BufferType.ORIGINAL,
                        start=0,
                        length=len(text),
                    )
                )
                ###############################################################################
# Text Export
###############################################################################

    def text(
        self,
    ) -> str:
        """
        Return complete document text.
        """

        with self._lock:

            chunks: list[str] = []

            for piece in self._pieces:

                source = (
                    self._original
                    if piece.buffer is BufferType.ORIGINAL
                    else self._add
                )

                chunks.append(
                    source[
                        piece.start:
                        piece.end
                    ]
                )

            return "".join(chunks)

###############################################################################
# Queries
###############################################################################

    def length(
        self,
    ) -> int:
        """
        Return document length.
        """

        return sum(
            piece.length
            for piece in self._pieces
        )

###############################################################################
# Offset Resolution
###############################################################################

    def _find_piece(
        self,
        offset: int,
    ) -> tuple[int, int]:
        """
        Locate the piece containing the
        document offset.

        Returns:
            (piece_index, local_offset)
        """

        if offset < 0:

            raise ValueError(
                "Negative offset."
            )

        current = 0

        for index, piece in enumerate(
            self._pieces
        ):

            end = current + piece.length

            if offset <= end:

                return (
                    index,
                    offset - current,
                )

            current = end

        return (
            len(self._pieces),
            0,
        )

###############################################################################
# Insert
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

            if offset < 0 or offset > self.length():

                raise ValueError(
                    "Offset out of range."
                )

            add_start = len(
                self._add
            )

            self._add += text

            new_piece = Piece(
                buffer=BufferType.ADD,
                start=add_start,
                length=len(text),
            )

            if not self._pieces:

                self._pieces.append(
                    new_piece,
                )

                return

            piece_index, local = (
                self._find_piece(
                    offset,
                )
            )
            target = self._pieces[piece_index]

            left = None
            right = None

            if local > 0:

                left = Piece(
                    buffer=target.buffer,
                    start=target.start,
                    length=local,
                )

            if local < target.length:

                right = Piece(
                    buffer=target.buffer,
                    start=target.start + local,
                    length=target.length - local,
                )

            replacement: list[Piece] = []

            if left is not None:
                replacement.append(left)

            replacement.append(new_piece)

            if right is not None:
                replacement.append(right)

            self._pieces[
                piece_index:piece_index + 1
            ] = replacement

###############################################################################
# Delete
###############################################################################

    def delete(
        self,
        offset: int,
        length: int,
    ) -> None:
        """
        Delete a text range.

        NOTE:
        Initial implementation.
        Full multi-piece delete optimization
        will be added together with UndoEngine.
        """

        if length <= 0:

            return

        text = self.text()

        updated = (
            text[:offset]
            + text[offset + length:]
        )

        self.set_text(
            updated,
        )

###############################################################################
# Replace
###############################################################################

    def replace(
        self,
        offset: int,
        length: int,
        text: str,
    ) -> None:
        """
        Replace a range.
        """

        self.delete(
            offset,
            length,
        )

        self.insert(
            offset,
            text,
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return Piece Table statistics.
        """

        return {
            "pieces": len(
                self._pieces,
            ),
            "characters": self.length(),
            "original_buffer": len(
                self._original,
            ),
            "add_buffer": len(
                self._add,
            ),
        }

###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return diagnostics.
        """

        return {
            **self.statistics(),
            "empty": (
                self.length() == 0
            ),
        }

###############################################################################
# Representation
###############################################################################

    def __repr__(
        self,
    ) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(pieces={len(self._pieces)}, "
            f"length={self.length()})"
        )

###############################################################################
# Exports
###############################################################################

__all__ = [
    "PieceTable",
]