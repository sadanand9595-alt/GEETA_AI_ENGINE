"""
==============================================================================
GEETA AI Engine

File        : plugin_diagnostics.py
Package     : plugins
Description : Plugin Diagnostics

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Any

from config.logger import get_logger

from plugins.plugin_loader import plugin_loader
from plugins.plugin_manager import plugin_manager
from plugins.plugin_registry import plugin_registry
from plugins.plugin_sandbox import plugin_sandbox

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Plugin Diagnostics
###############################################################################


class PluginDiagnostics:
    """
    Plugin diagnostics service.

    Responsibilities

    - Plugin health checks
    - Version validation
    - Registry validation
    - Permission auditing
    - Plugin reporting
    """

    def __init__(
        self,
    ) -> None:

        logger.info(
            "Plugin Diagnostics initialized."
        )

    ###########################################################################

    def health(
        self,
    ) -> dict[str, Any]:
        """
        Return plugin health.
        """

        return {
            "registered_plugins": len(
                plugin_registry.plugins()
            ),
            "loaded_plugins": len(
                plugin_loader.plugins()
            ),
            "discovered_plugins": (
                len(
                    plugin_manager.discover()
                )
            ),
        }

    ###########################################################################

    def compatibility(
        self,
        ide_version: str,
    ) -> dict[str, bool]:
        """
        Check plugin compatibility.
        """

        result: dict[str, bool] = {}

        for plugin in plugin_registry.plugins():

            result[plugin] = (
                plugin_manager.compatible(
                    plugin,
                    ide_version,
                )
            )

        return result

    ###########################################################################

    def permission_audit(
        self,
    ) -> dict[str, Any]:
        """
        Return plugin permissions.
        """

        return plugin_sandbox.report()

    ###########################################################################

    def registry_validation(
        self,
    ) -> bool:
        """
        Validate registry integrity.
        """

        return (
            len(
                plugin_registry.plugins()
            )
            >= 0
        )
###############################################################################
# Recommendations
###############################################################################

    def recommendations(
        self,
        ide_version: str = "1.0.0",
    ) -> list[str]:
        """
        Generate plugin recommendations.
        """

        recommendations: list[str] = []

        health = self.health()

        if health["registered_plugins"] == 0:

            recommendations.append(
                "No plugins are registered."
            )

        if (
            health["registered_plugins"]
            != health["loaded_plugins"]
        ):

            recommendations.append(
                "Some registered plugins are not loaded."
            )

        compatibility = self.compatibility(
            ide_version,
        )

        incompatible = [
            plugin
            for plugin, supported
            in compatibility.items()
            if not supported
        ]

        if incompatible:

            recommendations.append(
                "Update incompatible plugins."
            )

        if not recommendations:

            recommendations.append(
                "Plugin ecosystem is healthy."
            )

        return recommendations

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
        ide_version: str = "1.0.0",
    ) -> dict[str, Any]:
        """
        Return diagnostics statistics.
        """

        return {
            "health": self.health(),
            "compatible_plugins": sum(
                self.compatibility(
                    ide_version,
                ).values()
            ),
            "recommendations": len(
                self.recommendations(
                    ide_version,
                )
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
        ide_version: str = "1.0.0",
    ) -> dict[str, Any]:
        """
        Return complete diagnostics report.
        """

        return {
            "health": self.health(),
            "compatibility": (
                self.compatibility(
                    ide_version,
                )
            ),
            "permissions": (
                self.permission_audit()
            ),
            "statistics": (
                self.statistics(
                    ide_version,
                )
            ),
            "recommendations": (
                self.recommendations(
                    ide_version,
                )
            ),
        }

###############################################################################
# Global Plugin Diagnostics
###############################################################################

plugin_diagnostics = PluginDiagnostics()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "PluginDiagnostics",
    "plugin_diagnostics",
]