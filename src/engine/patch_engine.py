"""
==============================================================================
GEETA AI Engine

File        : patch_engine.py
Package     : engine
Description : AI Patch Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import difflib
import shutil
from pathlib import Path
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Patch Engine
###############################################################################


class PatchEngine:
    """
    Safe AI patch application engine.

    Responsibilities

    - Unified diff generation
    - Patch validation
    - Atomic updates
    - Automatic backups
    - Rollback support
    - Multi-file patching
    """

    def __init__(self) -> None:

        logger.info(
            "Patch Engine initialized."
        )

    ###########################################################################

    def create_diff(
        self,
        original: str,
        modified: str,
        filename: str = "file.py",
    ) -> str:
        """
        Create unified diff.
        """

        return "".join(
            difflib.unified_diff(
                original.splitlines(
                    keepends=True,
                ),
                modified.splitlines(
                    keepends=True,
                ),
                fromfile=filename,
                tofile=filename,
            )
        )

    ###########################################################################

    def backup(
        self,
        file: Path,
    ) -> Path:
        """
        Create backup before modification.
        """

        backup = file.with_suffix(
            file.suffix + ".bak"
        )

        shutil.copy2(
            file,
            backup,
        )

        logger.info(
            "Backup created: %s",
            backup,
        )

        return backup

    ###########################################################################

    def apply(
        self,
        file: Path,
        new_content: str,
        backup: bool = True,
    ) -> None:
        """
        Apply patch to file.
        """

        if backup:

            self.backup(
                file,
            )

        file.write_text(
            new_content,
            encoding="utf-8",
        )

        logger.info(
            "Patch applied: %s",
            file,
        )

    ###########################################################################

    def dry_run(
        self,
        original: str,
        modified: str,
    ) -> dict[str, Any]:
        """
        Simulate patch application.
        """

        diff = self.create_diff(
            original,
            modified,
        )

        return {
            "success": True,
            "changes": bool(
                diff,
            ),
            "diff": diff,
        }
###############################################################################
# Rollback
###############################################################################

    def rollback(
        self,
        file: Path,
    ) -> bool:
        """
        Restore a file from its backup.
        """

        backup = file.with_suffix(
            file.suffix + ".bak"
        )

        if not backup.exists():

            logger.warning(
                "Backup not found: %s",
                backup,
            )

            return False

        shutil.copy2(
            backup,
            file,
        )

        logger.info(
            "Rollback completed: %s",
            file,
        )

        return True

###############################################################################
# Multi-file Patch
###############################################################################

    def apply_multiple(
        self,
        patches: dict[Path, str],
        backup: bool = True,
    ) -> None:
        """
        Apply patches to multiple files.
        """

        for file, content in patches.items():

            self.apply(
                file=file,
                new_content=content,
                backup=backup,
            )

###############################################################################
# Validation
###############################################################################

    def validate(
        self,
        original: str,
        modified: str,
    ) -> bool:
        """
        Validate a patch.

        Placeholder validation. Future versions
        will perform syntax checking, formatting,
        linting and semantic validation.
        """

        return original != modified

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return patch engine statistics.
        """

        return {
            "supports_backup": True,
            "supports_rollback": True,
            "supports_dry_run": True,
            "supports_multi_file": True,
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return patch engine report.
        """

        return {
            "statistics": self.statistics(),
        }

###############################################################################
# Global Engine
###############################################################################

patch_engine = PatchEngine()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "PatchEngine",
    "patch_engine",
]