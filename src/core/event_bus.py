"""Backward-compatible imports for the active core event bus.

The runnable application imports :mod:`core.event_bus`. Keeping this module as
an explicit re-export prevents the legacy ``src.core`` namespace from drifting
into a second event-bus implementation.
"""

from core.event_bus import (
    Event,
    EventBus,
    EventCallback,
    event_bus,
    publish,
    subscribe,
    unsubscribe,
)

__all__ = [
    "Event",
    "EventBus",
    "EventCallback",
    "event_bus",
    "publish",
    "subscribe",
    "unsubscribe",
]
