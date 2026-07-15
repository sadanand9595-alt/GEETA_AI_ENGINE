"""
==============================================================================
GEETA AI Engine

File        : test_bootstrap.py
Package     : tests
Description : Unit Tests for Bootstrap

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import unittest

from core.bootstrap import Bootstrap


###############################################################################
# Tests
###############################################################################


class TestBootstrap(unittest.TestCase):
    """
    Unit tests for Bootstrap.
    """

    def setUp(self) -> None:
        """
        Create a fresh Bootstrap instance.
        """

        self.bootstrap = Bootstrap()

    ###########################################################################

    def test_initial_state(self) -> None:
        """
        Verify bootstrap is not initialized initially.
        """

        self.assertFalse(
            self.bootstrap.initialized
        )

    ###########################################################################

    def test_initialize(self) -> None:
        """
        Verify bootstrap initializes successfully.
        """

        self.bootstrap.initialize()

        self.assertTrue(
            self.bootstrap.initialized
        )

    ###########################################################################

    def test_initialize_twice(self) -> None:
        """
        Calling initialize() multiple times should be safe.
        """

        self.bootstrap.initialize()

        self.bootstrap.initialize()

        self.assertTrue(
            self.bootstrap.initialized
        )

    ###########################################################################

    def test_shutdown(self) -> None:
        """
        Verify bootstrap shutdown.
        """

        self.bootstrap.initialize()

        self.bootstrap.shutdown()

        self.assertFalse(
            self.bootstrap.initialized
        )

    ###########################################################################

    def test_shutdown_without_initialize(self) -> None:
        """
        Shutdown before initialization should not fail.
        """

        self.bootstrap.shutdown()

        self.assertFalse(
            self.bootstrap.initialized
        )

    ###########################################################################

    def test_reinitialize_after_shutdown(self) -> None:
        """
        Bootstrap should support initialize -> shutdown -> initialize.
        """

        self.bootstrap.initialize()

        self.bootstrap.shutdown()

        self.bootstrap.initialize()

        self.assertTrue(
            self.bootstrap.initialized
        )


###############################################################################
# Entry Point
###############################################################################

if __name__ == "__main__":

    unittest.main(verbosity=2)