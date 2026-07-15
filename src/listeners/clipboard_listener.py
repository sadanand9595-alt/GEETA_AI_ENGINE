"""
==============================================================================
GEETA AI Engine

File        : clipboard_listener.py
Package     : listeners
Description : Clipboard Listener

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import threading
import time

import pyperclip

from config.logger import get_logger
from core.event_bus import publish

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Clipboard Listener
###############################################################################


class ClipboardListener:
    """
    Monitors clipboard changes.
    """

    def __init__(
        self,
        interval: float = 0.5,
    ) -> None:

        self.interval = interval

        self._running = False

        self._thread: threading.Thread | None = None

        self._last_text = ""

    ###########################################################################

    @property
    def running(self) -> bool:
        """
        Return listener state.
        """

        return self._running

    ###########################################################################

    def start(self) -> None:
        """
        Start clipboard monitoring.
        """

        if self._running:
            return

        logger.info(
            "Starting Clipboard Listener..."
        )

        self._running = True

        self._thread = threading.Thread(
            target=self._monitor,
            daemon=True,
            name="ClipboardListener",
        )

        self._thread.start()

        logger.info(
            "Clipboard Listener Started."
        )

    ###########################################################################

    def stop(self) -> None:
        """
        Stop clipboard monitoring.
        """

        if not self._running:
            return

        logger.info(
            "Stopping Clipboard Listener..."
        )

        self._running = False

        if self._thread:

            self._thread.join(timeout=2)

        logger.info(
            "Clipboard Listener Stopped."
        )

    ###########################################################################

    def _monitor(self) -> None:
        """
        Monitor clipboard continuously.
        """

        while self._running:

            try:

                text = pyperclip.paste()

                if text != self._last_text:

                    self._last_text = text

                    logger.debug(
                        "Clipboard updated."
                    )

                    publish(
                        "clipboard.changed",
                        text=text,
                    )

            except Exception:

                logger.exception(
                    "Clipboard listener failed."
                )

            time.sleep(self.interval)
###############################################################################
# Clipboard Utilities
###############################################################################

    def current_text(self) -> str:
        """
        Return the current clipboard text.
        """

        try:

            return pyperclip.paste()

        except Exception:

            logger.exception(
                "Unable to read clipboard."
            )

            return ""

    ###########################################################################

    def restart(self) -> None:
        """
        Restart the clipboard listener.
        """

        logger.info(
            "Restarting Clipboard Listener..."
        )

        self.stop()

        self.start()


###############################################################################
# Context Manager
###############################################################################

    def __enter__(self):
        """
        Context manager entry.
        """

        self.start()

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ) -> None:
        """
        Context manager exit.
        """

        self.stop()


###############################################################################
# Helper Functions
###############################################################################


def start_clipboard_listener(
    interval: float = 0.5,
) -> ClipboardListener:
    """
    Create and start a clipboard listener.
    """

    listener = ClipboardListener(
        interval=interval,
    )

    listener.start()

    return listener


def stop_clipboard_listener(
    listener: ClipboardListener,
) -> None:
    """
    Stop a running clipboard listener.
    """

    listener.stop()


###############################################################################
# Exports
###############################################################################

__all__ = [
    "ClipboardListener",
    "start_clipboard_listener",
    "stop_clipboard_listener",
]