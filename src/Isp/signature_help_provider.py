"""
==============================================================================
GEETA AI IDE

File        : signature_help_provider.py
Package     : lsp
Description : LSP Signature Help Provider

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from config.logger import get_logger
from lsp.lsp_client import LSPClient

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Signature Information
###############################################################################


@dataclass(slots=True)
class SignatureInformation:
    """
    Represents a function signature.
    """

    label: str

    documentation: str = ""

    parameters: list[str] = field(
        default_factory=list,
    )

###############################################################################
# Signature Help
###############################################################################


@dataclass(slots=True)
class SignatureHelp:
    """
    Represents signature help.
    """

    signatures: list[
        SignatureInformation
    ] = field(
        default_factory=list,
    )

    active_signature: int = 0

    active_parameter: int = 0

###############################################################################
# Signature Help Provider
###############################################################################


class SignatureHelpProvider:
    """
    LSP Signature Help Provider.

    Responsibilities

    - Parameter hints
    - Overload resolution
    - Signature cache
    - Active parameter
    - AI explanations
    """

    ###########################################################################

    def __init__(
        self,
        client: LSPClient,
    ) -> None:

        self._client = client

        self._cache: dict[
            tuple[str, int, int],
            SignatureHelp,
        ] = {}

        logger.info(
            "Signature Help Provider initialized."
        )

###############################################################################
# Request
###############################################################################

    def request(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> int:
        """
        Send signature help request.
        """

        return self._client.send_request(
            "textDocument/signatureHelp",
            {
                "textDocument": {
                    "uri": uri,
                },
                "position": {
                    "line": line,
                    "character": character,
                },
            },
        )

###############################################################################
# Cache
###############################################################################

    def cache(
        self,
        uri: str,
        line: int,
        character: int,
        help_result: SignatureHelp,
    ) -> None:
        """
        Cache signature help.
        """

        self._cache[
            (
                uri,
                line,
                character,
            )
        ] = help_result

###############################################################################
# Lookup
###############################################################################

    def cached(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> SignatureHelp | None:
        """
        Return cached signature help.
        """

        return self._cache.get(
            (
                uri,
                line,
                character,
            )
        )

###############################################################################
# Clear Cache
###############################################################################

    def clear_cache(
        self,
    ) -> None:
        """
        Clear signature help cache.
        """

        self._cache.clear()
###############################################################################
# Active Signature
###############################################################################

    def active_signature(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> SignatureInformation | None:
        """
        Return the active signature.
        """

        help_result = self.cached(
            uri,
            line,
            character,
        )

        if (
            help_result is None
            or not help_result.signatures
        ):

            return None

        index = min(
            help_result.active_signature,
            len(help_result.signatures) - 1,
        )

        return help_result.signatures[
            index
        ]

###############################################################################
# Active Parameter
###############################################################################

    def active_parameter(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> str | None:
        """
        Return the active parameter.
        """

        signature = self.active_signature(
            uri,
            line,
            character,
        )

        if (
            signature is None
            or not signature.parameters
        ):

            return None

        help_result = self.cached(
            uri,
            line,
            character,
        )

        assert help_result is not None

        index = min(
            help_result.active_parameter,
            len(signature.parameters) - 1,
        )

        return signature.parameters[
            index
        ]

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return provider statistics.
        """

        return {
            "cached_requests": len(
                self._cache
            ),
            "cached_signatures": sum(
                len(item.signatures)
                for item
                in self._cache.values()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return signature help report.
        """

        return {
            "statistics": self.statistics(),
            "cached": [
                {
                    "uri": key[0],
                    "line": key[1],
                    "character": key[2],
                    "signatures": len(
                        value.signatures
                    ),
                }
                for key, value
                in self._cache.items()
            ],
        }

###############################################################################
# Global Signature Help Provider
###############################################################################

signature_help_provider: SignatureHelpProvider | None = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "SignatureInformation",
    "SignatureHelp",
    "SignatureHelpProvider",
    "signature_help_provider",
]