"""
==============================================================================
GEETA AI Engine

File        : selection_manager.py
Package     : editor
Description : Selection Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

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

    start_line: int = 0

    start_column: int = 0

    end_line: int = 0

    end_column: int = 0

###############################################################################
# Selection Manager
###############################################################################


class SelectionManager:
    """
    Selection management.

    Responsibilities

    - Single selection
    - Multi-selection
    - Expand selection
    - Clear selection
    - Clipboard support
    """

    def __init__(
        self,
    ) -> None:

        self._selections: list[
            Selection
        ] = []

        logger.info(
            "Selection Manager initialized."
        )

###############################################################################
# Add Selection
###############################################################################

    def add(
        self,
        start_line: int,
        start_column: int,
        end_line: int,
        end_column: int,
    ) -> None:
        """
        Add a text selection.
        """

        self._selections.append(
            Selection(
                start_line=max(
                    0,
                    start_line,
                ),
                start_column=max(
                    0,
                    start_column,
                ),
                end_line=max(
                    0,
                    end_line,
                ),
                end_column=max(
                    0,
                    end_column,
                ),
            )
        )

###############################################################################
# Clear
###############################################################################

    def clear(
        self,
    ) -> None:
        """
        Remove all selections.
        """

        self._selections.clear()

###############################################################################
# Primary Selection
###############################################################################

    @property
    def primary(
        self,
    ) -> Selection | None:
        """
        Return primary selection.
        """

        if not self._selections:

            return None

        return self._selections[0]

###############################################################################
# Selection State
###############################################################################

    def has_selection(
        self,
    ) -> bool:
        """
        Return whether any selection exists.
        """

        return bool(
            self._selections
        )

###############################################################################
# Selection Count
###############################################################################

    def count(
        self,
    ) -> int:
        """
        Return selection count.
        """

        return len(
            self._selections
        )
###############################################################################
# Remove Selection
###############################################################################

    def remove(
        self,
        index: int,
    ) -> bool:
        """
        Remove a selection.
        """

        if (
            index < 0
            or index >= len(
                self._selections
            )
        ):

            return False

        del self._selections[index]

        return True

###############################################################################
# Enumerate
###############################################################################

    def selections(
        self,
    ) -> list[Selection]:
        """
        Return all selections.
        """

        return list(
            self._selections
        )

###############################################################################
# Normalize
###############################################################################

    def normalize(
        self,
    ) -> None:
        """
        Normalize all selections.
        """

        for selection in self._selections:

            if (
                selection.start_line
                > selection.end_line
            ):

                (
                    selection.start_line,
                    selection.end_line,
                ) = (
                    selection.end_line,
                    selection.start_line,
                )

            if (
                selection.start_column
                > selection.end_column
                and selection.start_line
                == selection.end_line
            ):

                (
                    selection.start_column,
                    selection.end_column,
                ) = (
                    selection.end_column,
                    selection.start_column,
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

        return {
            "selection_count": len(
                self._selections
            ),
            "has_selection": int(
                self.has_selection()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return selection report.
        """

        return {
            "statistics": self.statistics(),
            "selections": [
                {
                    "start_line": s.start_line,
                    "start_column": s.start_column,
                    "end_line": s.end_line,
                    "end_column": s.end_column,
                }
                for s in self._selections
            ],
        }

###############################################################################
# Global Selection Manager
###############################################################################

selection_manager = SelectionManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "Selection",
    "SelectionManager",
    "selection_manager",
]