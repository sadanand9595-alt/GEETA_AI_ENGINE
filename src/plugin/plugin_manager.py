"""File #228: discovery and import management for external plugins."""

from __future__ import annotations

import importlib
import json
import logging
import sys
from collections.abc import Mapping
from pathlib import Path
from threading import RLock
from types import ModuleType
from typing import Any

from packaging.version import InvalidVersion, Version


logger = logging.getLogger(__name__)


class PluginMetadataError(ValueError):
    """Raised when a plugin manifest cannot be used safely."""


class PluginManager:
    """Discover, validate, import, and unregister plugin modules.

    The manager intentionally does not call plugin lifecycle hooks. That
    responsibility belongs to :class:`src.plugin.plugin_loader.PluginLoader`,
    allowing callers to use discovery and metadata independently of execution.
    """

    def __init__(self, plugin_directory: str | Path = "plugins", package_name: str = "plugins") -> None:
        self._plugin_directory = Path(plugin_directory).resolve()
        self._package_name = self._validate_package_name(package_name)
        self._lock = RLock()
        self._plugins: dict[str, ModuleType] = {}
        self._metadata: dict[str, dict[str, Any]] = {}
        logger.info("Plugin manager initialized for directory '%s'", self._plugin_directory)

    @property
    def plugin_directory(self) -> Path:
        """Return the directory searched for plugin packages."""
        return self._plugin_directory

    def discover(self) -> list[Path]:
        """Return valid, immediate plugin package directories in name order."""
        if not self._plugin_directory.is_dir():
            return []

        return sorted(
            (
                path
                for path in self._plugin_directory.iterdir()
                if path.is_dir() and self._is_valid_plugin_name(path.name)
            ),
            key=lambda path: path.name,
        )

    def load_metadata(self, plugin: Path) -> dict[str, Any]:
        """Read, validate, cache, and return a plugin manifest.

        A plugin manifest is optional. When absent, an empty metadata mapping is
        returned; malformed manifests raise :class:`PluginMetadataError` so a
        caller can surface a meaningful configuration failure.
        """
        plugin_path = self._validate_plugin_path(plugin)
        metadata_file = plugin_path / "plugin.json"
        if not metadata_file.is_file():
            return {}

        try:
            decoded = json.loads(metadata_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise PluginMetadataError(f"Unable to read metadata for '{plugin_path.name}'.") from error

        if not isinstance(decoded, dict):
            raise PluginMetadataError(f"Metadata for '{plugin_path.name}' must be a JSON object.")

        metadata = dict(decoded)
        self._validate_metadata(plugin_path.name, metadata)
        with self._lock:
            self._metadata[plugin_path.name] = metadata
        return dict(metadata)

    def load(self, plugin_name: str) -> ModuleType:
        """Import ``plugin_name`` after validating its manifest and dependencies.

        Dependencies listed in the optional ``dependencies`` manifest field are
        loaded before the requested module. Cycles and missing dependencies are
        rejected with a clear error rather than partially loading a plugin.
        """
        self._validate_plugin_name(plugin_name)
        with self._lock:
            return self._load(plugin_name, loading=set())

    def unload(self, plugin_name: str) -> bool:
        """Unregister a plugin and remove its module namespace from ``sys.modules``."""
        self._validate_plugin_name(plugin_name)
        with self._lock:
            if plugin_name not in self._plugins:
                return False

            del self._plugins[plugin_name]
            module_prefix = f"{self._package_name}.{plugin_name}"
            for module_name in tuple(sys.modules):
                if module_name == module_prefix or module_name.startswith(f"{module_prefix}."):
                    del sys.modules[module_name]

            logger.info("Plugin unregistered: %s", plugin_name)
            return True

    def plugin(self, name: str) -> ModuleType | None:
        """Return a loaded plugin module, if present."""
        with self._lock:
            return self._plugins.get(name)

    def loaded_plugins(self) -> list[str]:
        """Return loaded plugin names in deterministic order."""
        with self._lock:
            return sorted(self._plugins)

    def metadata(self, name: str) -> dict[str, Any]:
        """Return a defensive copy of cached metadata for ``name``."""
        with self._lock:
            return dict(self._metadata.get(name, {}))

    def compatible(self, name: str, ide_version: str) -> bool:
        """Return whether ``ide_version`` meets a plugin's minimum version."""
        try:
            current_version = Version(ide_version)
        except InvalidVersion:
            logger.warning("Invalid IDE version supplied for compatibility check: %r", ide_version)
            return False

        metadata = self.metadata(name)
        minimum = metadata.get("minimum_ide_version", metadata.get("minimum_version"))
        if minimum is None:
            return True
        if not isinstance(minimum, str):
            logger.warning("Plugin '%s' has a non-string minimum version", name)
            return False

        try:
            return current_version >= Version(minimum)
        except InvalidVersion:
            logger.warning("Plugin '%s' has an invalid minimum version: %r", name, minimum)
            return False

    def statistics(self) -> dict[str, int]:
        """Return manager counts without importing additional plugins."""
        with self._lock:
            loaded = len(self._plugins)
            metadata_loaded = len(self._metadata)
        return {
            "discovered": len(self.discover()),
            "loaded": loaded,
            "metadata_loaded": metadata_loaded,
        }

    def report(self) -> dict[str, object]:
        """Return a diagnostics-safe manager summary."""
        return {"statistics": self.statistics(), "plugins": self.loaded_plugins()}

    def _load(self, plugin_name: str, loading: set[str]) -> ModuleType:
        existing = self._plugins.get(plugin_name)
        if existing is not None:
            return existing
        if plugin_name in loading:
            cycle = " -> ".join([*sorted(loading), plugin_name])
            raise PluginMetadataError(f"Plugin dependency cycle detected: {cycle}")

        plugin_path = self._plugin_path(plugin_name)
        metadata = self.load_metadata(plugin_path)
        loading.add(plugin_name)
        try:
            for dependency in self._dependencies(plugin_name, metadata):
                self._load(dependency, loading)
            module = importlib.import_module(f"{self._package_name}.{plugin_name}")
        except Exception:
            logger.exception("Failed to import plugin '%s'", plugin_name)
            raise
        finally:
            loading.remove(plugin_name)

        self._plugins[plugin_name] = module
        logger.info("Plugin imported: %s", plugin_name)
        return module

    def _plugin_path(self, plugin_name: str) -> Path:
        plugin_path = (self._plugin_directory / plugin_name).resolve()
        if not plugin_path.is_dir() or not plugin_path.is_relative_to(self._plugin_directory):
            raise FileNotFoundError(f"Plugin '{plugin_name}' was not found in '{self._plugin_directory}'.")
        return plugin_path

    def _validate_plugin_path(self, plugin: Path) -> Path:
        plugin_path = plugin.resolve()
        if not plugin_path.is_dir() or not plugin_path.is_relative_to(self._plugin_directory):
            raise ValueError("Plugin metadata path must be a directory within the plugin directory.")
        self._validate_plugin_name(plugin_path.name)
        return plugin_path

    @staticmethod
    def _dependencies(plugin_name: str, metadata: Mapping[str, Any]) -> list[str]:
        dependencies = metadata.get("dependencies", [])
        if not isinstance(dependencies, list) or not all(
            isinstance(dependency, str) and dependency.isidentifier() for dependency in dependencies
        ):
            raise PluginMetadataError(f"Plugin '{plugin_name}' has invalid dependencies.")
        if len(set(dependencies)) != len(dependencies):
            raise PluginMetadataError(f"Plugin '{plugin_name}' lists duplicate dependencies.")
        return dependencies

    @staticmethod
    def _validate_metadata(plugin_name: str, metadata: Mapping[str, Any]) -> None:
        declared_name = metadata.get("name")
        if declared_name is not None and declared_name != plugin_name:
            raise PluginMetadataError(
                f"Plugin metadata name '{declared_name}' does not match directory '{plugin_name}'."
            )
        PluginManager._dependencies(plugin_name, metadata)

    @staticmethod
    def _validate_plugin_name(plugin_name: str) -> None:
        if not PluginManager._is_valid_plugin_name(plugin_name):
            raise ValueError("Plugin name must be a valid Python identifier.")

    @staticmethod
    def _is_valid_plugin_name(plugin_name: str) -> bool:
        return isinstance(plugin_name, str) and plugin_name.isidentifier()

    @staticmethod
    def _validate_package_name(package_name: str) -> str:
        parts = package_name.split(".")
        if not parts or not all(part.isidentifier() for part in parts):
            raise ValueError("Plugin package name must be a dotted Python package name.")
        return package_name


plugin_manager = PluginManager()


__all__ = ["PluginManager", "PluginMetadataError", "plugin_manager"]
