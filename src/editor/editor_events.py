"""
==============================================================================
GEETA AI Engine

File        : editor_events.py
Package     : editor
Description : Editor Event System

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Event
###############################################################################


@dataclass(slots=True)
class EditorEvent:
    """
    Represents an editor event.
    """

    name: str

    source: str

    payload: dict[str, Any] = field(
        default_factory=dict,
    )

###############################################################################
# Editor Event Bus
###############################################################################


class EditorEvents:
    """
    Editor event manager.

    Responsibilities

    - Publish events
    - Subscribe listeners
    - Unsubscribe listeners
    - Dispatch notifications
    """

    def __init__(
        self,
    ) -> None:

        self._listeners: dict[
            str,
            list[Callable[[EditorEvent], None]]
        ] = defaultdict(
            list,
        )

        logger.info(
            "Editor Events initialized."
        )

###############################################################################
# Subscribe
###############################################################################

    def subscribe(
        self,
        event_name: str,
        callback: Callable[
            [EditorEvent],
            None,
        ],
    ) -> None:
        """
        Register an event listener.
        """

        self._listeners[
            event_name
        ].append(
            callback,
        )

###############################################################################
# Unsubscribe
###############################################################################

    def unsubscribe(
        self,
        event_name: str,
        callback: Callable[
            [EditorEvent],
            None,
        ],
    ) -> bool:
        """
        Remove an event listener.
        """

        listeners = self._listeners.get(
            event_name,
        )

        if (
            not listeners
            or callback not in listeners
        ):

            return False

        listeners.remove(
            callback,
        )

        return True

###############################################################################
# Publish
###############################################################################

    def publish(
        self,
        event: EditorEvent,
    ) -> None:
        """
        Publish an editor event.
        """

        listeners = self._listeners.get(
            event.name,
            [],
        )

        for callback in listeners:

            try:

                callback(
                    event,
                )

            except Exception:

                logger.exception(
                    "Editor event failed: %s",
                    event.name,
                )
###############################################################################
# Clear
###############################################################################

    def clear(
        self,
        event_name: str | None = None,
    ) -> None:
        """
        Clear listeners.
        """

        if event_name is None:

            self._listeners.clear()

            return

        self._listeners.pop(
            event_name,
            None,
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return event bus statistics.
        """

        return {
            "event_types": len(
                self._listeners
            ),
            "listeners": sum(
                len(callbacks)
                for callbacks
                in self._listeners.values()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return event manager report.
        """

        return {
            "statistics": self.statistics(),
            "events": {
                event_name: len(
                    callbacks
                )
                for event_name, callbacks
                in self._listeners.items()
            },
        }

###############################################################################
# Global Editor Events
###############################################################################

editor_events = EditorEvents()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "EditorEvent",
    "EditorEvents",
    "editor_events",
]