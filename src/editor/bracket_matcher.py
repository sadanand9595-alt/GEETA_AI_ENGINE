"""
==============================================================================
GEETA AI Engine

File        : bracket_matcher.py
Package     : editor
Description : Bracket Matcher

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
# Bracket Pair
###############################################################################


@dataclass(slots=True)
class BracketPair:
    """
    Represents a matching bracket pair.
    """

    opening: int

    closing: int

    character: str

###############################################################################
# Bracket Matcher
###############################################################################


class BracketMatcher:
    """
    Bracket matching engine.

    Responsibilities

    - Match brackets
    - Detect unmatched brackets
    - Pair highlighting
    - Scope detection
    """

    BRACKETS = {
        "(": ")",
        "[": "]",
        "{": "}",
    }

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        logger.info(
            "Bracket Matcher initialized."
        )

###############################################################################
# Match Brackets
###############################################################################

    def match(
        self,
        text: str,
    ) -> list[BracketPair]:
        """
        Return all bracket pairs.
        """

        pairs: list[
            BracketPair
        ] = []

        stack: list[
            tuple[str, int]
        ] = []

        for index, char in enumerate(
            text,
        ):

            if char in self.BRACKETS:

                stack.append(
                    (
                        char,
                        index,
                    )
                )

                continue

            for opening, closing in self.BRACKETS.items():

                if char != closing:

                    continue

                if not stack:

                    break

                last, position = stack.pop()

                if last == opening:

                    pairs.append(
                        BracketPair(
                            opening=position,
                            closing=index,
                            character=opening,
                        )
                    )

                break

        return pairs

###############################################################################
# Find Matching Pair
###############################################################################

    def find_pair(
        self,
        text: str,
        position: int,
    ) -> BracketPair | None:
        """
        Return bracket pair at position.
        """

        for pair in self.match(
            text,
        ):

            if (
                pair.opening == position
                or pair.closing == position
            ):

                return pair

        return None
###############################################################################
# Unmatched Brackets
###############################################################################

    def unmatched(
        self,
        text: str,
    ) -> list[int]:
        """
        Return positions of unmatched brackets.
        """

        unmatched: list[int] = []

        stack: list[
            tuple[str, int]
        ] = []

        for index, char in enumerate(text):

            if char in self.BRACKETS:

                stack.append(
                    (char, index)
                )

                continue

            if char in self.BRACKETS.values():

                if not stack:

                    unmatched.append(
                        index
                    )

                    continue

                opening, position = stack.pop()

                if self.BRACKETS[
                    opening
                ] != char:

                    unmatched.extend(
                        (
                            position,
                            index,
                        )
                    )

        unmatched.extend(
            position
            for _, position
            in stack
        )

        return sorted(
            unmatched
        )

###############################################################################
# Auto Close
###############################################################################

    def auto_close(
        self,
        character: str,
    ) -> str:
        """
        Return closing bracket.
        """

        return self.BRACKETS.get(
            character,
            "",
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
        text: str,
    ) -> dict[str, int]:
        """
        Return matcher statistics.
        """

        return {
            "pairs": len(
                self.match(
                    text,
                )
            ),
            "unmatched": len(
                self.unmatched(
                    text,
                )
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
        text: str,
    ) -> dict[str, object]:
        """
        Return matcher report.
        """

        return {
            "statistics": self.statistics(
                text,
            ),
            "pairs": [
                {
                    "opening": pair.opening,
                    "closing": pair.closing,
                    "character": pair.character,
                }
                for pair
                in self.match(text)
            ],
            "unmatched": self.unmatched(
                text,
            ),
        }

###############################################################################
# Global Bracket Matcher
###############################################################################

bracket_matcher = BracketMatcher()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "BracketPair",
    "BracketMatcher",
    "bracket_matcher",
]