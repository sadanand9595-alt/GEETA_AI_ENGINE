"""
==============================================================================
GEETA AI ENGINE

File        : selection_engine.py
Package     : editor.core
Description : Selection Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from threading import RLock

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Selection
###############################################################################


@dataclass(slots=True)
class Selection:
    """
    Represents a text selection.
    """

    start_offset: int = 0

    end_offset: int = 0

    rectangular: bool = False

    ###########################################################################

    @property
    def empty(
        self,
    ) -> bool:
        """
        Return True if nothing is selected.
        """

        return self.start_offset == self.end_offset

    ###########################################################################

    @property
    def normalized(
        self,
    ) -> tuple[int, int]:
        """
        Return ordered selection range.
        """

        if self.start_offset <= self.end_offset:

            return (
                self.start_offset,
                self.end_offset,
            )

        return (
            self.end_offset,
            self.start_offset,
        )

###############################################################################
# Selection Engine
###############################################################################


class SelectionEngine:
    """
    Enterprise Selection Engine.

    Features
    --------
    • Multiple selections
    • Rectangular selection
    • AI selection support
    • Thread Safe
    """

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._lock = RLock()

        self._selections: list[
            Selection
        ] = [
            Selection(),
        ]

        logger.info(
            "Selection Engine initialized."
        )

###############################################################################
# Queries
###############################################################################

    @property
    def primary(
        self,
    ) -> Selection:
        """
        Return primary selection.
        """

        return self._selections[0]

    ###########################################################################

    @property
    def selections(
        self,
    ) -> list[Selection]:
        """
        Return all selections.
        """

        return self._selections.copy()

###############################################################################
# Management
###############################################################################

    def clear(
        self,
    ) -> None:
        """
        Clear all selections.
        """

        with self._lock:

            self._selections = [
                Selection(),
            ]

    ###########################################################################

    def add_selection(
        self,
        start: int,
        end: int,
        rectangular: bool = False,
    ) -> None:
        """
        Add a selection.
        """

        with self._lock:

            self._selections.append(
                Selection(
                    start_offset=start,
                    end_offset=end,
                    rectangular=rectangular,
                )
            )
            ###############################################################################
# Selection Management
###############################################################################

    def set_selection(
        self,
        start: int,
        end: int,
    ) -> None:
        """
        Replace the primary selection.
        """

        with self._lock:

            self.primary.start_offset = max(0, start)
            self.primary.end_offset = max(0, end)

    ###########################################################################

    def remove_selection(
        self,
        index: int,
    ) -> bool:
        """
        Remove a secondary selection.

        The primary selection (index 0) cannot be removed.
        """

        with self._lock:

            if index <= 0:

                return False

            if index >= len(self._selections):

                return False

            self._selections.pop(index)

            return True

###############################################################################
# Selection Operations
###############################################################################

    def extend_selection(
        self,
        offset: int,
    ) -> None:
        """
        Extend the primary selection.
        """

        with self._lock:

            self.primary.end_offset = max(
                0,
                offset,
            )

    ###########################################################################

    def collapse_selection(
        self,
    ) -> None:
        """
        Collapse the selection to its end.
        """

        with self._lock:

            self.primary.start_offset = (
                self.primary.end_offset
            )

    ###########################################################################

    def select_all(
        self,
        document_length: int,
    ) -> None:
        """
        Select the entire document.
        """

        with self._lock:

            self.primary.start_offset = 0

            self.primary.end_offset = max(
                0,
                document_length,
            )

###############################################################################
# Queries
###############################################################################

    def contains(
        self,
        offset: int,
    ) -> bool:
        """
        Return True if the primary selection
        contains the given offset.
        """

        start, end = self.primary.normalized

        return start <= offset < end

    ###########################################################################

    def selection_count(
        self,
    ) -> int:
        """
        Return number of selections.
        """

        return len(
            self._selections,
        )

###############################################################################
# Validation
###############################################################################

    def validate(
        self,
        document_length: int,
    ) -> None:
        """
        Clamp all selections to the document.
        """

        with self._lock:

            for selection in self._selections:

                selection.start_offset = min(
                    max(selection.start_offset, 0),
                    document_length,
                )

                selection.end_offset = min(
                    max(selection.end_offset, 0),
                    document_length,
                )
                ###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return selection statistics.
        """

        primary = self.primary

        start, end = primary.normalized

        return {
            "selection_count": len(
                self._selections,
            ),
            "selection_length": end - start,
            "start_offset": start,
            "end_offset": end,
        }

###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return Selection Engine diagnostics.
        """

        stats = self.statistics()

        return {
            **stats,
            "multi_selection": (
                len(self._selections) > 1
            ),
            "rectangular_selection": any(
                selection.rectangular
                for selection in self._selections
            ),
        }

###############################################################################
# Reset
###############################################################################

    def reset(
        self,
    ) -> None:
        """
        Reset Selection Engine.
        """

        self.clear()

        logger.info(
            "Selection Engine reset.",
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
            f"(count={stats['selection_count']}, "
            f"length={stats['selection_length']})"
        )

###############################################################################
# Global Instance
###############################################################################

selection_engine = SelectionEngine()

###############################################################################
# Helper Functions
###############################################################################

def current_selection(
) -> Selection:
    """
    Return the primary selection.
    """

    return selection_engine.primary


def clear_selection(
) -> None:
    """
    Clear the current selection.
    """

    selection_engine.clear()


###############################################################################
# Exports
###############################################################################

__all__ = [
    "Selection",
    "SelectionEngine",
    "selection_engine",
    "current_selection",
    "clear_selection",
]