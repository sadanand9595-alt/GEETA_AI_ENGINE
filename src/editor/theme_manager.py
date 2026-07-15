"""
==============================================================================
GEETA AI Engine

File        : theme_manager.py
Package     : editor
Description : Theme Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Theme Manager
###############################################################################


class ThemeManager:
    """
    Theme management.

    Responsibilities

    - Theme loading
    - Theme switching
    - Color lookup
    - Font settings
    - Theme persistence
    """

    def __init__(
        self,
    ) -> None:

        self._theme: dict[
            str,
            Any,
        ] = {}

        self._theme_name = "Default"

        logger.info(
            "Theme Manager initialized."
        )

###############################################################################
# Load Theme
###############################################################################

    def load(
        self,
        file_path: str | Path,
    ) -> None:
        """
        Load a theme file.
        """

        path = Path(
            file_path
        )

        self._theme = json.loads(
            path.read_text(
                encoding="utf-8",
            )
        )

        self._theme_name = (
            self._theme.get(
                "name",
                path.stem,
            )
        )

        logger.info(
            "Loaded theme: %s",
            self._theme_name,
        )

###############################################################################
# Apply Theme
###############################################################################

    def apply(
        self,
        theme: dict[str, Any],
    ) -> None:
        """
        Apply a theme.
        """

        self._theme = dict(
            theme,
        )

        self._theme_name = (
            theme.get(
                "name",
                "Custom",
            )
        )

###############################################################################
# Color Lookup
###############################################################################

    def color(
        self,
        key: str,
        default: str = "#FFFFFF",
    ) -> str:
        """
        Return a theme color.
        """

        colors = self._theme.get(
            "colors",
            {},
        )

        return colors.get(
            key,
            default,
        )

###############################################################################
# Active Theme
###############################################################################

    @property
    def name(
        self,
    ) -> str:
        """
        Return theme name.
        """

        return self._theme_name
###############################################################################
# Font Configuration
###############################################################################

    def font(
        self,
    ) -> dict[str, Any]:
        """
        Return font configuration.
        """

        return self._theme.get(
            "font",
            {
                "family": "Consolas",
                "size": 12,
            },
        )

###############################################################################
# Validation
###############################################################################

    def validate(
        self,
    ) -> bool:
        """
        Validate current theme.
        """

        return (
            isinstance(
                self._theme,
                dict,
            )
            and "colors" in self._theme
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return theme statistics.
        """

        return {
            "theme_name": self._theme_name,
            "color_count": len(
                self._theme.get(
                    "colors",
                    {},
                )
            ),
            "valid": self.validate(),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return theme report.
        """

        return {
            "statistics": self.statistics(),
            "font": self.font(),
            "colors": self._theme.get(
                "colors",
                {},
            ),
        }

###############################################################################
# Global Theme Manager
###############################################################################

theme_manager = ThemeManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "ThemeManager",
    "theme_manager",
]