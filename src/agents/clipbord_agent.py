"""
==============================================================================
GEETA AI Engine

File        : clipboard_agent.py
Package     : agents
Description : AI Clipboard Agent

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import json
import re
from typing import Any

from agents.base_agent import BaseAgent
from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Clipboard Agent
###############################################################################


class ClipboardAgent(BaseAgent):
    """
    AI agent responsible for understanding clipboard contents.

    Supported clipboard types:

    - Source Code
    - Python Tracebacks
    - Terminal Output
    - JSON
    - SQL
    - URLs
    - Markdown
    - Plain Text
    """

    def __init__(self) -> None:

        super().__init__(
            name="clipboard_agent",
            description="AI Clipboard Assistant",
        )

    ###########################################################################

    def can_handle(
        self,
        context: dict[str, Any],
    ) -> bool:
        """
        Determine whether this agent can process
        clipboard content.
        """

        return context.get("type") == "clipboard"

    ###########################################################################

    def execute(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Analyze clipboard content.
        """

        logger.info(
            "Clipboard Agent executing..."
        )

        text = context.get(
            "text",
            "",
        )

        detected_type = self.detect_type(text)

        return {
            "agent": self.name,
            "clipboard_type": detected_type,
            "summary": self._build_summary(
                detected_type,
            ),
            "prompt": self.build_prompt(
                detected_type,
                text,
            ),
            "status": "ready",
        }

    ###########################################################################

    def detect_type(
        self,
        text: str,
    ) -> str:
        """
        Detect clipboard content type.
        """

        text = text.strip()

        if not text:

            return "empty"

        if "Traceback (most recent call last)" in text:

            return "python_traceback"

        if text.startswith("{"):

            try:

                json.loads(text)

                return "json"

            except Exception:

                pass

        if re.search(
            r"https?://",
            text,
        ):

            return "url"

        if re.search(
            r"\bSELECT\b|\bINSERT\b|\bUPDATE\b|\bDELETE\b",
            text,
            flags=re.IGNORECASE,
        ):

            return "sql"

        if "def " in text or "class " in text:

            return "python_code"

        if "#include" in text:

            return "cpp_code"

        if "<html" in text.lower():

            return "html"

        if "function " in text or "=>" in text:

            return "javascript"

        return "text"

    ###########################################################################

    def _build_summary(
        self,
        clipboard_type: str,
    ) -> str:
        """
        Build clipboard summary.
        """

        return (
            f"Clipboard contains "
            f"{clipboard_type.replace('_', ' ')}."
        )
###############################################################################
# Prompt Builder
###############################################################################

    def build_prompt(
        self,
        clipboard_type: str,
        text: str,
    ) -> str:
        """
        Build AI prompt based on clipboard content.
        """

        return f"""
You are an expert software engineering assistant.

Clipboard Content Type:
{clipboard_type}

Clipboard Content:

{text}

Tasks:

1. Identify the content.
2. Explain what it is.
3. Detect possible issues.
4. Suggest improvements.
5. Recommend the next action.
6. If it is code, review it.
7. If it is an error, debug it.
8. If it is JSON or SQL, validate it.
9. Return the result in structured Markdown.
""".strip()

###############################################################################
# Suggestions
###############################################################################

    def suggested_action(
        self,
        clipboard_type: str,
    ) -> str:
        """
        Return the recommended action.
        """

        actions = {
            "python_traceback": "debug",
            "python_code": "review",
            "cpp_code": "review",
            "javascript": "review",
            "html": "review",
            "json": "validate",
            "sql": "optimize",
            "url": "analyze",
            "text": "summarize",
            "empty": "ignore",
        }

        return actions.get(
            clipboard_type,
            "analyze",
        )

###############################################################################
# Report
###############################################################################

    def create_report(
        self,
        text: str,
    ) -> dict[str, Any]:
        """
        Build a structured clipboard analysis report.
        """

        clipboard_type = self.detect_type(text)

        return {
            "agent": self.name,
            "clipboard_type": clipboard_type,
            "recommended_action": self.suggested_action(
                clipboard_type,
            ),
            "summary": self._build_summary(
                clipboard_type,
            ),
            "prompt": self.build_prompt(
                clipboard_type,
                text,
            ),
            "text_length": len(text),
        }


###############################################################################
# Exports
###############################################################################

__all__ = [
    "ClipboardAgent",
]