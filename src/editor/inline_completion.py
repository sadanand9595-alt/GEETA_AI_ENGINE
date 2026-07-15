"""
==============================================================================
GEETA AI Engine

File        : inline_completion.py
Package     : editor
Description : AI Inline Completion

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
# Inline Suggestion
###############################################################################


@dataclass(slots=True)
class InlineSuggestion:
    """
    Represents an inline AI suggestion.
    """

    text: str

    provider: str

    confidence: float = 1.0

###############################################################################
# Inline Completion
###############################################################################


class InlineCompletion:
    """
    AI inline completion engine.

    Responsibilities

    - Ghost text
    - Suggestion management
    - Accept/Dismiss
    - Provider abstraction
    - AI integration
    """

    def __init__(
        self,
    ) -> None:

        self._suggestion: (
            InlineSuggestion | None
        ) = None

        logger.info(
            "Inline Completion initialized."
        )

###############################################################################
# Suggestion
###############################################################################

    def set(
        self,
        text: str,
        provider: str,
        confidence: float = 1.0,
    ) -> None:
        """
        Set current suggestion.
        """

        self._suggestion = InlineSuggestion(
            text=text,
            provider=provider,
            confidence=confidence,
        )

###############################################################################
# Current Suggestion
###############################################################################

    @property
    def suggestion(
        self,
    ) -> InlineSuggestion | None:
        """
        Return current suggestion.
        """

        return self._suggestion

###############################################################################
# Accept
###############################################################################

    def accept(
        self,
    ) -> str:
        """
        Accept current suggestion.
        """

        if self._suggestion is None:

            return ""

        text = self._suggestion.text

        self._suggestion = None

        return text

###############################################################################
# Dismiss
###############################################################################

    def dismiss(
        self,
    ) -> None:
        """
        Dismiss current suggestion.
        """

        self._suggestion = None
###############################################################################
# Partial Acceptance
###############################################################################

    def accept_word(
        self,
    ) -> str:
        """
        Accept the first word of the suggestion.
        """

        if self._suggestion is None:

            return ""

        words = self._suggestion.text.split(
            maxsplit=1,
        )

        accepted = words[0]

        remaining = (
            words[1]
            if len(words) > 1
            else ""
        )

        if remaining:

            self._suggestion.text = remaining

        else:

            self._suggestion = None

        return accepted

    ###########################################################################

    def accept_line(
        self,
    ) -> str:
        """
        Accept the first line of the suggestion.
        """

        if self._suggestion is None:

            return ""

        lines = self._suggestion.text.splitlines()

        if not lines:

            self._suggestion = None

            return ""

        accepted = lines[0]

        remaining = "\n".join(
            lines[1:]
        )

        if remaining:

            self._suggestion.text = remaining

        else:

            self._suggestion = None

        return accepted

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return inline completion statistics.
        """

        return {
            "has_suggestion": (
                self._suggestion is not None
            ),
            "provider": (
                self._suggestion.provider
                if self._suggestion
                else None
            ),
            "confidence": (
                self._suggestion.confidence
                if self._suggestion
                else 0.0
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return inline completion report.
        """

        return {
            "statistics": self.statistics(),
            "suggestion": (
                self._suggestion.text
                if self._suggestion
                else None
            ),
        }

###############################################################################
# Global Inline Completion
###############################################################################

inline_completion = InlineCompletion()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "InlineSuggestion",
    "InlineCompletion",
    "inline_completion",
]