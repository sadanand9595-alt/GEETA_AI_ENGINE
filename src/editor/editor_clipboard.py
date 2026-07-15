"""
==============================================================================
GEETA AI Engine

File        : editor_clipboard.py
Package     : editor
Description : Editor Clipboard Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Clipboard Item
###############################################################################


@dataclass(slots=True)
class ClipboardItem:
    """
    Represents a clipboard entry.
    """

    text: str

    mime_type: str = "text/plain"

###############################################################################
# Editor Clipboard
###############################################################################


class EditorClipboard:
    """
    Enterprise clipboard manager.

    Responsibilities

    - Copy
    - Cut
    - Paste
    - Clipboard history
    - Clipboard ring
    - Duplicate line
    """

    def __init__(
        self,
        history_size: int = 100,
    ) -> None:

        self._history: deque[
            ClipboardItem
        ] = deque(
            maxlen=history_size,
        )

        logger.info(
            "Editor Clipboard initialized."
        )

###############################################################################
# Copy
###############################################################################

    def copy(
        self,
        text: str,
    ) -> None:
        """
        Copy text.
        """

        self._history.appendleft(
            ClipboardItem(
                text=text,
            )
        )

###############################################################################
# Cut
###############################################################################

    def cut(
        self,
        text: str,
    ) -> str:
        """
        Cut text.
        """

        self.copy(
            text,
        )

        return ""

###############################################################################
# Paste
###############################################################################

    def paste(
        self,
    ) -> str:
        """
        Return latest clipboard text.
        """

        if not self._history:

            return ""

        return self._history[
            0
        ].text

###############################################################################
# History
###############################################################################

    def history(
        self,
    ) -> list[ClipboardItem]:
        """
        Return clipboard history.
        """

        return list(
            self._history
        )
"""
==============================================================================
GEETA AI Engine

File        : editor_clipboard.py
Package     : editor
Description : Editor Clipboard Manager

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
# Clipboard Item
###############################################################################


@dataclass(slots=True)
class ClipboardItem:
    """
    Represents a clipboard entry.
    """

    text: str

    mime_type: str = "text/plain"

###############################################################################
# Editor Clipboard
###############################################################################


class EditorClipboard:
    """
    Enterprise clipboard manager.

    Responsibilities

    - Copy
    - Cut
    - Paste
    - Clipboard history
    - Clipboard ring
    - Duplicate line
    """

    def __init__(
        self,
        history_size: int = 100,
    ) -> None:

        self._history: deque[
            ClipboardItem
        ] = deque(
            maxlen=history_size,
        )

        logger.info(
            "Editor Clipboard initialized."
        )

###############################################################################
# Copy
###############################################################################

    def copy(
        self,
        text: str,
    ) -> None:
        """
        Copy text.
        """

        self._history.appendleft(
            ClipboardItem(
                text=text,
            )
        )

###############################################################################
# Cut
###############################################################################

    def cut(
        self,
        text: str,
    ) -> str:
        """
        Cut text.
        """

        self.copy(
            text,
        )

        return ""

###############################################################################
# Paste
###############################################################################

    def paste(
        self,
    ) -> str:
        """
        Return latest clipboard text.
        """

        if not self._history:

            return ""

        return self._history[
            0
        ].text

###############################################################################
# History
###############################################################################

    def history(
        self,
    ) -> list[ClipboardItem]:
        """
        Return clipboard history.
        """

        return list(
            self._history
        )