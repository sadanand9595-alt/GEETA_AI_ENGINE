"""
==============================================================================
GEETA AI Engine

File        : context_optimizer.py
Package     : ai
Description : Intelligent Context Optimizer

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Context Item
###############################################################################


@dataclass(slots=True)
class ContextItem:
    """
    Single context item.
    """

    name: str

    content: str

    priority: int = 100

    source: str = ""

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

###############################################################################
# Context Optimizer
###############################################################################


class ContextOptimizer:
    """
    Optimizes project context before
    sending it to the AI provider.
    """

    def __init__(self) -> None:

        logger.info(
            "Context Optimizer initialized."
        )

    ###########################################################################

    def optimize(
        self,
        items: list[ContextItem],
        max_length: int = 120000,
    ) -> list[ContextItem]:
        """
        Optimize context.
        """

        ordered = sorted(
            items,
            key=lambda item: item.priority,
        )

        result: list[ContextItem] = []

        current = 0

        for item in ordered:

            length = len(
                item.content,
            )

            if current + length > max_length:

                break

            result.append(
                item,
            )

            current += length

        logger.info(
            "Optimized %d → %d context items.",
            len(items),
            len(result),
        )

        return result
        ###############################################################################
# Duplicate Removal
###############################################################################

    def remove_duplicates(
        self,
        items: list[ContextItem],
    ) -> list[ContextItem]:
        """
        Remove duplicate context items.
        """

        seen: set[tuple[str, str]] = set()

        unique: list[ContextItem] = []

        for item in items:

            key = (
                item.name,
                item.content,
            )

            if key in seen:

                continue

            seen.add(
                key,
            )

            unique.append(
                item,
            )

        logger.info(
            "Removed %d duplicate context items.",
            len(items) - len(unique),
        )

        return unique

###############################################################################
# Priority Adjustment
###############################################################################

    def prioritize_active_file(
        self,
        items: list[ContextItem],
        active_file: str,
    ) -> None:
        """
        Boost priority for the active file.
        """

        for item in items:

            if item.name == active_file:

                item.priority = 0

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
        items: list[ContextItem],
    ) -> dict[str, int]:
        """
        Return optimizer statistics.
        """

        return {
            "items": len(items),
            "characters": sum(
                len(item.content)
                for item in items
            ),
        }

###############################################################################
# Prompt Conversion
###############################################################################

    def build_context(
        self,
        items: list[ContextItem],
    ) -> str:
        """
        Build optimized context text.
        """

        parts: list[str] = []

        for item in items:

            parts.append(
                f"# {item.name}\n"
                f"{item.content}"
            )

        return "\n\n".join(
            parts,
        )
        ###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
        items: list[ContextItem],
    ) -> dict[str, Any]:
        """
        Return optimizer diagnostics.
        """

        stats = self.statistics(items)

        return {
            **stats,
            "duplicates_removed": (
                len(items)
                - len(
                    self.remove_duplicates(items)
                )
            ),
        }

###############################################################################
# Future Hooks
###############################################################################

    def semantic_rank(
        self,
        items: list[ContextItem],
        query: str,
    ) -> list[ContextItem]:
        """
        Semantic ranking hook.

        Currently returns priority ordering.
        Future versions will integrate the
        Embedding Engine and RAG Engine.
        """

        logger.debug(
            "Semantic ranking requested for: %s",
            query,
        )

        return sorted(
            items,
            key=lambda item: item.priority,
        )

###############################################################################
# Global Optimizer
###############################################################################

context_optimizer = ContextOptimizer()

###############################################################################
# Helper Functions
###############################################################################


def optimize_context(
    items: list[ContextItem],
    max_length: int = 120000,
) -> list[ContextItem]:
    """
    Optimize context items.
    """

    return context_optimizer.optimize(
        items,
        max_length=max_length,
    )


def build_context(
    items: list[ContextItem],
) -> str:
    """
    Build optimized context string.
    """

    return context_optimizer.build_context(
        items,
    )


def context_statistics(
    items: list[ContextItem],
) -> dict[str, int]:
    """
    Return context statistics.
    """

    return context_optimizer.statistics(
        items,
    )

###############################################################################
# Exports
###############################################################################

__all__ = [
    "ContextItem",
    "ContextOptimizer",
    "context_optimizer",
    "optimize_context",
    "build_context",
    "context_statistics",
]