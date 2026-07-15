"""
==============================================================================
GEETA AI Engine

File        : runtime_events.py
Package     : runtime
Description : Runtime Event System

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from time import time
from typing import Any, Callable

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Runtime Event
###############################################################################


@dataclass(slots=True)
class RuntimeEvent:
    """
    Runtime event.
    """

    event_type: str

    payload: dict[str, Any] = field(
        default_factory=dict,
    )

    timestamp: float = field(
        default_factory=time,
    )


###############################################################################
# Runtime Event Bus
###############################################################################


class RuntimeEventBus:
    """
    Publish / Subscribe runtime event bus.

    Responsibilities

    - Publish events
    - Subscribe handlers
    - Remove handlers
    - Broadcast runtime activity
    """

    def __init__(self) -> None:

        self._subscribers: dict[
            str,
            list[Callable[[RuntimeEvent], None]]
        ] = defaultdict(list)

        logger.info(
            "Runtime Event Bus initialized."
        )

    ###########################################################################

    def subscribe(
        self,
        event_type: str,
        callback: Callable[[RuntimeEvent], None],
    ) -> None:
        """
        Subscribe to an event.
        """

        self._subscribers[
            event_type
        ].append(callback)

    ###########################################################################

    def unsubscribe(
        self,
        event_type: str,
        callback: Callable[[RuntimeEvent], None],
    ) -> bool:
        """
        Remove an event subscriber.
        """

        handlers = self._subscribers.get(
            event_type,
        )

        if not handlers:

            return False

        if callback in handlers:

            handlers.remove(callback)

            return True

        return False

    ###########################################################################

    def publish(
        self,
        event_type: str,
        **payload: Any,
    ) -> None:
        """
        Publish an event.
        """

        event = RuntimeEvent(
            event_type=event_type,
            payload=payload,
        )

        logger.info(
            "Runtime event: %s",
            event_type,
        )

        for callback in self._subscribers.get(
            event_type,
            [],
        ):

            callback(
                event,
            )
###############################################################################
# Event Information
###############################################################################

    def event_types(
        self,
    ) -> list[str]:
        """
        Return registered event types.
        """

        return sorted(
            self._subscribers.keys()
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

        total_handlers = sum(
            len(handlers)
            for handlers
            in self._subscribers.values()
        )

        return {
            "event_types": len(
                self._subscribers
            ),
            "subscribers": total_handlers,
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return runtime event report.
        """

        return {
            "statistics": self.statistics(),
            "events": {
                event_type: len(handlers)
                for event_type, handlers
                in self._subscribers.items()
            },
        }

###############################################################################
# Global Runtime Event Bus
###############################################################################

runtime_events = RuntimeEventBus()

###############################################################################
# Common Runtime Events
###############################################################################

PROCESS_STARTED = "process.started"
PROCESS_FINISHED = "process.finished"
PROCESS_FAILED = "process.failed"

TERMINAL_OPENED = "terminal.opened"
TERMINAL_CLOSED = "terminal.closed"

DEBUG_STARTED = "debug.started"
DEBUG_STOPPED = "debug.stopped"

PROJECT_RUN = "project.run"
PROJECT_BUILD = "project.build"

###############################################################################
# Exports
###############################################################################

__all__ = [
    "RuntimeEvent",
    "RuntimeEventBus",
    "runtime_events",
    "PROCESS_STARTED",
    "PROCESS_FINISHED",
    "PROCESS_FAILED",
    "TERMINAL_OPENED",
    "TERMINAL_CLOSED",
    "DEBUG_STARTED",
    "DEBUG_STOPPED",
    "PROJECT_RUN",
    "PROJECT_BUILD",
]