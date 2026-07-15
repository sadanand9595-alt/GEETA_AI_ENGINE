"""
==============================================================================
GEETA AI Engine

File        : code_folding.py
Package     : editor
Description : Code Folding

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
# Fold Region
###############################################################################


@dataclass(slots=True)
class FoldRegion:
    """
    Represents a foldable region.
    """

    start_line: int

    end_line: int

    collapsed: bool = False

###############################################################################
# Code Folding
###############################################################################


class CodeFolding:
    """
    Code folding engine.

    Responsibilities

    - Fold regions
    - Collapse/Expand
    - Region lookup
    - Fold state
    """

    def __init__(
        self,
    ) -> None:

        self._regions: list[
            FoldRegion
        ] = []

        logger.info(
            "Code Folding initialized."
        )

###############################################################################
# Add Region
###############################################################################

    def add_region(
        self,
        start_line: int,
        end_line: int,
    ) -> None:
        """
        Register a fold region.
        """

        self._regions.append(
            FoldRegion(
                start_line=start_line,
                end_line=end_line,
            )
        )

###############################################################################
# Collapse
###############################################################################

    def collapse(
        self,
        index: int,
    ) -> bool:
        """
        Collapse a region.
        """

        if (
            index < 0
            or index >= len(
                self._regions
            )
        ):

            return False

        self._regions[
            index
        ].collapsed = True

        return True

###############################################################################
# Expand
###############################################################################

    def expand(
        self,
        index: int,
    ) -> bool:
        """
        Expand a region.
        """

        if (
            index < 0
            or index >= len(
                self._regions
            )
        ):

            return False

        self._regions[
            index
        ].collapsed = False

        return True

###############################################################################
# Toggle
###############################################################################

    def toggle(
        self,
        index: int,
    ) -> bool:
        """
        Toggle fold state.
        """

        if (
            index < 0
            or index >= len(
                self._regions
            )
        ):

            return False

        region = self._regions[index]

        region.collapsed = (
            not region.collapsed
        )

        return True
###############################################################################
# Remove Region
###############################################################################

    def remove_region(
        self,
        index: int,
    ) -> bool:
        """
        Remove a fold region.
        """

        if (
            index < 0
            or index >= len(
                self._regions
            )
        ):

            return False

        del self._regions[index]

        return True

###############################################################################
# Region Lookup
###############################################################################

    def regions(
        self,
    ) -> list[FoldRegion]:
        """
        Return all fold regions.
        """

        return list(
            self._regions
        )

    ###########################################################################

    def collapsed_regions(
        self,
    ) -> list[FoldRegion]:
        """
        Return collapsed fold regions.
        """

        return [
            region
            for region
            in self._regions
            if region.collapsed
        ]

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return folding statistics.
        """

        return {
            "regions": len(
                self._regions
            ),
            "collapsed": len(
                self.collapsed_regions()
            ),
            "expanded": (
                len(self._regions)
                - len(
                    self.collapsed_regions()
                )
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return code folding report.
        """

        return {
            "statistics": self.statistics(),
            "regions": [
                {
                    "start_line": region.start_line,
                    "end_line": region.end_line,
                    "collapsed": region.collapsed,
                }
                for region
                in self._regions
            ],
        }

###############################################################################
# Global Code Folding
###############################################################################

code_folding = CodeFolding()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "FoldRegion",
    "CodeFolding",
    "code_folding",
]