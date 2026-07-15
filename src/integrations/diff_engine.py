"""
==============================================================================
GEETA AI ENGINE

File        : diff_engine.py
Package     : integrations
Description : Enterprise AI Diff Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

###############################################################################
# Imports
###############################################################################

import difflib

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any
from uuid import uuid4

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Diff Status
###############################################################################


class DiffStatus(str, Enum):
    """
    Diff engine status.
    """

    IDLE = "idle"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


###############################################################################
# Diff Type
###############################################################################


class DiffType(str, Enum):
    """
    Supported diff formats.
    """

    UNIFIED = "unified"
    INLINE = "inline"
    GIT = "git"
    ###############################################################################
# Diff Request
###############################################################################


@dataclass(slots=True)
class DiffRequest:
    """
    Diff generation request.
    """

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    file_path: str = ""

    original: str = ""

    modified: str = ""

    diff_type: DiffType = (
        DiffType.UNIFIED
    )


###############################################################################
# Diff Result
###############################################################################


@dataclass(slots=True)
class DiffResult:
    """
    Diff generation result.
    """

    success: bool = False

    diff: str = ""

    additions: int = 0

    deletions: int = 0

    generated_at: datetime = field(
        default_factory=datetime.utcnow
    )


###############################################################################
# Diff Engine
###############################################################################


class DiffEngine:
    """
    Enterprise AI Diff Engine.

    Responsibilities

    - Unified diff generation
    - Inline diff generation
    - Git patch generation
    - Three-way merge
    - Patch export
    - Statistics
    - History management
    """

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._status = (
            DiffStatus.IDLE
        )

        self._history: list[
            DiffResult
        ] = []

        logger.info(
            "Diff Engine initialized."
        )

###############################################################################
# Status
###############################################################################

    @property
    def status(
        self,
    ) -> DiffStatus:
        """
        Return current engine status.
        """

        return self._status
        ###############################################################################
# Generate Diff
###############################################################################

    def generate(
        self,
        request: DiffRequest,
    ) -> DiffResult:
        """
        Generate unified diff.
        """

        self._status = (
            DiffStatus.GENERATING
        )

        diff = "".join(

            difflib.unified_diff(

                request.original.splitlines(
                    keepends=True,
                ),

                request.modified.splitlines(
                    keepends=True,
                ),

                fromfile=request.file_path,

                tofile=request.file_path,
            )
        )

        additions = sum(

            1

            for line in diff.splitlines()

            if line.startswith("+")
            and not line.startswith("+++")
        )

        deletions = sum(

            1

            for line in diff.splitlines()

            if line.startswith("-")
            and not line.startswith("---")
        )

        result = DiffResult(

            success=True,

            diff=diff,

            additions=additions,

            deletions=deletions,
        )

        self._history.append(
            result,
        )

        self._status = (
            DiffStatus.COMPLETED
        )

        return result

###############################################################################
# History
###############################################################################

    def history(
        self,
    ) -> list[DiffResult]:
        """
        Return diff history.
        """

        return list(
            self._history,
        )

###############################################################################
# Clear History
###############################################################################

    def clear_history(
        self,
    ) -> None:
        """
        Clear diff history.
        """

        self._history.clear()

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return engine statistics.
        """

        return {

            "status": self._status.value,

            "history": len(
                self._history,
            ),

        }
        ###############################################################################
# Three-Way Merge
###############################################################################

    def three_way_merge(
        self,
        base: str,
        local: str,
        remote: str,
    ) -> str:
        """
        Perform a simple three-way merge.
        """

        if local == remote:

            return local

        if base == local:

            return remote

        if base == remote:

            return local

        return (
            "<<<<<<< LOCAL\n"
            f"{local}\n"
            "=======\n"
            f"{remote}\n"
            ">>>>>>> REMOTE\n"
        )

###############################################################################
# Normalize
###############################################################################

    def normalize(
        self,
        text: str,
    ) -> str:
        """
        Normalize whitespace.
        """

        return "\n".join(

            line.rstrip()

            for line
            in text.splitlines()

        )

###############################################################################
# Optimized Diff
###############################################################################

    def optimized_diff(
        self,
        original: str,
        modified: str,
    ) -> str:
        """
        Generate whitespace-aware diff.
        """

        original = self.normalize(
            original,
        )

        modified = self.normalize(
            modified,
        )

        return "".join(

            difflib.unified_diff(

                original.splitlines(
                    keepends=True,
                ),

                modified.splitlines(
                    keepends=True,
                ),
            )

        )

###############################################################################
# Git Patch
###############################################################################

    def git_patch(
        self,
        request: DiffRequest,
    ) -> str:
        """
        Generate Git-compatible patch.
        """

        return "".join(

            difflib.unified_diff(

                request.original.splitlines(
                    keepends=True,
                ),

                request.modified.splitlines(
                    keepends=True,
                ),

                fromfile=f"a/{request.file_path}",

                tofile=f"b/{request.file_path}",
            )

        )
        ###############################################################################
# Review Notes
###############################################################################

    def review_notes(
        self,
        result: DiffResult,
    ) -> list[str]:
        """
        Generate AI review notes.
        """

        notes: list[str] = []

        if result.additions:

            notes.append(
                f"{result.additions} line(s) added."
            )

        if result.deletions:

            notes.append(
                f"{result.deletions} line(s) removed."
            )

        if (
            result.additions == 0
            and result.deletions == 0
        ):

            notes.append(
                "No functional changes detected."
            )

        return notes

###############################################################################
# Metadata
###############################################################################

    def metadata(
        self,
        request: DiffRequest,
        result: DiffResult,
    ) -> dict[str, Any]:
        """
        Generate diff metadata.
        """

        return {

            "id": request.id,

            "file": request.file_path,

            "type": request.diff_type.value,

            "generated": (
                result.generated_at.isoformat()
            ),

            "additions": result.additions,

            "deletions": result.deletions,

            "risk": self.risk_score(
                result,
            ),

        }

###############################################################################
# Serialize
###############################################################################

    def serialize(
        self,
        result: DiffResult,
    ) -> dict[str, Any]:
        """
        Serialize diff result.
        """

        return {

            "success": result.success,

            "diff": result.diff,

            "additions": result.additions,

            "deletions": result.deletions,

            "generated_at": (
                result.generated_at.isoformat()
            ),

        }

###############################################################################
# Risk Score
###############################################################################

    def risk_score(
        self,
        result: DiffResult,
    ) -> float:
        """
        Estimate modification risk.
        """

        changes = (
            result.additions
            + result.deletions
        )

        return min(
            1.0,
            changes / 500.0,
        )

###############################################################################
# Export Patch
###############################################################################

    def export_patch(
        self,
        result: DiffResult,
        path: str | Path,
    ) -> Path:
        """
        Export patch to disk.
        """

        output = Path(path)

        output.write_text(

            result.diff,

            encoding="utf-8",

        )

        logger.info(

            "Patch exported: %s",

            output,

        )

        return output
        ###############################################################################
# Global Instance
###############################################################################

diff_engine = DiffEngine()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "DiffStatus",
    "DiffType",
    "DiffRequest",
    "DiffResult",
    "DiffEngine",
    "diff_engine",
]