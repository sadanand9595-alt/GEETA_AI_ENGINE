"""Focused integration tests for File #228 plugin discovery and imports."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

from src.plugin.plugin_manager import PluginManager, PluginMetadataError


class TestSourcePluginManager(unittest.TestCase):
    """Verify manifest validation, dependency order, and module cleanup."""

    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.package_name = "test_plugins"
        self.package_directory = self.root / self.package_name
        self.package_directory.mkdir()
        (self.package_directory / "__init__.py").write_text("", encoding="utf-8")
        sys.path.insert(0, str(self.root))
        self.manager = PluginManager(self.package_directory, self.package_name)

    def tearDown(self) -> None:
        sys.path.remove(str(self.root))
        for module_name in tuple(sys.modules):
            if module_name == self.package_name or module_name.startswith(f"{self.package_name}."):
                del sys.modules[module_name]
        self.temporary_directory.cleanup()

    def create_plugin(self, name: str, metadata: dict[str, object]) -> None:
        """Create a real importable plugin package and manifest."""
        plugin_directory = self.package_directory / name
        plugin_directory.mkdir()
        (plugin_directory / "__init__.py").write_text("PLUGIN = True\n", encoding="utf-8")
        (plugin_directory / "plugin.json").write_text(json.dumps(metadata), encoding="utf-8")

    def test_loads_dependencies_before_requested_plugin(self) -> None:
        """Dependencies are imported and recorded before their dependent plugin."""
        self.create_plugin("dependency", {"name": "dependency", "version": "1.0.0"})
        self.create_plugin(
            "feature",
            {"name": "feature", "dependencies": ["dependency"], "minimum_ide_version": "1.2"},
        )

        plugin = self.manager.load("feature")

        self.assertTrue(plugin.PLUGIN)
        self.assertEqual(self.manager.loaded_plugins(), ["dependency", "feature"])
        self.assertTrue(self.manager.compatible("feature", "1.2.0"))
        self.assertFalse(self.manager.compatible("feature", "1.1.9"))

    def test_unload_removes_the_plugin_module_namespace(self) -> None:
        """Unregistering removes the module so a future import starts fresh."""
        self.create_plugin("feature", {"name": "feature"})
        self.manager.load("feature")

        self.assertTrue(self.manager.unload("feature"))
        self.assertNotIn(f"{self.package_name}.feature", sys.modules)
        self.assertEqual(self.manager.loaded_plugins(), [])

    def test_rejects_metadata_with_a_mismatched_name(self) -> None:
        """A manifest cannot claim the identity of a different plugin."""
        self.create_plugin("feature", {"name": "other"})

        with self.assertRaises(PluginMetadataError):
            self.manager.load_metadata(self.package_directory / "feature")


if __name__ == "__main__":
    unittest.main(verbosity=2)
