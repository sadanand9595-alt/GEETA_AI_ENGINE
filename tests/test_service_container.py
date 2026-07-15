"""
==============================================================================
GEETA AI Engine

File        : test_service_container.py
Package     : tests
Description : Unit Tests for Service Container

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import unittest

from core.service_container import ServiceContainer


class DummyService:
    """
    Test service.
    """

    def __init__(self) -> None:
        self.name = "DummyService"


class TestServiceContainer(unittest.TestCase):
    """
    Unit tests for ServiceContainer.
    """

    def setUp(self) -> None:
        """
        Create a fresh container.
        """

        self.container = ServiceContainer()

        self.container.clear()

    ###########################################################################

    def test_register_service(self) -> None:
        """
        Verify service registration.
        """

        self.container.register(
            "dummy",
            DummyService,
        )

        self.assertTrue(
            self.container.is_registered(
                "dummy"
            )
        )

    ###########################################################################

    def test_resolve_service(self) -> None:
        """
        Verify transient service resolution.
        """

        self.container.register(
            "dummy",
            DummyService,
        )

        service = self.container.resolve(
            "dummy"
        )

        self.assertIsInstance(
            service,
            DummyService,
        )

    ###########################################################################

    def test_register_singleton(self) -> None:
        """
        Verify singleton registration.
        """

        instance = DummyService()

        self.container.register_singleton(
            "singleton",
            instance,
        )

        resolved = self.container.resolve(
            "singleton"
        )

        self.assertIs(
            resolved,
            instance,
        )

    ###########################################################################

    def test_remove_service(self) -> None:
        """
        Verify service removal.
        """

        self.container.register(
            "dummy",
            DummyService,
        )

        removed = self.container.remove(
            "dummy"
        )

        self.assertTrue(removed)

        self.assertFalse(
            self.container.is_registered(
                "dummy"
            )
        )

    ###########################################################################

    def test_registered_services(self) -> None:
        """
        Verify registered service list.
        """

        self.container.register(
            "service_one",
            DummyService,
        )

        self.container.register(
            "service_two",
            DummyService,
        )

        services = (
            self.container.registered_services()
        )

        self.assertEqual(
            len(services),
            2,
        )

    ###########################################################################

    def test_service_count(self) -> None:
        """
        Verify service count.
        """

        self.container.register(
            "service_one",
            DummyService,
        )

        self.container.register(
            "service_two",
            DummyService,
        )

        self.assertEqual(
            self.container.service_count(),
            2,
        )

    ###########################################################################

    def test_clear(self) -> None:
        """
        Verify clear().
        """

        self.container.register(
            "dummy",
            DummyService,
        )

        self.container.clear()

        self.assertEqual(
            self.container.service_count(),
            0,
        )

    ###########################################################################

    def test_unregistered_service(self) -> None:
        """
        Verify resolving an unknown service raises KeyError.
        """

        with self.assertRaises(KeyError):
            self.container.resolve(
                "unknown_service"
            )


###############################################################################
# Entry Point
###############################################################################

if __name__ == "__main__":
    unittest.main(verbosity=2)