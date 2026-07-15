"""
==============================================================================
GEETA AI Engine

File        : syntax_highlighter.py
Package     : editor
Description : Syntax Highlighter

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import keyword
import re
from dataclasses import dataclass
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Highlight Token
###############################################################################


@dataclass(slots=True)
class HighlightToken:
    """
    Represents a syntax token.
    """

    token_type: str

    value: str

    line: int

    column: int

###############################################################################
# Syntax Highlighter
###############################################################################


class SyntaxHighlighter:
    """
    Syntax highlighting engine.

    Responsibilities

    - Tokenization
    - Keyword detection
    - String detection
    - Number detection
    - Comment detection
    """

    KEYWORDS = set(
        keyword.kwlist
    )

    IDENTIFIER = re.compile(
        r"[A-Za-z_][A-Za-z0-9_]*"
    )

    NUMBER = re.compile(
        r"\b\d+(\.\d+)?\b"
    )

    STRING = re.compile(
        r'(\".*?\"|\'.*?\')'
    )

    COMMENT = re.compile(
        r"#.*$"
    )

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        logger.info(
            "Syntax Highlighter initialized."
        )

###############################################################################
# Highlight
###############################################################################

    def highlight(
        self,
        text: str,
    ) -> list[HighlightToken]:
        """
        Generate syntax tokens.
        """

        tokens: list[
            HighlightToken
        ] = []

        for line_number, line in enumerate(
            text.splitlines()
        ):

            tokens.extend(
                self._tokenize_line(
                    line,
                    line_number,
                )
            )

        return tokens

###############################################################################
# Tokenize Line
###############################################################################

    def _tokenize_line(
        self,
        line: str,
        line_number: int,
    ) -> list[HighlightToken]:
        """
        Tokenize a single line.
        """

        tokens: list[
            HighlightToken
        ] = []

        for match in self.IDENTIFIER.finditer(
            line
        ):

            value = match.group()

            token_type = (
                "keyword"
                if value in self.KEYWORDS
                else "identifier"
            )

            tokens.append(
                HighlightToken(
                    token_type=token_type,
                    value=value,
                    line=line_number,
                    column=match.start(),
                )
            )

        return tokens
###############################################################################
# String Tokens
###############################################################################

    def string_tokens(
        self,
        text: str,
    ) -> list[HighlightToken]:
        """
        Return string tokens.
        """

        tokens: list[HighlightToken] = []

        for line_number, line in enumerate(
            text.splitlines()
        ):

            for match in self.STRING.finditer(
                line,
            ):

                tokens.append(
                    HighlightToken(
                        token_type="string",
                        value=match.group(),
                        line=line_number,
                        column=match.start(),
                    )
                )

        return tokens

###############################################################################
# Number Tokens
###############################################################################

    def number_tokens(
        self,
        text: str,
    ) -> list[HighlightToken]:
        """
        Return number tokens.
        """

        tokens: list[HighlightToken] = []

        for line_number, line in enumerate(
            text.splitlines()
        ):

            for match in self.NUMBER.finditer(
                line,
            ):

                tokens.append(
                    HighlightToken(
                        token_type="number",
                        value=match.group(),
                        line=line_number,
                        column=match.start(),
                    )
                )

        return tokens

###############################################################################
# Comment Tokens
###############################################################################

    def comment_tokens(
        self,
        text: str,
    ) -> list[HighlightToken]:
        """
        Return comment tokens.
        """

        tokens: list[HighlightToken] = []

        for line_number, line in enumerate(
            text.splitlines()
        ):

            match = self.COMMENT.search(
                line,
            )

            if match:

                tokens.append(
                    HighlightToken(
                        token_type="comment",
                        value=match.group(),
                        line=line_number,
                        column=match.start(),
                    )
                )

        return tokens

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
        text: str,
    ) -> dict[str, Any]:
        """
        Return highlighting statistics.
        """

        return {
            "keywords_identifiers": len(
                self.highlight(text)
            ),
            "strings": len(
                self.string_tokens(text)
            ),
            "numbers": len(
                self.number_tokens(text)
            ),
            "comments": len(
                self.comment_tokens(text)
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
        text: str,
    ) -> dict[str, Any]:
        """
        Return syntax highlighting report.
        """

        return {
            "statistics": self.statistics(
                text,
            ),
        }

###############################################################################
# Global Syntax Highlighter
###############################################################################

syntax_highlighter = SyntaxHighlighter()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "HighlightToken",
    "SyntaxHighlighter",
    "syntax_highlighter",
]