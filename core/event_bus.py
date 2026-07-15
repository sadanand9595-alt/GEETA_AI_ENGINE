"""Thread-safe synchronous event dispatch for application infrastructure."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
import logging
from threading import RLock
from typing import Any


logger = logging.getLogger(__name__)

EventCallback = Callable[["Event"], None]


@dataclass(frozen=True, slots=True)
class Event:
    """An event published by an :class:`EventBus`.

    ``data`` deliberately remains a dictionary for compatibility with existing
    listener code. Subscribers should treat it as read-only.
    """

    name: str
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


class EventBus:
    """A thread-safe, in-process, synchronous publish/subscribe event bus.

    Subscribers execute on the publishing thread. A failing subscriber is
    logged and does not prevent the remaining subscribers from receiving the
    event. Long-running work belongs in a worker owned by the subscriber.
    """

    def __init__(self) -> None:
        self._lock = RLock()
        self._subscribers: dict[str, list[EventCallback]] = defaultdict(list)
        logger.info("Event bus initialized")

    def subscribe(self, event_name: str, callback: EventCallback) -> None:
        """Register ``callback`` once for ``event_name``.

        Raises:
            ValueError: If ``event_name`` is blank.
            TypeError: If ``callback`` is not callable.
        """
        self._validate_event_name(event_name)
        if not callable(callback):
            raise TypeError("Event callback must be callable.")

        with self._lock:
            subscribers = self._subscribers[event_name]
            if callback not in subscribers:
                subscribers.append(callback)
                logger.debug("Subscriber registered for event '%s'", event_name)

    def unsubscribe(self, event_name: str, callback: EventCallback) -> None:
        """Remove ``callback`` from ``event_name`` if it is registered."""
        self._validate_event_name(event_name)

        with self._lock:
            subscribers = self._subscribers.get(event_name)
            if subscribers is None or callback not in subscribers:
                return

            subscribers.remove(callback)
            if not subscribers:
                del self._subscribers[event_name]
            logger.debug("Subscriber removed from event '%s'", event_name)

    def publish(self, event_name: str, **data: Any) -> Event:
        """Publish an event and return the event delivered to subscribers."""
        self._validate_event_name(event_name)
        event = Event(name=event_name, data=dict(data))

        with self._lock:
            subscribers = tuple(self._subscribers.get(event_name, ()))

        logger.debug("Publishing event '%s' to %d subscriber(s)", event_name, len(subscribers))
        for callback in subscribers:
            try:
                callback(event)
            except Exception:
                logger.exception("Event subscriber failed for event '%s'", event_name)

        return event

    def clear(self) -> None:
        """Remove every subscriber from the bus."""
        with self._lock:
            self._subscribers.clear()
        logger.info("Event bus subscribers cleared")

    def has_subscribers(self, event_name: str) -> bool:
        """Return whether at least one callback is registered for an event."""
        self._validate_event_name(event_name)
        with self._lock:
            return bool(self._subscribers.get(event_name))

    def subscriber_count(self, event_name: str) -> int:
        """Return the number of callbacks registered for an event."""
        self._validate_event_name(event_name)
        with self._lock:
            return len(self._subscribers.get(event_name, ()))

    def registered_events(self) -> list[str]:
        """Return registered event names in deterministic order."""
        with self._lock:
            return sorted(self._subscribers)

    @staticmethod
    def _validate_event_name(event_name: str) -> None:
        if not isinstance(event_name, str) or not event_name.strip():
            raise ValueError("Event name must be a non-empty string.")


# Legacy convenience API for listeners that pre-date constructor injection.
event_bus = EventBus()


def subscribe(event_name: str, callback: EventCallback) -> None:
    """Register a callback on the process-wide compatibility event bus."""
    event_bus.subscribe(event_name, callback)


def unsubscribe(event_name: str, callback: EventCallback) -> None:
    """Unregister a callback from the process-wide compatibility event bus."""
    event_bus.unsubscribe(event_name, callback)


def publish(event_name: str, **data: Any) -> Event:
    """Publish an event on the process-wide compatibility event bus."""
    return event_bus.publish(event_name, **data)


__all__ = [
    "Event",
    "EventBus",
    "EventCallback",
    "event_bus",
    "publish",
    "subscribe",
    "unsubscribe",
]
