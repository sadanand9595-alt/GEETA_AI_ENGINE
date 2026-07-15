"""
==============================================================================
GEETA AI Engine

File        : auto_complete_popup.py
Package     : editor
Description : Auto Complete Popup

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Completion Entry
###############################################################################


@dataclass(slots=True)
class CompletionEntry:
    """
    Completion popup item.
    """

    label: str

    kind: str

    detail: str = ""

    documentation: str = ""

###############################################################################
# Auto Complete Popup
###############################################################################


class AutoCompletePopup:
    """
    IntelliSense popup.

    Responsibilities

    - Completion popup
    - Keyboard navigation
    - Ranking
    - Incremental filtering
    - Documentation preview
    """

    def __init__(
        self,
    ) -> None:

        self._items: list[
            CompletionEntry
        ] = []

        self._selected = 0

        self._visible = False

        logger.info(
            "Auto Complete Popup initialized."
        )

###############################################################################
# Show / Hide
###############################################################################

    def show(
        self,
        items: list[CompletionEntry],
    ) -> None:
        """
        Display completion popup.
        """

        self._items = list(
            items,
        )

        self._selected = 0

        self._visible = True

    ###########################################################################

    def hide(
        self,
    ) -> None:
        """
        Hide popup.
        """

        self._visible = False

###############################################################################
# Navigation
###############################################################################

    def next(
        self,
    ) -> None:
        """
        Select next item.
        """

        if not self._items:

            return

        self._selected = (
            self._selected + 1
        ) % len(
            self._items
        )

    ###########################################################################

    def previous(
        self,
    ) -> None:
        """
        Select previous item.
        """

        if not self._items:

            return

        self._selected = (
            self._selected - 1
        ) % len(
            self._items
        )

###############################################################################
# Current Item
###############################################################################

    def current(
        self,
    ) -> CompletionEntry | None:
        """
        Return selected completion.
        """

        if (
            not self._visible
            or not self._items
        ):

            return None

        return self._items[
            self._selected
        ]
###############################################################################
# Filter
###############################################################################

    def filter(
        self,
        prefix: str,
    ) -> list[CompletionEntry]:
        """
        Filter completion entries.
        """

        query = prefix.lower()

        return [
            item
            for item
            in self._items
            if query in item.label.lower()
        ]

###############################################################################
# Accept
###############################################################################

    def accept(
        self,
    ) -> CompletionEntry | None:
        """
        Accept the selected completion.
        """

        item = self.current()

        self.hide()

        return item

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return popup statistics.
        """

        return {
            "visible": self._visible,
            "items": len(
                self._items
            ),
            "selected_index": (
                self._selected
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return popup report.
        """

        return {
            "statistics": (
                self.statistics()
            ),
            "current": (
                self.current().label
                if self.current()
                else None
            ),
            "items": [
                item.label
                for item
                in self._items
            ],
        }

###############################################################################
# Global Auto Complete Popup
###############################################################################

auto_complete_popup = AutoCompletePopup()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "CompletionEntry",
    "AutoCompletePopup",
    "auto_complete_popup",
]