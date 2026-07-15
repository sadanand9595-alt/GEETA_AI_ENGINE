"""
==============================================================================
GEETA AI Engine

File        : test_application.py
Package     : tests
Description : Unit Tests for Application

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import unittest

from core.application import Application


###############################################################################
# Tests
###############################################################################


class TestApplication(unittest.TestCase):
    """
    Unit tests for Application.
    """

    def setUp(self) -> None:
        """
        Create a fresh application instance.
        """

        self.application = Application()

    ###########################################################################

    def test_initial_state(self) -> None:
        """
        Verify application is not running initially.
        """

        self.assertFalse(
            self.application.running
        )

    ###########################################################################

    def test_start(self) -> None:
        """
        Verify application starts successfully.
        """

        self.application.start()

        self.assertTrue(
            self.application.running
        )

    ###########################################################################

    def test_stop(self) -> None:
        """
        Verify application stops successfully.
        """

        self.application.start()

        self.application.stop()

        self.assertFalse(
            self.application.running
        )

    ###########################################################################

    def test_restart(self) -> None:
        """
        Verify restart keeps application running.
        """

        self.application.start()

        self.application.restart()

        self.assertTrue(
            self.application.running
        )

    ###########################################################################

    def test_multiple_start(self) -> None:
        """
        Calling start() multiple times should not fail.
        """

        self.application.start()

        self.application.start()

        self.application.start()

        self.assertTrue(
            self.application.running
        )

    ###########################################################################

    def test_multiple_stop(self) -> None:
        """
        Calling stop() multiple times should not fail.
        """

        self.application.stop()

        self.application.stop()

        self.application.stop()

        self.assertFalse(
            self.application.running
        )

    ###########################################################################

    def test_shutdown(self) -> None:
        """
        Verify graceful shutdown.
        """

        self.application.start()

        self.application.shutdown()

        self.assertFalse(
            self.application.running
        )


###############################################################################
# Entry Point
###############################################################################

if __name__ == "__main__":

    unittest.main(verbosity=2)