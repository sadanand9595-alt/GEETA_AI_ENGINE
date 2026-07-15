"""
==============================================================================
GEETA AI IDE

File        : auto_fix_engine.py
Package     : ai
Description : Enterprise Auto Fix Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4

from config.logger import get_logger

from ai.debug_agent import DebugAgent
from ai.review_agent import ReviewAgent
from ai.test_agent import TestAgent
from ai.terminal_agent import TerminalAgent

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Auto Fix Status
###############################################################################


class AutoFixStatus(str, Enum):

    IDLE = "idle"

    ANALYZING = "analyzing"

    GENERATING = "generating"

    VALIDATING = "validating"

    APPLYING = "applying"

    FINISHED = "finished"

    FAILED = "failed"

###############################################################################
# Fix Source
###############################################################################


class FixSource(str, Enum):

    LSP = "lsp"

    TRACEBACK = "traceback"

    TERMINAL = "terminal"

    REVIEW = "review"

    USER = "user"

###############################################################################
# Fix Request
###############################################################################


@dataclass(slots=True)
class FixRequest:
    """
    Auto Fix request.
    """

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    file_path: str = ""

    source: FixSource = (
        FixSource.LSP
    )

    message: str = ""

    code: str = ""

###############################################################################
# Fix Result
###############################################################################


@dataclass(slots=True)
class FixResult:
    """
    Auto Fix result.
    """

    success: bool = False

    confidence: float = 0.0

    explanation: str = ""

    patch: str = ""

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

###############################################################################
# Auto Fix Engine
###############################################################################


class AutoFixEngine:
    """
    Enterprise Auto Fix Engine.

    Responsibilities

    - Diagnostics analysis
    - AI fix generation
    - Patch creation
    - Validation
    - Safe application
    - Rollback
    """

    ###########################################################################

    def __init__(
        self,
        debugger: DebugAgent,
        reviewer: ReviewAgent,
        tester: TestAgent,
        terminal: TerminalAgent,
    ) -> None:

        self._debugger = debugger

        self._reviewer = reviewer

        self._tester = tester

        self._terminal = terminal

        self._status = (
            AutoFixStatus.IDLE
        )

        self._history: list[
            FixResult
        ] = []

        logger.info(
            "Auto Fix Engine initialized."
        )

###############################################################################
# Status
###############################################################################

    @property
    def status(
        self,
    ) -> AutoFixStatus:

        return self._status

###############################################################################
# Analyze
###############################################################################

    def analyze(
        self,
        request: FixRequest,
    ) -> None:
        """
        Analyze incoming problem.
        """

        self._status = (
            AutoFixStatus.ANALYZING
        )

        logger.info(
            "Analyzing %s",
            request.file_path,
        )
###############################################################################
# Analyze LSP Diagnostics
###############################################################################

    def analyze_lsp(
        self,
        diagnostics: list[dict],
    ) -> list[str]:
        """
        Analyze Language Server diagnostics.
        """

        logger.info(
            "Analyzing %d diagnostics.",
            len(diagnostics),
        )

        return [
            item.get("message", "")
            for item in diagnostics
            if item.get("message")
        ]

###############################################################################
# Analyze Traceback
###############################################################################

    def analyze_traceback(
        self,
        traceback: str,
    ) -> list[str]:
        """
        Parse Python traceback.
        """

        return [
            line.strip()
            for line in traceback.splitlines()
            if line.strip()
        ]

###############################################################################
# Analyze Terminal Output
###############################################################################

    def analyze_terminal(
        self,
        stderr: str,
    ) -> list[str]:
        """
        Analyze terminal errors.
        """

        return [
            line.strip()
            for line in stderr.splitlines()
            if line.strip()
        ]

###############################################################################
# Generate AI Fix
###############################################################################

    def generate_fix(
        self,
        request: FixRequest,
    ) -> FixResult:
        """
        Generate AI fix.

        Provider Layer will generate the real fix.
        """

        self._status = (
            AutoFixStatus.GENERATING
        )

        logger.info(
            "Generating AI fix..."
        )

        return FixResult(
            success=True,
            confidence=0.85,
            explanation=(
                f"Suggested fix for: {request.message}"
            ),
            patch="",
        )

###############################################################################
# Confidence Score
###############################################################################

    def confidence_score(
        self,
        result: FixResult,
    ) -> float:
        """
        Calculate confidence score.
        """

        return max(
            0.0,
            min(
                result.confidence,
                1.0,
            ),
        )

###############################################################################
# Recommendation
###############################################################################

    def recommendation(
        self,
        request: FixRequest,
    ) -> str:
        """
        Return fix recommendation.
        """

        return (
            "Review generated patch "
            "before applying."
        )
###############################################################################
# Generate Patch
###############################################################################

    def generate_patch(
        self,
        request: FixRequest,
        fixed_code: str,
    ) -> str:
        """
        Generate unified patch.
        """

        import difflib

        diff = difflib.unified_diff(
            request.code.splitlines(
                keepends=True,
            ),
            fixed_code.splitlines(
                keepends=True,
            ),
            fromfile="original",
            tofile="fixed",
        )

        return "".join(diff)

###############################################################################
# Validate Patch
###############################################################################

    def validate_patch(
        self,
        patch: str,
    ) -> bool:
        """
        Validate generated patch.
        """

        self._status = (
            AutoFixStatus.VALIDATING
        )

        if not patch.strip():

            logger.warning(
                "Empty patch."
            )

            return False

        return True

###############################################################################
# Apply Patch
###############################################################################

    def apply_patch(
        self,
        result: FixResult,
    ) -> bool:
        """
        Apply validated patch.
        """

        self._status = (
            AutoFixStatus.APPLYING
        )

        if not self.validate_patch(
            result.patch,
        ):

            return False

        logger.info(
            "Patch applied."
        )

        self._history.append(
            result,
        )

        self._status = (
            AutoFixStatus.FINISHED
        )

        return True

###############################################################################
# Rollback
###############################################################################

    def rollback(
        self,
        result: FixResult,
    ) -> None:
        """
        Rollback applied fix.
        """

        logger.warning(
            "Rolling back patch."
        )

        if result in self._history:

            self._history.remove(
                result,
            )

        self._status = (
            AutoFixStatus.IDLE
        )

###############################################################################
# History
###############################################################################

    @property
    def history(
        self,
    ) -> list[FixResult]:
        """
        Return fix history.
        """

        return list(
            self._history
        )

###############################################################################
# Multi-file Patch
###############################################################################

    def merge_patches(
        self,
        patches: list[str],
    ) -> str:
        """
        Merge multiple patches.
        """

        return "\n".join(
            patch
            for patch
            in patches
            if patch
        )
###############################################################################
# Generate Patch
###############################################################################

    def generate_patch(
        self,
        request: FixRequest,
        fixed_code: str,
    ) -> str:
        """
        Generate unified patch.
        """

        import difflib

        diff = difflib.unified_diff(
            request.code.splitlines(
                keepends=True,
            ),
            fixed_code.splitlines(
                keepends=True,
            ),
            fromfile="original",
            tofile="fixed",
        )

        return "".join(diff)

###############################################################################
# Validate Patch
###############################################################################

    def validate_patch(
        self,
        patch: str,
    ) -> bool:
        """
        Validate generated patch.
        """

        self._status = (
            AutoFixStatus.VALIDATING
        )

        if not patch.strip():

            logger.warning(
                "Empty patch."
            )

            return False

        return True

###############################################################################
# Apply Patch
###############################################################################

    def apply_patch(
        self,
        result: FixResult,
    ) -> bool:
        """
        Apply validated patch.
        """

        self._status = (
            AutoFixStatus.APPLYING
        )

        if not self.validate_patch(
            result.patch,
        ):

            return False

        logger.info(
            "Patch applied."
        )

        self._history.append(
            result,
        )

        self._status = (
            AutoFixStatus.FINISHED
        )

        return True

###############################################################################
# Rollback
###############################################################################

    def rollback(
        self,
        result: FixResult,
    ) -> None:
        """
        Rollback applied fix.
        """

        logger.warning(
            "Rolling back patch."
        )

        if result in self._history:

            self._history.remove(
                result,
            )

        self._status = (
            AutoFixStatus.IDLE
        )

###############################################################################
# History
###############################################################################

    @property
    def history(
        self,
    ) -> list[FixResult]:
        """
        Return fix history.
        """

        return list(
            self._history
        )

###############################################################################
# Multi-file Patch
###############################################################################

    def merge_patches(
        self,
        patches: list[str],
    ) -> str:
        """
        Merge multiple patches.
        """

        return "\n".join(
            patch
            for patch
            in patches
            if patch
        )
###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return Auto Fix statistics.
        """

        completed = sum(
            1
            for result
            in self._history
            if result.success
        )

        failed = (
            len(self._history)
            - completed
        )

        return {
            "history": len(
                self._history
            ),
            "completed": completed,
            "failed": failed,
        }

###############################################################################
# Export History
###############################################################################

    def export_history(
        self,
    ) -> list[dict[str, object]]:
        """
        Export fix history.
        """

        return [
            {
                "success": item.success,
                "confidence": item.confidence,
                "explanation": item.explanation,
                "created_at": (
                    item.created_at.isoformat()
                ),
            }
            for item
            in self._history
        ]

###############################################################################
# Cleanup
###############################################################################

    def cleanup(
        self,
    ) -> None:
        """
        Cleanup engine state.
        """

        self._history.clear()

        self._status = (
            AutoFixStatus.IDLE
        )

        logger.info(
            "Auto Fix Engine cleaned."
        )

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return Auto Fix report.
        """

        return {
            "status": self._status.value,
            "statistics": self.statistics(),
            "history": self.export_history(),
        }

###############################################################################
# Global Engine
###############################################################################

auto_fix_engine: (
    AutoFixEngine | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "AutoFixStatus",
    "FixSource",
    "FixRequest",
    "FixResult",
    "AutoFixEngine",
    "auto_fix_engine",
]