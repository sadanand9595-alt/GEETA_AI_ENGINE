"""Focused tests for File #229 plugin metadata indexing."""

from __future__ import annotations

import unittest

from src.plugin.plugin_registry import PluginRegistry


class TestSourcePluginRegistry(unittest.TestCase):
    """Verify registry behavior, copies, and validation."""

    def setUp(self) -> None:
        self.registry = PluginRegistry()

    def test_register_search_and_defensive_copies(self) -> None:
        """Registered metadata is indexed and returned as a copy."""
        metadata = {
            "name": "sample_plugin",
            "version": "1.2.3",
            "capabilities": ["search", "format"],
            "dependencies": ["core"],
            "description": "Sample plugin",
        }

        self.registry.register(metadata)

        stored = self.registry.plugin("sample_plugin")
        self.assertIsNotNone(stored)
        assert stored is not None
        stored["capabilities"].append("mutated")

        self.assertEqual(self.registry.plugins(), ["sample_plugin"])
        self.assertEqual(self.registry.search("sample"), ["sample_plugin"])
        self.assertEqual(self.registry.version("sample_plugin"), "1.2.3")
        self.assertEqual(self.registry.capabilities("sample_plugin"), ["search", "format"])
        self.assertEqual(self.registry.dependencies("sample_plugin"), ["core"])

    def test_unregister_and_statistics(self) -> None:
        """Unregistering removes the plugin and updates registry counts."""
        self.registry.register({"name": "alpha", "version": "1.0.0"})
        self.registry.register({"name": "beta", "version": "2.0.0", "capabilities": ["lint"]})

        self.assertEqual(self.registry.statistics()["registered_plugins"], 2)
        self.assertTrue(self.registry.unregister("alpha"))
        self.assertFalse(self.registry.unregister("alpha"))
        self.assertEqual(self.registry.plugins(), ["beta"])
        self.assertEqual(self.registry.statistics()["versioned_plugins"], 1)
        self.assertEqual(self.registry.statistics()["capability_entries"], 1)

    def test_rejects_invalid_metadata(self) -> None:
        """Invalid metadata is rejected before it reaches the registry."""
        with self.assertRaises(ValueError):
            self.registry.register({"version": "1.0.0"})

        with self.assertRaises(ValueError):
            self.registry.register({"name": "not valid", "version": "1.0.0"})

        with self.assertRaises(ValueError):
            self.registry.register({"name": "duplicate", "capabilities": ["a", "a"]})


if __name__ == "__main__":
    unittest.main(verbosity=2)
