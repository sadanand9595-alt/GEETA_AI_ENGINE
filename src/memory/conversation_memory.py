"""
==============================================================================
GEETA AI Engine

File        : conversation_memory.py
Package     : memory
Description : Conversation Memory

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Any

from config.logger import get_logger
from memory.base_memory import BaseMemory

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Conversation Memory
###############################################################################


class ConversationMemory(BaseMemory):
    """
    Stores conversation history for GEETA AI.

    Responsibilities:

    - User messages
    - Assistant responses
    - Conversation history
    - Context retrieval
    - Session continuity
    """

    def __init__(self) -> None:

        super().__init__(
            name="conversation_memory",
        )

        self._messages: list[
            dict[str, Any]
        ] = []

    ###########################################################################

    def store(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store conversation item.
        """

        self._messages.append(
            {
                "key": key,
                "value": value,
            }
        )

    ###########################################################################

    def retrieve(
        self,
        key: str,
    ) -> Any:
        """
        Retrieve conversation item.
        """

        for item in reversed(
            self._messages
        ):

            if item["key"] == key:

                return item["value"]

        return None

    ###########################################################################

    def delete(
        self,
        key: str,
    ) -> None:
        """
        Delete conversation item.
        """

        self._messages = [
            item
            for item in self._messages
            if item["key"] != key
        ]

    ###########################################################################

    def clear(self) -> None:
        """
        Clear conversation history.
        """

        self._messages.clear()

        logger.info(
            "Conversation memory cleared."
        )

    ###########################################################################

    def messages(
        self,
    ) -> list[dict[str, Any]]:
        """
        Return all stored messages.
        """

        return list(
            self._messages
        )
###############################################################################
# Conversation Utilities
###############################################################################

    def recent(
        self,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Return the most recent conversation items.
        """

        if limit <= 0:
            return []

        return self._messages[-limit:]

    ###########################################################################

    def summarize(self) -> str:
        """
        Return a simple conversation summary.

        Override with AI-based summarization if required.
        """

        return (
            f"{len(self._messages)} message(s) "
            f"stored in conversation memory."
        )

    ###########################################################################

    def estimated_tokens(self) -> int:
        """
        Estimate token usage.

        Uses a simple approximation of
        four characters per token.
        """

        total_characters = sum(
            len(str(item["value"]))
            for item in self._messages
        )

        return total_characters // 4

###############################################################################
# Statistics
###############################################################################

    def statistics(self) -> dict[str, Any]:
        """
        Return conversation memory statistics.
        """

        data = super().statistics()

        data.update(
            {
                "messages": len(self._messages),
                "estimated_tokens": (
                    self.estimated_tokens()
                ),
            }
        )

        return data

###############################################################################
# Exports
###############################################################################

__all__ = [
    "ConversationMemory",
]