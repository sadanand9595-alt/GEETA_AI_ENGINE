"""
==============================================================================
GEETA AI IDE

File        : clipboard_agent.py
Package     : integrations
Description : Enterprise Clipboard Agent

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Clipboard State
###############################################################################


class ClipboardState(str, Enum):

    STOPPED = "stopped"

    RUNNING = "running"

    PAUSED = "paused"

###############################################################################
# Clipboard Entry
###############################################################################


@dataclass(slots=True)
class ClipboardEntry:
    """
    Clipboard history entry.
    """

    text: str

    language: str = ""

    copied_at: datetime = field(
        default_factory=datetime.utcnow
    )

###############################################################################
# Clipboard Agent
###############################################################################


class ClipboardAgent:
    """
    Enterprise Clipboard Agent.

    Responsibilities

    - Clipboard monitoring
    - Clipboard history
    - Code detection
    - Language detection
    - Smart paste
    - AI context extraction
    """

    ###########################################################################

    def __init__(
        self,
        poll_interval: float = 0.5,
    ) -> None:

        self._state = (
            ClipboardState.STOPPED
        )

        self._history: list[
            ClipboardEntry
        ] = []

        self._last_text = ""

        self._poll_interval = (
            poll_interval
        )

        logger.info(
            "Clipboard Agent initialized."
        )

###############################################################################
# State
###############################################################################

    @property
    def state(
        self,
    ) -> ClipboardState:

        return self._state

###############################################################################
# Start
###############################################################################

    async def start(
        self,
    ) -> None:
        """
        Start clipboard monitoring.
        """

        self._state = (
            ClipboardState.RUNNING
        )

        logger.info(
            "Clipboard monitoring started."
        )

###############################################################################
# Stop
###############################################################################

    async def stop(
        self,
    ) -> None:
        """
        Stop clipboard monitoring.
        """

        self._state = (
            ClipboardState.STOPPED
        )

        logger.info(
            "Clipboard monitoring stopped."
        )

###############################################################################
# Pause
###############################################################################

    def pause(
        self,
    ) -> None:
        """
        Pause monitoring.
        """

        self._state = (
            ClipboardState.PAUSED
        )

###############################################################################
# Resume
###############################################################################

    def resume(
        self,
    ) -> None:
        """
        Resume monitoring.
        """

        self._state = (
            ClipboardState.RUNNING
        )

###############################################################################
# Add History
###############################################################################

    def add_history(
        self,
        text: str,
        language: str = "",
    ) -> None:
        """
        Store clipboard history.
        """

        self._history.append(
            ClipboardEntry(
                text=text,
                language=language,
            )
        )

        self._last_text = text
###############################################################################
# Clipboard Backend
###############################################################################

    def read_clipboard(
        self,
    ) -> str:
        """
        Read clipboard text.

        Platform-specific implementation will be added
        (Windows / Linux / macOS).
        """

        try:

            import pyperclip

            return pyperclip.paste()

        except Exception:

            logger.exception(
                "Clipboard read failed."
            )

            return ""

###############################################################################
# Write Clipboard
###############################################################################

    def write_clipboard(
        self,
        text: str,
    ) -> bool:
        """
        Write clipboard.
        """

        try:

            import pyperclip

            pyperclip.copy(
                text,
            )

            return True

        except Exception:

            logger.exception(
                "Clipboard write failed."
            )

            return False

###############################################################################
# Duplicate Detection
###############################################################################

    def is_duplicate(
        self,
        text: str,
    ) -> bool:
        """
        Detect duplicate clipboard content.
        """

        return (
            text == self._last_text
        )

###############################################################################
# Poll Loop
###############################################################################

    async def poll(
        self,
    ) -> None:
        """
        Clipboard monitoring loop.
        """

        while (
            self._state
            == ClipboardState.RUNNING
        ):

            try:

                text = self.read_clipboard()

                if (
                    text
                    and not self.is_duplicate(
                        text,
                    )
                ):

                    await self.on_copy(
                        text,
                    )

                await asyncio.sleep(
                    self._poll_interval,
                )

            except asyncio.CancelledError:

                raise

            except Exception:

                logger.exception(
                    "Clipboard polling failed."
                )

###############################################################################
# Copy Event
###############################################################################

    async def on_copy(
        self,
        text: str,
    ) -> None:
        """
        Clipboard copy event.
        """

        logger.info(
            "Clipboard updated."
        )

        self.add_history(
            text,
            language=self.detect_language(
                text,
            ),
        )

###############################################################################
# Paste Event
###############################################################################

    async def on_paste(
        self,
        text: str,
    ) -> None:
        """
        Clipboard paste event.
        """

        logger.info(
            "Clipboard pasted."
        )

###############################################################################
# History
###############################################################################

    @property
    def history(
        self,
    ) -> list[ClipboardEntry]:
        """
        Clipboard history.
        """

        return list(
            self._history
        )
###############################################################################
# Detect Programming Language
###############################################################################

    def detect_language(
        self,
        text: str,
    ) -> str:
        """
        Detect programming language.
        """

        source = text.lower()

        if (
            "def "
            in source
            or "import "
            in source
        ):
            return "python"

        if (
            "public class"
            in source
            or "system.out"
            in source
        ):
            return "java"

        if (
            "#include"
            in source
        ):
            return "cpp"

        if (
            "function "
            in source
            or "const "
            in source
            or "let "
            in source
        ):
            return "javascript"

        if (
            "<html"
            in source
        ):
            return "html"

        if (
            "body {"
            in source
        ):
            return "css"

        return "text"

###############################################################################
# Smart Paste
###############################################################################

    async def smart_paste(
        self,
        text: str,
    ) -> str:
        """
        Prepare clipboard text before paste.
        """

        return text.rstrip()

###############################################################################
# AI Context
###############################################################################

    def extract_context(
        self,
        text: str,
    ) -> dict[str, object]:
        """
        Build AI context.
        """

        return {
            "language": self.detect_language(
                text,
            ),
            "characters": len(text),
            "lines": len(
                text.splitlines()
            ),
            "is_code": (
                self.detect_language(text)
                != "text"
            ),
        }

###############################################################################
# Search History
###############################################################################

    def search(
        self,
        keyword: str,
    ) -> list[ClipboardEntry]:
        """
        Search clipboard history.
        """

        keyword = keyword.lower()

        return [
            entry
            for entry
            in self._history
            if keyword
            in entry.text.lower()
        ]

###############################################################################
# Clear History
###############################################################################

    def clear_history(
        self,
    ) -> None:
        """
        Clear clipboard history.
        """

        self._history.clear()

###############################################################################
# Security Filter
###############################################################################

    def contains_sensitive_data(
        self,
        text: str,
    ) -> bool:
        """
        Detect sensitive information.
        """

        patterns = [

            "password",

            "secret",

            "api_key",

            "private_key",

            "access_token",

            "authorization",

            "bearer ",
        ]

        source = text.lower()

        return any(
            token in source
            for token in patterns
        )

###############################################################################
# Safe Clipboard
###############################################################################

    def safe_content(
        self,
        text: str,
    ) -> bool:
        """
        Validate clipboard before AI processing.
        """

        return (
            not self.contains_sensitive_data(
                text,
            )
        )
###############################################################################
# Maximum History
###############################################################################

    def trim_history(
        self,
        maximum: int = 100,
    ) -> None:
        """
        Keep only the newest history entries.
        """

        if len(self._history) <= maximum:

            return

        self._history = self._history[-maximum:]

###############################################################################
# Cleanup
###############################################################################

    def cleanup(
        self,
        maximum: int = 100,
    ) -> None:
        """
        Cleanup clipboard history.
        """

        self.trim_history(
            maximum,
        )

        logger.info(
            "Clipboard history cleaned."
        )

###############################################################################
# Export History
###############################################################################

    def export_history(
        self,
    ) -> list[dict[str, str]]:
        """
        Export clipboard history.
        """

        return [
            {
                "text": entry.text,
                "language": entry.language,
                "copied_at": entry.copied_at.isoformat(),
            }
            for entry
            in self._history
        ]

###############################################################################
# Import History
###############################################################################

    def import_history(
        self,
        entries: list[dict[str, str]],
    ) -> None:
        """
        Import clipboard history.
        """

        for item in entries:

            self._history.append(
                ClipboardEntry(
                    text=item.get(
                        "text",
                        "",
                    ),
                    language=item.get(
                        "language",
                        "",
                    ),
                )
            )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Clipboard statistics.
        """

        return {
            "entries": len(
                self._history
            ),
            "python": sum(
                1
                for entry
                in self._history
                if entry.language == "python"
            ),
            "javascript": sum(
                1
                for entry
                in self._history
                if entry.language == "javascript"
            ),
            "text": sum(
                1
                for entry
                in self._history
                if entry.language == "text"
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Clipboard Agent report.
        """

        return {
            "state": self._state.value,
            "statistics": self.statistics(),
        }

###############################################################################
# Global Clipboard Agent
###############################################################################

clipboard_agent: (
    ClipboardAgent | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "ClipboardState",
    "ClipboardEntry",
    "ClipboardAgent",
    "clipboard_agent",
]