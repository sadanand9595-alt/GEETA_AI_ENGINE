"""File #227: lifecycle-safe loading for external plugin modules.

The loader owns module lifecycle transitions. Discovery, metadata, and module
resolution stay in :mod:`plugin_manager`, so callers can replace that service
without coupling plugin lifecycle code to a filesystem layout.
"""

from __future__ import annotations

import importlib
import logging
from threading import RLock
from types import ModuleType
from typing import Protocol, cast


logger = logging.getLogger(__name__)

class PluginModuleManager(Protocol):
    """The focused module-management contract required by ``PluginLoader``."""

    def load(self, plugin_name: str) -> ModuleType:
        """Import and register a plugin module."""

    def unload(self, plugin_name: str) -> bool:
        """Remove a plugin module from the manager registry."""


class PluginLoader:
    """Load, unload, and reload plugin modules with lifecycle isolation.

    A plugin may expose module-level ``initialize`` and ``shutdown`` hooks.
    Hooks run synchronously on the caller's thread, because they can safely
    establish or release the plugin resources they own. Exceptions are logged
    and converted to an explicit failure result, preserving the original
    public API.
    """

    def __init__(self, manager: PluginModuleManager | None = None) -> None:
        self._lock = RLock()
        self._manager = manager
        self._loaded: dict[str, ModuleType] = {}
        logger.info("Plugin loader initialized")

    def load(self, plugin_name: str) -> ModuleType | None:
        """Load and initialize ``plugin_name`` once.

        Returns the existing module when it is already initialized. ``None``
        signals that importing or initializing the plugin failed.
        """
        if not self._is_valid_plugin_name(plugin_name):
            logger.warning("Rejected invalid plugin name: %r", plugin_name)
            return None

        with self._lock:
            existing = self._loaded.get(plugin_name)
            if existing is not None:
                return existing

            manager = self._resolve_manager()
            if manager is None:
                return None

            try:
                module = manager.load(plugin_name)
                self._ensure_module(plugin_name, module)
                self._run_hook(plugin_name, module, "initialize")
            except Exception:
                logger.exception("Failed to load plugin '%s'", plugin_name)
                self._discard_manager_registration(manager, plugin_name)
                return None

            self._loaded[plugin_name] = module
            logger.info("Plugin initialized: %s", plugin_name)
            return module

    def unload(self, plugin_name: str) -> bool:
        """Shut down and unregister a loaded plugin.

        A shutdown failure leaves the plugin tracked so the caller can retry or
        inspect it. The module is removed only after both lifecycle and manager
        transitions complete.
        """
        if not self._is_valid_plugin_name(plugin_name):
            return False

        with self._lock:
            module = self._loaded.get(plugin_name)
            if module is None:
                return False

            manager = self._resolve_manager()
            if manager is None:
                return False

            try:
                self._run_hook(plugin_name, module, "shutdown")
            except Exception:
                logger.exception("Failed to shut down plugin '%s'", plugin_name)
                return False

            try:
                unloaded = manager.unload(plugin_name)
            except Exception:
                logger.exception("Failed to unregister plugin '%s'", plugin_name)
                return False

            if not unloaded:
                logger.warning("Plugin manager did not unregister plugin '%s'", plugin_name)
                return False

            del self._loaded[plugin_name]
            logger.info("Plugin unloaded: %s", plugin_name)
            return True

    def reload(self, plugin_name: str) -> ModuleType | None:
        """Reload an initialized plugin and run its lifecycle hooks in order."""
        if not self._is_valid_plugin_name(plugin_name):
            return None

        with self._lock:
            module = self._loaded.get(plugin_name)
            if module is None:
                return self.load(plugin_name)

            try:
                self._run_hook(plugin_name, module, "shutdown")
            except Exception:
                logger.exception("Failed to shut down plugin '%s' before reload", plugin_name)
                return None

            try:
                reloaded_module = importlib.reload(module)
                self._run_hook(plugin_name, reloaded_module, "initialize")
            except Exception:
                logger.exception("Failed to reload plugin '%s'", plugin_name)
                self._loaded.pop(plugin_name, None)
                manager = self._resolve_manager()
                if manager is not None:
                    self._discard_manager_registration(manager, plugin_name)
                return None

            self._loaded[plugin_name] = reloaded_module
            logger.info("Plugin reloaded: %s", plugin_name)
            return reloaded_module

    def plugin(self, name: str) -> ModuleType | None:
        """Return an initialized plugin module by name."""
        with self._lock:
            return self._loaded.get(name)

    def plugins(self) -> list[str]:
        """Return initialized plugin names in deterministic order."""
        with self._lock:
            return sorted(self._loaded)

    def statistics(self) -> dict[str, int | list[str]]:
        """Return a concise snapshot of loader state."""
        plugins = self.plugins()
        return {"loaded_plugins": len(plugins), "plugin_names": plugins}

    def report(self) -> dict[str, object]:
        """Return module names for diagnostics without exposing module objects."""
        with self._lock:
            modules = {name: module.__name__ for name, module in self._loaded.items()}
        return {"statistics": self.statistics(), "plugins": modules}

    def _resolve_manager(self) -> PluginModuleManager | None:
        if self._manager is not None:
            return self._manager

        try:
            package_name = __package__
            if package_name is None:
                raise ImportError("Plugin loader has no package context.")
            manager_module = importlib.import_module(f"{package_name}.plugin_manager")
            plugin_manager = cast(PluginModuleManager, manager_module.plugin_manager)
        except (AttributeError, ImportError):
            logger.exception("Plugin manager is unavailable")
            return None

        self._manager = plugin_manager
        return plugin_manager

    @staticmethod
    def _ensure_module(plugin_name: str, module: ModuleType) -> None:
        if not isinstance(module, ModuleType):
            raise TypeError(f"Plugin manager returned a non-module for '{plugin_name}'.")

    @staticmethod
    def _run_hook(plugin_name: str, module: ModuleType, hook_name: str) -> None:
        hook = getattr(module, hook_name, None)
        if hook is None:
            return
        if not callable(hook):
            raise TypeError(f"Plugin '{plugin_name}' has a non-callable {hook_name} hook.")
        hook()

    @staticmethod
    def _is_valid_plugin_name(plugin_name: str) -> bool:
        return isinstance(plugin_name, str) and plugin_name.isidentifier()

    @staticmethod
    def _discard_manager_registration(manager: PluginModuleManager, plugin_name: str) -> None:
        try:
            manager.unload(plugin_name)
        except Exception:
            logger.exception("Failed to clean up plugin '%s' after load failure", plugin_name)


plugin_loader = PluginLoader()


__all__ = ["PluginLoader", "PluginModuleManager", "plugin_loader"]
