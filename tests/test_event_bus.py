"""
==============================================================================
GEETA AI Engine

File        : test_event_bus.py
Package     : tests
Description : Unit Tests for Event Bus

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import unittest

from core.event_bus import (
    Event,
    EventBus,
)


class TestEventBus(unittest.TestCase):
    """
    Unit tests for EventBus.
    """

    def setUp(self) -> None:
        """
        Create fresh EventBus instance.
        """

        self.event_bus = EventBus()

        self.received = False

        self.received_event: Event | None = None

    ###########################################################################

    def callback(
        self,
        event: Event,
    ) -> None:
        """
        Test callback.
        """

        self.received = True

        self.received_event = event

    ###########################################################################

    def test_subscribe(self) -> None:
        """
        Verify subscriber registration.
        """

        self.event_bus.subscribe(
            "startup",
            self.callback,
        )

        self.assertTrue(
            self.event_bus.has_subscribers(
                "startup"
            )
        )

    ###########################################################################

    def test_publish(self) -> None:
        """
        Verify event publishing.
        """

        self.event_bus.subscribe(
            "startup",
            self.callback,
        )

        self.event_bus.publish(
            "startup",
            version="1.0.0",
        )

        self.assertTrue(self.received)

        self.assertIsNotNone(
            self.received_event
        )

        self.assertEqual(
            self.received_event.name,
            "startup",
        )

        self.assertEqual(
            self.received_event.data["version"],
            "1.0.0",
        )

    ###########################################################################

    def test_unsubscribe(self) -> None:
        """
        Verify subscriber removal.
        """

        self.event_bus.subscribe(
            "startup",
            self.callback,
        )

        self.event_bus.unsubscribe(
            "startup",
            self.callback,
        )

        self.assertFalse(
            self.event_bus.has_subscribers(
                "startup"
            )
        )

    ###########################################################################

    def test_registered_events(self) -> None:
        """
        Verify registered events.
        """

        self.event_bus.subscribe(
            "event_one",
            self.callback,
        )

        self.event_bus.subscribe(
            "event_two",
            self.callback,
        )

        events = self.event_bus.registered_events()

        self.assertEqual(
            len(events),
            2,
        )

    ###########################################################################

    def test_clear(self) -> None:
        """
        Verify clear().
        """

        self.event_bus.subscribe(
            "startup",
            self.callback,
        )

        self.event_bus.clear()

        self.assertFalse(
            self.event_bus.has_subscribers(
                "startup"
            )
        )

    ###########################################################################

    def test_duplicate_subscriber_is_called_once(self) -> None:
        """Registering the same callback twice must not duplicate delivery."""

        self.event_bus.subscribe("startup", self.callback)
        self.event_bus.subscribe("startup", self.callback)

        self.event_bus.publish("startup")

        self.assertTrue(self.received)
        self.assertEqual(self.event_bus.subscriber_count("startup"), 1)

    ###########################################################################

    def test_failed_subscriber_does_not_block_remaining_subscribers(self) -> None:
        """Subscriber failures are isolated from other event listeners."""

        def failing_callback(event: Event) -> None:
            raise RuntimeError(f"Cannot process {event.name}")

        self.event_bus.subscribe("startup", failing_callback)
        self.event_bus.subscribe("startup", self.callback)

        self.event_bus.publish("startup")

        self.assertTrue(self.received)

    ###########################################################################

    def test_blank_event_name_is_rejected(self) -> None:
        """Blank event topics cannot silently create unusable subscriptions."""

        with self.assertRaises(ValueError):
            self.event_bus.publish(" ")


###############################################################################
# Entry Point
###############################################################################

if __name__ == "__main__":
    unittest.main(verbosity=2)
