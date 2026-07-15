"""Focused tests for File #227 plugin lifecycle handling."""

from __future__ import annotations

from types import ModuleType
import unittest

from src.plugin.plugin_loader import PluginLoader


class InMemoryPluginManager:
    """Concrete in-memory manager used to exercise the loader contract."""

    def __init__(self, module: ModuleType) -> None:
        self.module = module
        self.loaded_names: list[str] = []
        self.unloaded_names: list[str] = []

    def load(self, plugin_name: str) -> ModuleType:
        self.loaded_names.append(plugin_name)
        return self.module

    def unload(self, plugin_name: str) -> bool:
        self.unloaded_names.append(plugin_name)
        return True


class TestPluginLoader(unittest.TestCase):
    """Verify loader lifecycle and failure isolation."""

    def setUp(self) -> None:
        self.calls: list[str] = []
        self.module = ModuleType("sample_plugin")
        self.module.initialize = lambda: self.calls.append("initialize")
        self.module.shutdown = lambda: self.calls.append("shutdown")
        self.manager = InMemoryPluginManager(self.module)
        self.loader = PluginLoader(self.manager)

    def test_load_is_idempotent_and_initializes_once(self) -> None:
        """A loaded module is not initialized again."""
        first = self.loader.load("sample_plugin")
        second = self.loader.load("sample_plugin")

        self.assertIs(first, self.module)
        self.assertIs(second, self.module)
        self.assertEqual(self.calls, ["initialize"])
        self.assertEqual(self.manager.loaded_names, ["sample_plugin"])

    def test_unload_shuts_down_then_unregisters(self) -> None:
        """Unloading completes both lifecycle stages in order."""
        self.loader.load("sample_plugin")

        unloaded = self.loader.unload("sample_plugin")

        self.assertTrue(unloaded)
        self.assertEqual(self.calls, ["initialize", "shutdown"])
        self.assertEqual(self.manager.unloaded_names, ["sample_plugin"])
        self.assertIsNone(self.loader.plugin("sample_plugin"))

    def test_initialize_failure_is_cleaned_up(self) -> None:
        """Failed initialization leaves no loaded or manager registration state."""
        def fail_initialize() -> None:
            raise RuntimeError("initialization failed")

        self.module.initialize = fail_initialize

        loaded = self.loader.load("sample_plugin")

        self.assertIsNone(loaded)
        self.assertEqual(self.loader.plugins(), [])
        self.assertEqual(self.manager.unloaded_names, ["sample_plugin"])

    def test_invalid_name_is_rejected_without_manager_access(self) -> None:
        """Invalid import names cannot reach the manager boundary."""
        self.assertIsNone(self.loader.load("../../plugin"))
        self.assertEqual(self.manager.loaded_names, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
