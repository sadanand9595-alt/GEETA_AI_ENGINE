"""
==============================================================================
GEETA AI Engine

File        : debug_agent.py
Package     : agents
Description : AI Debug Agent

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Any

from agents.base_agent import BaseAgent
from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Debug Agent
###############################################################################


class DebugAgent(BaseAgent):
    """
    AI agent responsible for analyzing:

    - Python Tracebacks
    - Runtime Errors
    - Exceptions
    - Logs
    - Stack Traces
    """

    def __init__(self) -> None:

        super().__init__(
            name="debug_agent",
            description="AI Debug Assistant",
        )

    ###########################################################################

    def can_handle(
        self,
        context: dict[str, Any],
    ) -> bool:
        """
        Determine whether this agent can
        process the supplied context.
        """

        return context.get("type") in {
            "traceback",
            "exception",
            "error",
            "debug",
            "log",
        }

    ###########################################################################

    def execute(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Analyze debugging information.
        """

        logger.info(
            "Debug Agent executing..."
        )

        return {
            "agent": self.name,
            "summary": self._build_summary(
                context
            ),
            "context": self._extract_context(
                context
            ),
            "status": "ready",
        }

    ###########################################################################

    def _build_summary(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Build a short error summary.
        """

        error = context.get(
            "error",
            "Unknown Error",
        )

        message = context.get(
            "message",
            "",
        )

        return f"{error}: {message}"

    ###########################################################################

    def _extract_context(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Extract relevant debugging fields.
        """

        return {
            "file": context.get("file"),
            "line": context.get("line"),
            "traceback": context.get(
                "traceback"
            ),
            "log": context.get("log"),
            "working_directory": context.get(
                "workspace"
            ),
        }
###############################################################################
# Severity Detection
###############################################################################

    def detect_severity(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Determine error severity.
        """

        error = str(
            context.get("error", "")
        ).lower()

        if any(
            keyword in error
            for keyword in (
                "syntax",
                "import",
                "memory",
                "recursion",
            )
        ):
            return "critical"

        if any(
            keyword in error
            for keyword in (
                "type",
                "value",
                "attribute",
                "key",
                "index",
            )
        ):
            return "high"

        return "normal"

###############################################################################
# AI Prompt
###############################################################################

    def build_prompt(
        self,
        context: dict[str, Any],
    ) -> str:
        """
        Build a structured debugging prompt.
        """

        return f"""
You are an expert Python debugging assistant.

File:
{context.get("file")}

Line:
{context.get("line")}

Error:
{context.get("error")}

Message:
{context.get("message")}

Traceback:
{context.get("traceback")}

Tasks:

1. Explain the root cause.
2. Identify the exact failing code.
3. Suggest the best fix.
4. Explain why the fix works.
5. Produce corrected code only where necessary.
""".strip()

###############################################################################
# Report
###############################################################################

    def create_report(
        self,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Build a structured debug report.
        """

        return {
            "agent": self.name,
            "severity": self.detect_severity(
                context,
            ),
            "summary": self._build_summary(
                context,
            ),
            "prompt": self.build_prompt(
                context,
            ),
            "context": self._extract_context(
                context,
            ),
        }


###############################################################################
# Exports
###############################################################################

__all__ = [
    "DebugAgent",
]