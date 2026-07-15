"""
==============================================================================
GEETA AI Engine

File        : plugin_sandbox.py
Package     : plugins
Description : Plugin Sandbox

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Plugin Permissions
###############################################################################


@dataclass(slots=True)
class PluginPermissions:
    """
    Plugin permission model.
    """

    filesystem: bool = False

    network: bool = False

    subprocess: bool = False

    runtime: bool = True

    git: bool = False

    workspace: bool = True

###############################################################################
# Plugin Sandbox
###############################################################################


class PluginSandbox:
    """
    Secure plugin execution environment.

    Responsibilities

    - Permission validation
    - Filesystem protection
    - Network policy
    - API access validation
    - Audit logging
    - Security enforcement
    """

    def __init__(self) -> None:

        self._permissions: dict[
            str,
            PluginPermissions,
        ] = {}

        logger.info(
            "Plugin Sandbox initialized."
        )

    ###########################################################################

    def register(
        self,
        plugin: str,
        permissions: PluginPermissions,
    ) -> None:
        """
        Register plugin permissions.
        """

        self._permissions[
            plugin
        ] = permissions

    ###########################################################################

    def permissions(
        self,
        plugin: str,
    ) -> PluginPermissions | None:
        """
        Return plugin permissions.
        """

        return self._permissions.get(
            plugin,
        )

    ###########################################################################

    def allowed(
        self,
        plugin: str,
        permission: str,
    ) -> bool:
        """
        Check whether a permission is granted.
        """

        permissions = self.permissions(
            plugin,
        )

        if permissions is None:

            return False

        return bool(
            getattr(
                permissions,
                permission,
                False,
            )
        )

    ###########################################################################

    def validate_path(
        self,
        plugin: str,
        path: str | Path,
    ) -> bool:
        """
        Validate filesystem access.
        """

        if not self.allowed(
            plugin,
            "filesystem",
        ):

            return False

        return Path(path).exists()
###############################################################################
# Network Validation
###############################################################################

    def validate_network(
        self,
        plugin: str,
    ) -> bool:
        """
        Validate network access.
        """

        return self.allowed(
            plugin,
            "network",
        )

###############################################################################
# Audit Logging
###############################################################################

    def audit(
        self,
        plugin: str,
        action: str,
    ) -> None:
        """
        Record a sandbox audit event.
        """

        logger.info(
            "[Sandbox] %s -> %s",
            plugin,
            action,
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return sandbox statistics.
        """

        filesystem = sum(
            permissions.filesystem
            for permissions
            in self._permissions.values()
        )

        network = sum(
            permissions.network
            for permissions
            in self._permissions.values()
        )

        subprocesses = sum(
            permissions.subprocess
            for permissions
            in self._permissions.values()
        )

        return {
            "registered_plugins": len(
                self._permissions
            ),
            "filesystem_access": filesystem,
            "network_access": network,
            "subprocess_access": subprocesses,
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return sandbox report.
        """

        return {
            "statistics": self.statistics(),
            "plugins": {
                name: {
                    "filesystem": permissions.filesystem,
                    "network": permissions.network,
                    "subprocess": permissions.subprocess,
                    "runtime": permissions.runtime,
                    "git": permissions.git,
                    "workspace": permissions.workspace,
                }
                for name, permissions
                in self._permissions.items()
            },
        }

###############################################################################
# Global Plugin Sandbox
###############################################################################

plugin_sandbox = PluginSandbox()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "PluginPermissions",
    "PluginSandbox",
    "plugin_sandbox",
]