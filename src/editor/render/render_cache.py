"""
==============================================================================
GEETA AI ENGINE

File        : render_cache.py
Package     : editor.render
Description : Rendering Cache

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from threading import RLock
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Render Cache
###############################################################################


class RenderCache:
    """
    Enterprise rendering cache.

    Responsibilities
    ----------------
    • Glyph cache
    • Line cache
    • Layout cache
    • Syntax cache
    • Pixmap cache

    This class significantly reduces rendering
    overhead during scrolling and repaint.
    """

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._lock = RLock()

        self._glyph_cache: dict[Any, Any] = {}

        self._line_cache: dict[int, Any] = {}

        self._layout_cache: dict[int, Any] = {}

        self._syntax_cache: dict[int, Any] = {}

        self._pixmap_cache: dict[Any, Any] = {}

        logger.info(
            "Render Cache initialized.",
        )

###############################################################################
# Glyph Cache
###############################################################################

    def cache_glyph(
        self,
        key: Any,
        glyph: Any,
    ) -> None:
        """
        Store a glyph.
        """

        with self._lock:

            self._glyph_cache[key] = glyph

    ###########################################################################

    def glyph(
        self,
        key: Any,
    ) -> Any | None:
        """
        Return cached glyph.
        """

        return self._glyph_cache.get(
            key,
        )

###############################################################################
# Line Cache
###############################################################################

    def cache_line(
        self,
        line: int,
        value: Any,
    ) -> None:
        """
        Cache rendered line information.
        """

        with self._lock:

            self._line_cache[line] = value

    ###########################################################################

    def line(
        self,
        line: int,
    ) -> Any | None:
        """
        Return cached line.
        """

        return self._line_cache.get(
            line,
        )

###############################################################################
# Layout Cache
###############################################################################

    def cache_layout(
        self,
        line: int,
        layout: Any,
    ) -> None:
        """
        Cache text layout.
        """

        with self._lock:

            self._layout_cache[line] = layout
            ###############################################################################
# Layout Cache
###############################################################################

    def layout(
        self,
        line: int,
    ) -> Any | None:
        """
        Return cached layout.
        """

        return self._layout_cache.get(
            line,
        )

###############################################################################
# Syntax Cache
###############################################################################

    def cache_syntax(
        self,
        line: int,
        tokens: Any,
    ) -> None:
        """
        Cache syntax highlighting tokens.
        """

        with self._lock:

            self._syntax_cache[line] = tokens

    ###########################################################################

    def syntax(
        self,
        line: int,
    ) -> Any | None:
        """
        Return cached syntax tokens.
        """

        return self._syntax_cache.get(
            line,
        )

###############################################################################
# Pixmap Cache
###############################################################################

    def cache_pixmap(
        self,
        key: Any,
        pixmap: Any,
    ) -> None:
        """
        Cache a rendered pixmap.
        """

        with self._lock:

            self._pixmap_cache[key] = pixmap

    ###########################################################################

    def pixmap(
        self,
        key: Any,
    ) -> Any | None:
        """
        Return cached pixmap.
        """

        return self._pixmap_cache.get(
            key,
        )

###############################################################################
# Cache Invalidation
###############################################################################

    def invalidate_line(
        self,
        line: int,
    ) -> None:
        """
        Invalidate all cached information for a line.
        """

        with self._lock:

            self._line_cache.pop(
                line,
                None,
            )

            self._layout_cache.pop(
                line,
                None,
            )

            self._syntax_cache.pop(
                line,
                None,
            )

###############################################################################
# Cache Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return cache statistics.
        """

        return {
            "glyphs": len(
                self._glyph_cache,
            ),
            "lines": len(
                self._line_cache,
            ),
            "layouts": len(
                self._layout_cache,
            ),
            "syntax": len(
                self._syntax_cache,
            ),
            "pixmaps": len(
                self._pixmap_cache,
            ),
        }
        ###############################################################################
# Cache Lifecycle
###############################################################################

    def clear(
        self,
    ) -> None:
        """
        Clear all render caches.
        """

        with self._lock:

            self._glyph_cache.clear()

            self._line_cache.clear()

            self._layout_cache.clear()

            self._syntax_cache.clear()

            self._pixmap_cache.clear()

        logger.info(
            "Render cache cleared.",
        )

###############################################################################
# Cache Reset
###############################################################################

    def reset(
        self,
    ) -> None:
        """
        Reset the render cache.
        """

        self.clear()

        logger.info(
            "Render cache reset.",
        )

###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return cache diagnostics.
        """

        stats = self.statistics()

        return {
            **stats,
            "total_entries": sum(
                stats.values(),
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

        stats = self.statistics()

        return (
            f"{self.__class__.__name__}("
            f"glyphs={stats['glyphs']}, "
            f"lines={stats['lines']}, "
            f"layouts={stats['layouts']}, "
            f"syntax={stats['syntax']}, "
            f"pixmaps={stats['pixmaps']})"
        )

###############################################################################
# Exports
###############################################################################

__all__ = [
    "RenderCache",
]