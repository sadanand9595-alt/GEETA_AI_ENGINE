"""
==============================================================================
GEETA AI Engine

File        : test_plugin_manager.py
Package     : tests
Description : Unit Tests for Plugin Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import unittest

from core.plugin_manager import (
    Plugin,
    PluginManager,
)


###############################################################################
# Dummy Plugin
###############################################################################


class DummyPlugin(Plugin):
    """
    Dummy plugin used for testing.
    """

    def __init__(self) -> None:

        self.initialized = False

        self.stopped = False

    @property
    def name(self) -> str:

        return "dummy"

    @property
    def version(self) -> str:

        return "1.0.0"

    def initialize(self) -> None:

        self.initialized = True

    def shutdown(self) -> None:

        self.stopped = True


###############################################################################
# Tests
###############################################################################


class TestPluginManager(unittest.TestCase):
    """
    Unit tests for PluginManager.
    """

    def setUp(self) -> None:

        self.manager = PluginManager()

    ###########################################################################

    def test_register_plugin(self) -> None:

        plugin = DummyPlugin()

        self.manager.register(plugin)

        self.assertTrue(
            self.manager.exists("dummy")
        )

    ###########################################################################

    def test_get_plugin(self) -> None:

        plugin = DummyPlugin()

        self.manager.register(plugin)

        loaded = self.manager.get("dummy")

        self.assertIs(
            loaded,
            plugin,
        )

    ###########################################################################

    def test_unregister_plugin(self) -> None:

        plugin = DummyPlugin()

        self.manager.register(plugin)

        self.manager.unregister("dummy")

        self.assertFalse(
            self.manager.exists("dummy")
        )

        self.assertTrue(
            plugin.stopped
        )

    ###########################################################################

    def test_plugin_count(self) -> None:

        self.manager.register(
            DummyPlugin()
        )

        self.assertEqual(
            self.manager.plugin_count(),
            1,
        )

    ###########################################################################

    def test_plugins(self) -> None:

        self.manager.register(
            DummyPlugin()
        )

        plugins = self.manager.plugins()

        self.assertEqual(
            plugins,
            ["dummy"],
        )

    ###########################################################################

    def test_clear(self) -> None:

        self.manager.register(
            DummyPlugin()
        )

        self.manager.clear()

        self.assertEqual(
            self.manager.plugin_count(),
            0,
        )

    ###########################################################################

    def test_duplicate_plugin(self) -> None:

        plugin = DummyPlugin()

        self.manager.register(plugin)

        with self.assertRaises(ValueError):

            self.manager.register(
                DummyPlugin()
            )


###############################################################################
# Entry Point
###############################################################################

if __name__ == "__main__":

    unittest.main(verbosity=2)