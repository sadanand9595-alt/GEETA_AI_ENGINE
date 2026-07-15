"""
==============================================================================
GEETA AI ENGINE

File        : editor_theme.py
Package     : editor.theme
Description : Enterprise Editor Theme Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field

from PySide6.QtGui import QColor

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Theme Colors
###############################################################################


@dataclass(slots=True)
class ThemeColors:
    """
    Complete editor color palette.
    """

    background: QColor = field(
        default_factory=lambda: QColor(30, 30, 30)
    )

    foreground: QColor = field(
        default_factory=lambda: QColor(220, 220, 220)
    )

    caret: QColor = field(
        default_factory=lambda: QColor(255, 255, 255)
    )

    selection: QColor = field(
        default_factory=lambda: QColor(38, 79, 120)
    )

    current_line: QColor = field(
        default_factory=lambda: QColor(40, 40, 40)
    )

    gutter: QColor = field(
        default_factory=lambda: QColor(34, 34, 34)
    )

    minimap: QColor = field(
        default_factory=lambda: QColor(42, 42, 42)
    )

    whitespace: QColor = field(
        default_factory=lambda: QColor(120, 120, 120, 140)
    )

    search_match: QColor = field(
        default_factory=lambda: QColor(255, 235, 59, 140)
    )

    active_search: QColor = field(
        default_factory=lambda: QColor(255, 152, 0, 180)
    )

    ghost_text: QColor = field(
        default_factory=lambda: QColor(150, 150, 150, 170)
    )

###############################################################################
# Theme
###############################################################################


class EditorTheme:
    """
    Enterprise editor theme.
    """

    def __init__(
        self,
        name: str = "GEETA Dark",
    ) -> None:

        self.name = name

        self.colors = ThemeColors()

        logger.info(
            "EditorTheme loaded: %s",
            name,
        )
        ###############################################################################
# Syntax Colors
###############################################################################


@dataclass(slots=True)
class SyntaxColors:
    """
    Syntax highlighting palette.
    """

    keyword: QColor = field(
        default_factory=lambda: QColor(86, 156, 214)
    )

    string: QColor = field(
        default_factory=lambda: QColor(214, 157, 133)
    )

    number: QColor = field(
        default_factory=lambda: QColor(181, 206, 168)
    )

    comment: QColor = field(
        default_factory=lambda: QColor(106, 153, 85)
    )

    function: QColor = field(
        default_factory=lambda: QColor(220, 220, 170)
    )

    class_name: QColor = field(
        default_factory=lambda: QColor(78, 201, 176)
    )

    decorator: QColor = field(
        default_factory=lambda: QColor(199, 146, 234)
    )

    operator: QColor = field(
        default_factory=lambda: QColor(212, 212, 212)
    )

###############################################################################
# Diagnostic Colors
###############################################################################


@dataclass(slots=True)
class DiagnosticColors:
    """
    Diagnostic rendering colors.
    """

    error: QColor = field(
        default_factory=lambda: QColor(244, 71, 71)
    )

    warning: QColor = field(
        default_factory=lambda: QColor(255, 193, 7)
    )

    information: QColor = field(
        default_factory=lambda: QColor(66, 165, 245)
    )

    hint: QColor = field(
        default_factory=lambda: QColor(120, 120, 120)
    )

###############################################################################
# Git Colors
###############################################################################


@dataclass(slots=True)
class GitColors:
    """
    Git decorations.
    """

    added: QColor = field(
        default_factory=lambda: QColor(46, 204, 113)
    )

    modified: QColor = field(
        default_factory=lambda: QColor(241, 196, 15)
    )

    deleted: QColor = field(
        default_factory=lambda: QColor(231, 76, 60)
    )

###############################################################################
# AI Colors
###############################################################################


@dataclass(slots=True)
class AIColors:
    """
    AI rendering colors.
    """

    ghost_text: QColor = field(
        default_factory=lambda: QColor(150, 150, 150, 170)
    )

    inline_completion: QColor = field(
        default_factory=lambda: QColor(180, 180, 180)
    )

    provider_badge: QColor = field(
        default_factory=lambda: QColor(55, 120, 240)
    )

###############################################################################
# Theme Initialization
###############################################################################

        self.syntax = SyntaxColors()

        self.diagnostics = DiagnosticColors()

        self.git = GitColors()

        self.ai = AIColors()

###############################################################################
# Theme Loader
###############################################################################

    @classmethod
    def from_name(
        cls,
        name: str,
    ) -> "EditorTheme":
        """
        Create a built-in theme.
        """

        theme = cls(name)

        if name.lower() == "light":

            theme.colors.background = QColor(
                255,
                255,
                255,
            )

            theme.colors.foreground = QColor(
                40,
                40,
                40,
            )

        return theme
        ###############################################################################
# Imports
###############################################################################

import json
from pathlib import Path

###############################################################################
# Serialization
###############################################################################

    def to_dict(
        self,
    ) -> dict[str, object]:
        """
        Serialize theme.
        """

        return {
            "name": self.name,

            "colors": {
                key: value.name()
                for key, value in vars(self.colors).items()
            },

            "syntax": {
                key: value.name()
                for key, value in vars(self.syntax).items()
            },

            "diagnostics": {
                key: value.name()
                for key, value in vars(self.diagnostics).items()
            },

            "git": {
                key: value.name()
                for key, value in vars(self.git).items()
            },

            "ai": {
                key: value.name()
                for key, value in vars(self.ai).items()
            },
        }

###############################################################################
# Save Theme
###############################################################################

    def save(
        self,
        path: str | Path,
    ) -> None:
        """
        Save theme to JSON.
        """

        file_path = Path(path)

        file_path.write_text(

            json.dumps(

                self.to_dict(),

                indent=4,

            ),

            encoding="utf-8",

        )

###############################################################################
# Load Theme
###############################################################################

    @classmethod
    def load(
        cls,
        path: str | Path,
    ) -> "EditorTheme":
        """
        Load theme from JSON.
        """

        data = json.loads(

            Path(path).read_text(

                encoding="utf-8",

            )

        )

        theme = cls(

            data.get(

                "name",

                "Custom Theme",

            )

        )

        #######################################################################
        # Colors
        #######################################################################

        for key, value in data.get(
            "colors",
            {},
        ).items():

            if hasattr(
                theme.colors,
                key,
            ):

                setattr(

                    theme.colors,

                    key,

                    QColor(value),

                )

        #######################################################################
        # Syntax
        #######################################################################

        for key, value in data.get(
            "syntax",
            {},
        ).items():

            if hasattr(
                theme.syntax,
                key,
            ):

                setattr(

                    theme.syntax,

                    key,

                    QColor(value),

                )

        #######################################################################
        # Diagnostics
        #######################################################################

        for key, value in data.get(
            "diagnostics",
            {},
        ).items():

            if hasattr(
                theme.diagnostics,
                key,
            ):

                setattr(

                    theme.diagnostics,

                    key,

                    QColor(value),

                )

        #######################################################################
        # Git
        #######################################################################

        for key, value in data.get(
            "git",
            {},
        ).items():

            if hasattr(
                theme.git,
                key,
            ):

                setattr(

                    theme.git,

                    key,

                    QColor(value),

                )

        #######################################################################
        # AI
        #######################################################################

        for key, value in data.get(
            "ai",
            {},
        ).items():

            if hasattr(
                theme.ai,
                key,
            ):

                setattr(

                    theme.ai,

                    key,

                    QColor(value),

                )

        return theme

###############################################################################
# Registry
###############################################################################

_THEME_REGISTRY: dict[str, EditorTheme] = {}


def register_theme(
    theme: EditorTheme,
) -> None:
    """
    Register a theme.
    """

    _THEME_REGISTRY[
        theme.name.lower()
    ] = theme


def get_theme(
    name: str,
) -> EditorTheme:
    """
    Retrieve registered theme.
    """

    return _THEME_REGISTRY[name.lower()]
    ###############################################################################
# Theme Validation
###############################################################################

    def validate(
        self,
    ) -> bool:
        """
        Validate theme integrity.
        """

        groups = (
            self.colors,
            self.syntax,
            self.diagnostics,
            self.git,
            self.ai,
        )

        for group in groups:

            for value in vars(group).values():

                if not isinstance(
                    value,
                    QColor,
                ):

                    return False

        return True

###############################################################################
# Live Theme Switching
###############################################################################

    def apply(
        self,
        editor,
    ) -> None:
        """
        Apply theme to the editor.

        Future:
            Notify all renderers automatically.
        """

        if hasattr(
            editor,
            "set_theme",
        ):

            editor.set_theme(
                self,
            )

        logger.info(
            "Theme applied: %s",
            self.name,
        )

###############################################################################
# High Contrast Theme
###############################################################################

    @classmethod
    def high_contrast(
        cls,
    ) -> "EditorTheme":
        """
        Create a high-contrast accessibility theme.
        """

        theme = cls(
            "GEETA High Contrast",
        )

        theme.colors.background = QColor(
            0,
            0,
            0,
        )

        theme.colors.foreground = QColor(
            255,
            255,
            255,
        )

        theme.colors.selection = QColor(
            255,
            255,
            0,
        )

        theme.colors.current_line = QColor(
            35,
            35,
            35,
        )

        return theme

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, object]:
        """
        Return theme statistics.
        """

        return {

            "name": self.name,

            "valid": self.validate(),

            "registered": (
                self.name.lower()
                in _THEME_REGISTRY
            ),

        }

###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return theme diagnostics.
        """

        return {

            **self.statistics(),

            "syntax_roles": len(
                vars(self.syntax)
            ),

            "diagnostic_roles": len(
                vars(self.diagnostics)
            ),

            "git_roles": len(
                vars(self.git)
            ),

            "ai_roles": len(
                vars(self.ai)
            ),

        }

###############################################################################
# Representation
###############################################################################

    def __repr__(
        self,
    ) -> str:
        """
        Developer-friendly representation.
        """

        return (

            f"{self.__class__.__name__}("

            f"name='{self.name}')"

        )

###############################################################################
# Exports
###############################################################################

__all__ = [

    "ThemeColors",

    "SyntaxColors",

    "DiagnosticColors",

    "GitColors",

    "AIColors",

    "EditorTheme",

    "register_theme",

    "get_theme",

]