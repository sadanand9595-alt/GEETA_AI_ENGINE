"""File #229: registry and metadata indexing for the plugin subsystem."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from copy import deepcopy
from threading import RLock
from typing import Any, cast

logger = logging.getLogger(__name__)


class PluginRegistry:
    """Thread-safe metadata registry for loaded or discoverable plugins.

    The registry keeps plugin identity, version, capabilities, and dependency
    metadata separate from module loading. The loader and manager own import
    lifecycles; this registry owns the index that diagnostics and UI layers can
    query without touching plugin import state.
    """

    def __init__(self) -> None:
        self._lock = RLock()
        self._plugins: dict[str, dict[str, Any]] = {}
        logger.info("Plugin registry initialized")

    def register(self, metadata: Mapping[str, Any]) -> None:
        """Register or replace a plugin metadata record."""
        normalized = self._normalize_metadata(metadata)
        name = cast(str, normalized["name"])

        with self._lock:
            replaced = name in self._plugins
            self._plugins[name] = normalized

        if replaced:
            logger.info("Plugin metadata updated: %s", name)
        else:
            logger.info("Plugin registered: %s", name)

    def unregister(self, name: str) -> bool:
        """Remove a plugin metadata record."""
        if not self._is_valid_plugin_name(name):
            return False

        with self._lock:
            if name not in self._plugins:
                return False
            del self._plugins[name]

        logger.info("Plugin removed: %s", name)
        return True

    def plugin(self, name: str) -> dict[str, Any] | None:
        """Return a defensive copy of the registered metadata, if present."""
        if not self._is_valid_plugin_name(name):
            return None

        with self._lock:
            metadata = self._plugins.get(name)
            if metadata is None:
                return None
            return cast(dict[str, Any], deepcopy(metadata))

    def plugins(self) -> list[str]:
        """Return registered plugin names in deterministic order."""
        with self._lock:
            return sorted(self._plugins)

    def search(self, keyword: str) -> list[str]:
        """Search registered plugins by name and common metadata fields."""
        if not isinstance(keyword, str):
            raise TypeError("Search keyword must be a string.")

        normalized_keyword = keyword.casefold().strip()
        if not normalized_keyword:
            return self.plugins()

        with self._lock:
            return sorted(
                name
                for name, metadata in self._plugins.items()
                if self._matches(metadata, name, normalized_keyword)
            )

    def version(self, name: str) -> str | None:
        """Return the registered version string for ``name``."""
        metadata = self.plugin(name)
        if metadata is None:
            return None

        version = metadata.get("version")
        return version if isinstance(version, str) else None

    def capabilities(self, name: str) -> list[str]:
        """Return the registered capability list for ``name``."""
        metadata = self.plugin(name)
        if metadata is None:
            return []

        return self._string_list(metadata, "capabilities")

    def dependencies(self, name: str) -> list[str]:
        """Return the registered dependency list for ``name``."""
        metadata = self.plugin(name)
        if metadata is None:
            return []

        return self._string_list(metadata, "dependencies", identifier_required=True)

    def statistics(self) -> dict[str, Any]:
        """Return registry statistics without exposing internal state."""
        with self._lock:
            registered_plugins = len(self._plugins)
            versioned_plugins = sum(
                1 for metadata in self._plugins.values() if isinstance(metadata.get("version"), str)
            )
            capability_entries = sum(
                len(self._string_list(metadata, "capabilities")) for metadata in self._plugins.values()
            )
            dependency_entries = sum(
                len(self._string_list(metadata, "dependencies", identifier_required=True))
                for metadata in self._plugins.values()
            )

        return {
            "registered_plugins": registered_plugins,
            "versioned_plugins": versioned_plugins,
            "capability_entries": capability_entries,
            "dependency_entries": dependency_entries,
        }

    def report(self) -> dict[str, Any]:
        """Return a diagnostics-safe registry summary."""
        with self._lock:
            metadata = {name: cast(dict[str, Any], deepcopy(value)) for name, value in self._plugins.items()}

        return {
            "statistics": self.statistics(),
            "plugins": self.plugins(),
            "metadata": metadata,
        }

    def clear(self) -> None:
        """Remove all registered plugin metadata."""
        with self._lock:
            self._plugins.clear()

        logger.info("Plugin registry cleared")

    def _normalize_metadata(self, metadata: Mapping[str, Any]) -> dict[str, Any]:
        if not isinstance(metadata, Mapping):
            raise TypeError("Plugin metadata must be a mapping.")

        normalized = cast(dict[str, Any], deepcopy(dict(metadata)))
        name = normalized.get("name")
        self._validate_plugin_name(name)
        normalized["name"] = cast(str, name)

        version = normalized.get("version")
        if version is not None and not isinstance(version, str):
            raise ValueError("Plugin version must be a string when provided.")

        normalized["capabilities"] = self._string_list(
            normalized,
            "capabilities",
            allow_missing=True,
        )
        normalized["dependencies"] = self._string_list(
            normalized,
            "dependencies",
            allow_missing=True,
            identifier_required=True,
        )

        return normalized

    @staticmethod
    def _matches(metadata: Mapping[str, Any], name: str, keyword: str) -> bool:
        values: list[str] = [name]
        for field_name in (
            "version",
            "author",
            "description",
            "summary",
            "homepage",
            "license",
            "minimum_ide_version",
            "minimum_version",
        ):
            field_value = metadata.get(field_name)
            if isinstance(field_value, str):
                values.append(field_value)

        for field_name in ("capabilities", "dependencies", "keywords", "tags"):
            values.extend(PluginRegistry._string_list(metadata, field_name, allow_missing=True))

        return any(keyword in candidate.casefold() for candidate in values)

    @staticmethod
    def _string_list(
        metadata: Mapping[str, Any],
        field_name: str,
        *,
        allow_missing: bool = False,
        identifier_required: bool = False,
    ) -> list[str]:
        raw_value = metadata.get(field_name)
        if raw_value is None:
            if allow_missing:
                return []
            raise ValueError(f"Plugin metadata field '{field_name}' is required.")

        if not isinstance(raw_value, list) or any(not isinstance(item, str) for item in raw_value):
            raise ValueError(f"Plugin metadata field '{field_name}' must be a list of strings.")

        if identifier_required and any(not item.isidentifier() for item in raw_value):
            raise ValueError(f"Plugin metadata field '{field_name}' must contain valid identifiers.")

        if len(set(raw_value)) != len(raw_value):
            raise ValueError(f"Plugin metadata field '{field_name}' cannot contain duplicates.")

        return list(raw_value)

    @staticmethod
    def _validate_plugin_name(name: Any) -> None:
        if not isinstance(name, str) or not name.isidentifier():
            raise ValueError("Plugin name must be a valid Python identifier.")

    @staticmethod
    def _is_valid_plugin_name(name: Any) -> bool:
        return isinstance(name, str) and name.isidentifier()


plugin_registry = PluginRegistry()


__all__ = ["PluginRegistry", "plugin_registry"]
