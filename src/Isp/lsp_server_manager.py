"""
==============================================================================
GEETA AI IDE

File        : lsp_server_manager.py
Package     : lsp
Description : Language Server Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from pathlib import Path

from config.logger import get_logger
from lsp.lsp_client import LSPClient

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# LSP Server Manager
###############################################################################


class LSPServerManager:
    """
    Enterprise Language Server Manager.

    Responsibilities

    - Multiple language servers
    - Workspace management
    - Auto discovery
    - Server lifecycle
    - Restart on crash
    """

    ###########################################################################

    DEFAULT_SERVERS = {
        "python": ["pyright-langserver", "--stdio"],
        "typescript": ["typescript-language-server", "--stdio"],
        "javascript": ["typescript-language-server", "--stdio"],
        "cpp": ["clangd"],
        "c": ["clangd"],
        "rust": ["rust-analyzer"],
        "go": ["gopls"],
        "java": ["jdtls"],
    }

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._servers: dict[
            str,
            LSPClient,
        ] = {}

        logger.info(
            "LSP Server Manager initialized."
        )

###############################################################################
# Register
###############################################################################

    def register(
        self,
        language: str,
        command: list[str],
    ) -> None:
        """
        Register a language server.
        """

        self.DEFAULT_SERVERS[
            language
        ] = command

###############################################################################
# Create
###############################################################################

    def create(
        self,
        language: str,
    ) -> LSPClient:
        """
        Create LSP client.
        """

        if language not in self.DEFAULT_SERVERS:

            raise ValueError(
                f"No language server registered for '{language}'."
            )

        client = LSPClient(
            self.DEFAULT_SERVERS[
                language
            ]
        )

        self._servers[
            language
        ] = client

        return client

###############################################################################
# Lookup
###############################################################################

    def client(
        self,
        language: str,
    ) -> LSPClient | None:
        """
        Return language client.
        """

        return self._servers.get(
            language,
        )

###############################################################################
# Workspace
###############################################################################

    def start_workspace(
        self,
        language: str,
        workspace: str | Path,
    ) -> LSPClient:
        """
        Start language server.
        """

        client = self.client(
            language,
        )

        if client is None:

            client = self.create(
                language,
            )

        client.start()

        client.initialize(
            Path(
                workspace
            ).resolve().as_uri()
        )

        return client
###############################################################################
# Stop Server
###############################################################################

    def stop(
        self,
        language: str,
    ) -> bool:
        """
        Stop a language server.
        """

        client = self._servers.get(
            language,
        )

        if client is None:

            return False

        try:

            client.shutdown()

        except Exception:

            logger.exception(
                "Shutdown request failed."
            )

        try:

            client.exit()

        except Exception:

            logger.exception(
                "Exit notification failed."
            )

        client.stop()

        del self._servers[
            language
        ]

        return True

###############################################################################
# Restart Server
###############################################################################

    def restart(
        self,
        language: str,
        workspace: str | Path,
    ) -> LSPClient:
        """
        Restart a language server.
        """

        self.stop(
            language,
        )

        return self.start_workspace(
            language,
            workspace,
        )

###############################################################################
# Shutdown All
###############################################################################

    def shutdown_all(
        self,
    ) -> None:
        """
        Shutdown all running language servers.
        """

        for language in list(
            self._servers.keys()
        ):

            self.stop(
                language,
            )

###############################################################################
# Running Servers
###############################################################################

    def running_servers(
        self,
    ) -> list[str]:
        """
        Return running language servers.
        """

        return sorted(
            self._servers.keys()
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, object]:
        """
        Return server statistics.
        """

        return {
            "registered_servers": len(
                self.DEFAULT_SERVERS
            ),
            "running_servers": len(
                self._servers
            ),
            "languages": self.running_servers(),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return manager report.
        """

        return {
            "statistics": self.statistics(),
            "servers": {
                language: {
                    "running": True,
                }
                for language
                in self.running_servers()
            },
        }

###############################################################################
# Global Manager
###############################################################################

lsp_server_manager = LSPServerManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "LSPServerManager",
    "lsp_server_manager",
]