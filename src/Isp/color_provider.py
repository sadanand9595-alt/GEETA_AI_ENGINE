"""
==============================================================================
GEETA AI IDE

File        : color_provider.py
Package     : lsp
Description : LSP Color Provider

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from config.logger import get_logger
from lsp.lsp_client import LSPClient

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Color Information
###############################################################################


@dataclass(slots=True)
class DocumentColor:
    """
    Represents a document color.
    """

    red: float

    green: float

    blue: float

    alpha: float

    start_line: int

    start_character: int

    end_line: int

    end_character: int

###############################################################################
# Color Presentation
###############################################################################


@dataclass(slots=True)
class ColorPresentation:
    """
    Represents an LSP color presentation.
    """

    label: str

    text: str = ""

###############################################################################
# Color Provider
###############################################################################


class ColorProvider:
    """
    Enterprise Color Provider.

    Responsibilities

    - Document colors
    - Color presentation
    - Inline color preview
    - Color picker
    - Theme integration
    """

    ###########################################################################

    def __init__(
        self,
        client: LSPClient,
    ) -> None:

        self._client = client

        self._color_cache: dict[
            str,
            list[DocumentColor],
        ] = {}

        self._presentation_cache: dict[
            str,
            list[ColorPresentation],
        ] = {}

        logger.info(
            "Color Provider initialized."
        )

###############################################################################
# Document Colors
###############################################################################

    def request_document_colors(
        self,
        uri: str,
    ) -> int:
        """
        Request document colors.
        """

        return self._client.send_request(
            "textDocument/documentColor",
            {
                "textDocument": {
                    "uri": uri,
                },
            },
        )

###############################################################################
# Color Presentation
###############################################################################

    def request_color_presentation(
        self,
        uri: str,
        color: DocumentColor,
    ) -> int:
        """
        Request color presentation.
        """

        return self._client.send_request(
            "textDocument/colorPresentation",
            {
                "textDocument": {
                    "uri": uri,
                },
                "color": {
                    "red": color.red,
                    "green": color.green,
                    "blue": color.blue,
                    "alpha": color.alpha,
                },
                "range": {
                    "start": {
                        "line": color.start_line,
                        "character": color.start_character,
                    },
                    "end": {
                        "line": color.end_line,
                        "character": color.end_character,
                    },
                },
            },
        )

###############################################################################
# Cache
###############################################################################

    def cache_colors(
        self,
        uri: str,
        colors: list[
            DocumentColor
        ],
    ) -> None:
        """
        Cache document colors.
        """

        self._color_cache[
            uri
        ] = colors

    ###########################################################################

    def cache_presentations(
        self,
        uri: str,
        presentations: list[
            ColorPresentation
        ],
    ) -> None:
        """
        Cache color presentations.
        """

        self._presentation_cache[
            uri
        ] = presentations

###############################################################################
# Lookup
###############################################################################

    def colors(
        self,
        uri: str,
    ) -> list[DocumentColor]:
        """
        Return cached document colors.
        """

        return list(
            self._color_cache.get(
                uri,
                [],
            )
        )

    ###########################################################################

    def presentations(
        self,
        uri: str,
    ) -> list[ColorPresentation]:
        """
        Return cached presentations.
        """

        return list(
            self._presentation_cache.get(
                uri,
                [],
            )
        )
###############################################################################
# Color Lookup
###############################################################################

    def color_at(
        self,
        uri: str,
        line: int,
        character: int,
    ) -> DocumentColor | None:
        """
        Return the color at the specified position.
        """

        for color in self.colors(
            uri,
        ):

            if (
                color.start_line
                <= line
                <= color.end_line
                and color.start_character
                <= character
                <= color.end_character
            ):

                return color

        return None

###############################################################################
# Color Conversion
###############################################################################

    @staticmethod
    def to_hex(
        color: DocumentColor,
    ) -> str:
        """
        Convert RGBA color to hexadecimal.
        """

        red = int(color.red * 255)
        green = int(color.green * 255)
        blue = int(color.blue * 255)

        return (
            f"#{red:02X}"
            f"{green:02X}"
            f"{blue:02X}"
        )

    ###########################################################################

    @staticmethod
    def to_rgb(
        color: DocumentColor,
    ) -> tuple[int, int, int]:
        """
        Convert color to RGB tuple.
        """

        return (
            int(color.red * 255),
            int(color.green * 255),
            int(color.blue * 255),
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return color provider statistics.
        """

        return {
            "cached_documents": len(
                self._color_cache
            ),
            "cached_colors": sum(
                len(colors)
                for colors
                in self._color_cache.values()
            ),
            "cached_presentations": sum(
                len(items)
                for items
                in self._presentation_cache.values()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return provider report.
        """

        return {
            "statistics": self.statistics(),
            "documents": {
                uri: len(colors)
                for uri, colors
                in self._color_cache.items()
            },
        }

###############################################################################
# Global Provider
###############################################################################

color_provider: (
    ColorProvider | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "DocumentColor",
    "ColorPresentation",
    "ColorProvider",
    "color_provider",
]