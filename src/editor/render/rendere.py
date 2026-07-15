"""
==============================================================================
GEETA AI ENGINE

File        : renderer.py
Package     : editor.render
Description : Rendering Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from threading import RLock
from typing import TYPE_CHECKING

from config.logger import get_logger

if TYPE_CHECKING:
    from PySide6.QtGui import QPainter

    from editor.core.editor_session import EditorSession
    from editor.render.render_context import RenderContext

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Render Layer
###############################################################################


class RenderLayer(ABC):
    """
    Base class for every rendering layer.

    Examples
    --------
    - Text
    - Caret
    - Selection
    - Current Line
    - Line Numbers
    - Diagnostics
    - AI Ghost Text
    """

    @abstractmethod
    def paint(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Paint the layer.
        """

###############################################################################
# Renderer
###############################################################################


class Renderer:
    """
    Central rendering engine.

    Responsibilities
    ----------------
    • Manage render layers
    • Execute paint pipeline
    • Coordinate rendering order
    """

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._lock = RLock()

        self._layers: list[RenderLayer] = []

        logger.info(
            "Renderer initialized.",
        )

###############################################################################
# Layer Management
###############################################################################

    def add_layer(
        self,
        layer: RenderLayer,
    ) -> None:
        """
        Register a render layer.
        """

        with self._lock:

            if layer not in self._layers:

                self._layers.append(
                    layer,
                )

                logger.debug(
                    "Layer added: %s",
                    layer.__class__.__name__,
                )

    ###########################################################################

    def remove_layer(
        self,
        layer: RenderLayer,
    ) -> None:
        """
        Remove a render layer.
        """

        with self._lock:

            if layer in self._layers:

                self._layers.remove(
                    layer,
                )

                logger.debug(
                    "Layer removed: %s",
                    layer.__class__.__name__,
                )
                ###############################################################################
# Rendering
###############################################################################

    def paint(
        self,
        painter: QPainter,
        context: RenderContext,
        session: EditorSession,
    ) -> None:
        """
        Execute the complete rendering pipeline.
        """

        with self._lock:

            for layer in self._layers:

                try:

                    layer.paint(
                        painter,
                        context,
                        session,
                    )

                except Exception:

                    logger.exception(
                        "Render layer failed: %s",
                        layer.__class__.__name__,
                    )

###############################################################################
# Queries
###############################################################################

    def layer_count(
        self,
    ) -> int:
        """
        Return the number of registered layers.
        """

        return len(
            self._layers,
        )

    ###########################################################################

    def layers(
        self,
    ) -> list[RenderLayer]:
        """
        Return a copy of registered layers.
        """

        return self._layers.copy()

###############################################################################
# Ordering
###############################################################################

    def clear_layers(
        self,
    ) -> None:
        """
        Remove all registered layers.
        """

        with self._lock:

            self._layers.clear()

            logger.info(
                "Render layers cleared.",
            )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return renderer statistics.
        """

        return {
            "layer_count": len(
                self._layers,
            ),
        }

###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, object]:
        """
        Return renderer diagnostics.
        """

        return {
            **self.statistics(),
            "initialized": True,
        }
        ###############################################################################
# Lifecycle
###############################################################################

    def reset(
        self,
    ) -> None:
        """
        Reset the renderer.
        """

        with self._lock:

            self._layers.clear()

        logger.info(
            "Renderer reset.",
        )

###############################################################################
# Render Order
###############################################################################

    def sort_layers(
        self,
    ) -> None:
        """
        Sort render layers by priority.

        Lower priority values are painted first.
        """

        with self._lock:

            self._layers.sort(
                key=lambda layer: getattr(
                    layer,
                    "priority",
                    100,
                ),
            )

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
            f"{self.__class__.__name__}"
            f"(layers={self.layer_count()})"
        )

###############################################################################
# Exports
###############################################################################

__all__ = [
    "RenderLayer",
    "Renderer",
]