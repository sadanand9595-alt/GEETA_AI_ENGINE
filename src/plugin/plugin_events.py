"""
==============================================================================
GEETA AI Engine

File        : plugin_events.py
Package     : plugins
Description : Plugin Event Bus

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
# Plugin Event
###############################################################################


@dataclass(slots=True)
class PluginEvent:
    """
    Plugin event.
    """

    event_type: str

    payload: dict[str, Any] = field(
        default_factory=dict,
    )

    timestamp: float = field(
        default_factory=time,
    )

###############################################################################
# Plugin Event Bus
###############################################################################


class PluginEventBus:
    """
    Publish/Subscribe event bus
    for the Plugin System.

    Responsibilities

    - Publish events
    - Subscribe handlers
    - Remove handlers
    - Broadcast plugin activity
    """

    def __init__(self) -> None:

        self._subscribers: dict[
            str,
            list[
                Callable[
                    [PluginEvent],
                    None,
                ]
            ],
        ] = defaultdict(list)

        logger.info(
            "Plugin Event Bus initialized."
        )

    ###########################################################################

    def subscribe(
        self,
        event_type: str,
        callback: Callable[
            [PluginEvent],
            None,
        ],
    ) -> None:
        """
        Subscribe to an event.
        """

        self._subscribers[
            event_type
        ].append(
            callback,
        )

    ###########################################################################

    def unsubscribe(
        self,
        event_type: str,
        callback: Callable[
            [PluginEvent],
            None,
        ],
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

            handlers.remove(
                callback,
            )

            return True

        return False

    ###########################################################################

    def publish(
        self,
        event_type: str,
        **payload: Any,
    ) -> None:
        """
        Publish a plugin event.
        """

        event = PluginEvent(
            event_type=event_type,
            payload=payload,
        )

        logger.info(
            "Plugin event: %s",
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
# Event Types
###############################################################################

    def event_types(
        self,
    ) -> list[str]:
        """
        Return registered plugin event types.
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
        Return plugin event statistics.
        """

        subscriber_count = sum(
            len(callbacks)
            for callbacks
            in self._subscribers.values()
        )

        return {
            "event_types": len(
                self._subscribers
            ),
            "subscribers": subscriber_count,
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return plugin event report.
        """

        return {
            "statistics": self.statistics(),
            "events": {
                event: len(callbacks)
                for event, callbacks
                in self._subscribers.items()
            },
        }

###############################################################################
# Global Plugin Event Bus
###############################################################################

plugin_events = PluginEventBus()

###############################################################################
# Standard Plugin Events
###############################################################################

PLUGIN_DISCOVERED = "plugin.discovered"
PLUGIN_REGISTERED = "plugin.registered"
PLUGIN_UNREGISTERED = "plugin.unregistered"

PLUGIN_LOADED = "plugin.loaded"
PLUGIN_UNLOADED = "plugin.unloaded"
PLUGIN_RELOADED = "plugin.reloaded"

PLUGIN_ENABLED = "plugin.enabled"
PLUGIN_DISABLED = "plugin.disabled"

PLUGIN_INITIALIZED = "plugin.initialized"
PLUGIN_SHUTDOWN = "plugin.shutdown"

SERVICE_REGISTERED = "plugin.service.registered"
COMMAND_REGISTERED = "plugin.command.registered"

###############################################################################
# Exports
###############################################################################

__all__ = [
    "PluginEvent",
    "PluginEventBus",
    "plugin_events",
    "PLUGIN_DISCOVERED",
    "PLUGIN_REGISTERED",
    "PLUGIN_UNREGISTERED",
    "PLUGIN_LOADED",
    "PLUGIN_UNLOADED",
    "PLUGIN_RELOADED",
    "PLUGIN_ENABLED",
    "PLUGIN_DISABLED",
    "PLUGIN_INITIALIZED",
    "PLUGIN_SHUTDOWN",
    "SERVICE_REGISTERED",
    "COMMAND_REGISTERED",
]