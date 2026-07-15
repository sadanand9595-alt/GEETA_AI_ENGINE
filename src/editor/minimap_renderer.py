"""
GEETA AI IDE Enterprise v3.0

File:
    src/editor/minimap_renderer.py

Description:
    High-performance minimap rendering engine.

Responsibilities:
    - Generate minimap data from document text.
    - Maintain viewport mapping.
    - Convert document positions to minimap coordinates.
    - Cache rendered data.
    - Support incremental updates.
    - Remain UI-framework independent.

This module does not perform any painting itself. It produces
rendering primitives that can be consumed by Qt, GTK, Tkinter,
or any future rendering backend.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import RLock
from typing import Dict, List, Optional, Sequence


# ----------------------------------------------------------------------
# Data Models
# ----------------------------------------------------------------------


@dataclass(slots=True, frozen=True)
class MinimapPixel:
    """
    Represents one minimap pixel block.
    """

    x: int
    y: int
    width: int
    height: int
    color_role: str


@dataclass(slots=True, frozen=True)
class ViewportOverlay:
    """
    Represents visible editor viewport inside minimap.
    """

    y: int
    height: int


@dataclass(slots=True)
class LineRenderData:
    """
    Cached render information for one line.
    """

    line_number: int
    text_hash: int
    pixels: List[MinimapPixel] = field(default_factory=list)


# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------


@dataclass(slots=True)
class MinimapConfiguration:
    """
    Rendering configuration.
    """

    pixel_width: int = 2
    pixel_height: int = 2

    horizontal_spacing: int = 1
    vertical_spacing: int = 1

    max_columns: int = 240

    tab_size: int = 4

    viewport_padding: int = 2


# ----------------------------------------------------------------------
# Cache
# ----------------------------------------------------------------------


class MinimapCache:
    """
    Thread-safe cache of rendered lines.
    """

    def __init__(self) -> None:
        self._cache: Dict[int, LineRenderData] = {}
        self._lock = RLock()

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()

    def get(self, line: int) -> Optional[LineRenderData]:
        with self._lock:
            return self._cache.get(line)

    def put(self, data: LineRenderData) -> None:
        with self._lock:
            self._cache[data.line_number] = data

    def remove(self, line: int) -> None:
        with self._lock:
            self._cache.pop(line, None)

    def remove_after(self, line: int) -> None:
        with self._lock:
            for key in list(self._cache.keys()):
                if key >= line:
                    del self._cache[key]


# ----------------------------------------------------------------------
# Renderer
# ----------------------------------------------------------------------


class MinimapRenderer:
    """
    Enterprise minimap renderer.

    The renderer converts text into lightweight pixel blocks.
    No UI dependencies exist inside this class.
    """

    def __init__(
        self,
        configuration: MinimapConfiguration | None = None,
    ) -> None:

        self._config = configuration or MinimapConfiguration()

        self._cache = MinimapCache()

        self._document: List[str] = []

        self._total_height = 0

    # --------------------------------------------------------------

    @property
    def configuration(self) -> MinimapConfiguration:
        return self._config

    # --------------------------------------------------------------

    def set_document(
        self,
        lines: Sequence[str],
    ) -> None:
        """
        Replace document contents.
        """

        self._document = list(lines)

        self._cache.clear()

        self._total_height = (
            len(self._document)
            * (
                self._config.pixel_height
                + self._config.vertical_spacing
            )
        )

    # --------------------------------------------------------------

    @property
    def line_count(self) -> int:
        return len(self._document)

    # --------------------------------------------------------------

    @property
    def total_height(self) -> int:
        return self._total_height

    # --------------------------------------------------------------

    def render_document(
        self,
    ) -> List[MinimapPixel]:
        """
        Render the complete document.
        """

        pixels: List[MinimapPixel] = []

        for line_number in range(len(self._document)):
            pixels.extend(
                self.render_line(line_number)
            )

        return pixels

    # --------------------------------------------------------------

    def render_line(
        self,
        line_number: int,
    ) -> List[MinimapPixel]:
        """
        Render one document line.
        """

        if line_number < 0:
            return []

        if line_number >= len(self._document):
            return []

        text = self._document[line_number]

        text_hash = hash(text)

        cached = self._cache.get(line_number)

        if cached is not None and cached.text_hash == text_hash:
            return cached.pixels

        pixels = self._generate_pixels(
            line_number=line_number,
            text=text,
        )

        self._cache.put(
            LineRenderData(
                line_number=line_number,
                text_hash=text_hash,
                pixels=pixels,
            )
        )

        return pixels

    # --------------------------------------------------------------

    def update_line(
        self,
        line_number: int,
        text: str,
    ) -> None:
        """
        Update one line without rebuilding entire cache.
        """

        if line_number < 0:
            return

        if line_number >= len(self._document):
            return

        self._document[line_number] = text

        self._cache.remove(line_number)

    # --------------------------------------------------------------

    def insert_line(
        self,
        line_number: int,
        text: str,
    ) -> None:
        """
        Insert a document line.
        """

        self._document.insert(line_number, text)

        self._cache.remove_after(line_number)

        self._total_height = (
            len(self._document)
            * (
                self._config.pixel_height
                + self._config.vertical_spacing
            )
        )
    # --------------------------------------------------------------

    def delete_line(
        self,
        line_number: int,
    ) -> None:
        """
        Delete a document line.
        """

        if line_number < 0:
            return

        if line_number >= len(self._document):
            return

        del self._document[line_number]

        self._cache.remove_after(line_number)

        self._total_height = (
            len(self._document)
            * (
                self._config.pixel_height
                + self._config.vertical_spacing
            )
        )

    # --------------------------------------------------------------

    def viewport_overlay(
        self,
        *,
        first_visible_line: int,
        visible_line_count: int,
    ) -> ViewportOverlay:
        """
        Calculate the minimap viewport rectangle.
        """

        row_height = (
            self._config.pixel_height
            + self._config.vertical_spacing
        )

        y = max(0, first_visible_line * row_height)

        height = max(
            row_height,
            visible_line_count * row_height,
        )

        maximum = max(0, self._total_height - height)

        if y > maximum:
            y = maximum

        return ViewportOverlay(
            y=y,
            height=height,
        )

    # --------------------------------------------------------------

    def line_to_y(
        self,
        line_number: int,
    ) -> int:
        """
        Convert a document line to minimap Y coordinate.
        """

        return line_number * (
            self._config.pixel_height
            + self._config.vertical_spacing
        )

    # --------------------------------------------------------------

    def y_to_line(
        self,
        y: int,
    ) -> int:
        """
        Convert minimap Y coordinate into a document line.
        """

        row_height = (
            self._config.pixel_height
            + self._config.vertical_spacing
        )

        if row_height <= 0:
            return 0

        line = y // row_height

        if line < 0:
            return 0

        if line >= len(self._document):
            return max(0, len(self._document) - 1)

        return line

    # --------------------------------------------------------------

    def visible_lines(
        self,
        *,
        scroll_y: int,
        viewport_height: int,
    ) -> range:
        """
        Return visible minimap lines.
        """

        start = self.y_to_line(scroll_y)

        end = self.y_to_line(
            scroll_y + viewport_height
        ) + 1

        end = min(end, len(self._document))

        return range(start, end)

    # --------------------------------------------------------------

    def render_visible_region(
        self,
        *,
        scroll_y: int,
        viewport_height: int,
    ) -> List[MinimapPixel]:
        """
        Render only the currently visible minimap region.
        """

        pixels: List[MinimapPixel] = []

        for line in self.visible_lines(
            scroll_y=scroll_y,
            viewport_height=viewport_height,
        ):
            pixels.extend(
                self.render_line(line)
            )

        return pixels

    # --------------------------------------------------------------

    def invalidate(
        self,
    ) -> None:
        """
        Clear all cached rendering data.
        """

        self._cache.clear()

    # --------------------------------------------------------------

    def _generate_pixels(
        self,
        *,
        line_number: int,
        text: str,
    ) -> List[MinimapPixel]:
        """
        Convert one document line into minimap pixel blocks.
        """

        pixels: List[MinimapPixel] = []

        row_y = self.line_to_y(line_number)

        column = 0

        for character in text:

            if column >= self._config.max_columns:
                break

            if character == "\t":
                column += self._config.tab_size
                continue

            if character == " ":
                column += 1
                continue

            x = column * (
                self._config.pixel_width
                + self._config.horizontal_spacing
            )

            pixels.append(
                MinimapPixel(
                    x=x,
                    y=row_y,
                    width=self._config.pixel_width,
                    height=self._config.pixel_height,
                    color_role=self._classify_character(
                        character
                    ),
                )
            )

            column += 1

        return pixels

    # --------------------------------------------------------------

    @staticmethod
    def _classify_character(
        character: str,
    ) -> str:
        """
        Map a character to a semantic color role.
        """

        if character.isdigit():
            return "number"

        if character.isalpha():
            return "identifier"

        if character == "#":
            return "comment"

        if character in (
            "\"",
            "'",
        ):
            return "string"

        if character in "()[]{}":
            return "delimiter"

        if character in ",.;:":
            return "punctuation"

        return "operator"
