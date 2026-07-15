"""
==============================================================================
GEETA AI Engine

File        : whitespace_renderer.py
Package     : editor
Description : Whitespace Renderer

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Whitespace Symbols
###############################################################################

SPACE_SYMBOL = "·"
TAB_SYMBOL = "→"
EOL_SYMBOL = "¶"

###############################################################################
# Rendered Line
###############################################################################


@dataclass(slots=True)
class RenderedWhitespace:
    """
    Represents rendered whitespace.
    """

    original: str

    rendered: str

###############################################################################
# Whitespace Renderer
###############################################################################


class WhitespaceRenderer:
    """
    Whitespace rendering engine.

    Responsibilities

    - Visible spaces
    - Visible tabs
    - End-of-line markers
    - Trailing whitespace
    - Indentation guides
    """

    def __init__(
        self,
    ) -> None:

        self._enabled = True

        self._show_spaces = True

        self._show_tabs = True

        self._show_eol = False

        logger.info(
            "Whitespace Renderer initialized."
        )

###############################################################################
# Enable / Disable
###############################################################################

    def enable(
        self,
    ) -> None:
        """
        Enable whitespace rendering.
        """

        self._enabled = True

    ###########################################################################

    def disable(
        self,
    ) -> None:
        """
        Disable whitespace rendering.
        """

        self._enabled = False

###############################################################################
# Rendering
###############################################################################

    def render(
        self,
        line: str,
    ) -> RenderedWhitespace:
        """
        Render whitespace for a line.
        """

        if not self._enabled:

            return RenderedWhitespace(
                original=line,
                rendered=line,
            )

        rendered = line

        if self._show_spaces:

            rendered = rendered.replace(
                " ",
                SPACE_SYMBOL,
            )

        if self._show_tabs:

            rendered = rendered.replace(
                "\t",
                TAB_SYMBOL,
            )

        if self._show_eol:

            rendered += EOL_SYMBOL

        return RenderedWhitespace(
            original=line,
            rendered=rendered,
        )
###############################################################################
# Configuration
###############################################################################

    def show_spaces(
        self,
        enabled: bool,
    ) -> None:
        """
        Enable or disable visible spaces.
        """

        self._show_spaces = enabled

    ###########################################################################

    def show_tabs(
        self,
        enabled: bool,
    ) -> None:
        """
        Enable or disable visible tabs.
        """

        self._show_tabs = enabled

    ###########################################################################

    def show_end_of_line(
        self,
        enabled: bool,
    ) -> None:
        """
        Enable or disable end-of-line markers.
        """

        self._show_eol = enabled

###############################################################################
# Trailing Whitespace
###############################################################################

    def trailing_whitespace(
        self,
        line: str,
    ) -> bool:
        """
        Return True if the line ends with whitespace.
        """

        return (
            len(line) != len(line.rstrip())
        )

###############################################################################
# Indentation Guides
###############################################################################

    def indentation_level(
        self,
        line: str,
        indent_size: int = 4,
    ) -> int:
        """
        Return indentation level.
        """

        expanded = line.expandtabs(
            indent_size,
        )

        leading = len(
            expanded
        ) - len(
            expanded.lstrip(" ")
        )

        return leading // indent_size

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, object]:
        """
        Return renderer statistics.
        """

        return {
            "enabled": self._enabled,
            "show_spaces": self._show_spaces,
            "show_tabs": self._show_tabs,
            "show_eol": self._show_eol,
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return renderer report.
        """

        return {
            "statistics": self.statistics(),
            "symbols": {
                "space": SPACE_SYMBOL,
                "tab": TAB_SYMBOL,
                "eol": EOL_SYMBOL,
            },
        }

###############################################################################
# Global Renderer
###############################################################################

whitespace_renderer = WhitespaceRenderer()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "SPACE_SYMBOL",
    "TAB_SYMBOL",
    "EOL_SYMBOL",
    "RenderedWhitespace",
    "WhitespaceRenderer",
    "whitespace_renderer",
]