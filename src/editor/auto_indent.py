"""
==============================================================================
GEETA AI Engine

File        : auto_indent.py
Package     : editor
Description : Auto Indentation Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Auto Indent
###############################################################################


class AutoIndent:
    """
    Smart indentation engine.

    Responsibilities

    - Smart indentation
    - Tab/Space handling
    - Block indentation
    - Outdent
    - Language aware indentation
    """

    def __init__(
        self,
        indent_size: int = 4,
        use_spaces: bool = True,
    ) -> None:

        self._indent_size = indent_size

        self._use_spaces = use_spaces

        logger.info(
            "Auto Indent initialized."
        )

###############################################################################
# Properties
###############################################################################

    @property
    def indent_string(
        self,
    ) -> str:
        """
        Return indentation string.
        """

        if self._use_spaces:

            return " " * self._indent_size

        return "\t"

###############################################################################
# Current Indent
###############################################################################

    def indentation(
        self,
        line: str,
    ) -> str:
        """
        Return indentation prefix.
        """

        result = ""

        for character in line:

            if character in (" ", "\t"):

                result += character

            else:

                break

        return result

###############################################################################
# Auto Indent
###############################################################################

    def indent_after_enter(
        self,
        previous_line: str,
    ) -> str:
        """
        Calculate indentation after pressing Enter.
        """

        indent = self.indentation(
            previous_line,
        )

        stripped = previous_line.rstrip()

        if stripped.endswith(
            (
                "{",
                "(",
                "[",
                ":",
            )
        ):

            indent += self.indent_string

        return indent

###############################################################################
# Indent Line
###############################################################################

    def indent_line(
        self,
        line: str,
    ) -> str:
        """
        Indent a line.
        """

        return (
            self.indent_string
            + line
        )
###############################################################################
# Outdent Line
###############################################################################

    def outdent_line(
        self,
        line: str,
    ) -> str:
        """
        Remove one indentation level.
        """

        if self._use_spaces:

            if line.startswith(
                self.indent_string,
            ):

                return line[
                    self._indent_size:
                ]

        else:

            if line.startswith("\t"):

                return line[1:]

        return line

###############################################################################
# Tab / Space Conversion
###############################################################################

    def tabs_to_spaces(
        self,
        text: str,
    ) -> str:
        """
        Convert tabs to spaces.
        """

        return text.replace(
            "\t",
            " " * self._indent_size,
        )

    ###########################################################################

    def spaces_to_tabs(
        self,
        text: str,
    ) -> str:
        """
        Convert spaces to tabs.
        """

        return text.replace(
            " " * self._indent_size,
            "\t",
        )

###############################################################################
# Block Indentation
###############################################################################

    def indent_block(
        self,
        lines: list[str],
    ) -> list[str]:
        """
        Indent a block of lines.
        """

        return [
            self.indent_line(line)
            for line in lines
        ]

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, object]:
        """
        Return indentation settings.
        """

        return {
            "indent_size": self._indent_size,
            "use_spaces": self._use_spaces,
            "indent_string": self.indent_string,
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return indentation report.
        """

        return {
            "statistics": self.statistics(),
        }

###############################################################################
# Global Auto Indent
###############################################################################

auto_indent = AutoIndent()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "AutoIndent",
    "auto_indent",
]