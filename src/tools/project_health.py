"""
==============================================================================
GEETA AI ENGINE

File        : project_health.py
Package     : tools
Description : Enterprise Project Health Monitor

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

###############################################################################
# Imports
###############################################################################

from dataclasses import dataclass, asdict
from typing import Any

from config.logger import get_logger

from tools.compile_recovery import (
    compile_recovery,
)

from workspace.project_analyzer import (
    project_analyzer,
)

from workspace.dependency_graph import (
    dependency_graph,
)

from workspace.symbol_indexer import (
    symbol_indexer,
)

from workspace.semantic_indexer import (
    semantic_indexer,
)

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Project Health
###############################################################################


@dataclass(slots=True)
class ProjectHealth:

    score: int

    status: str

    compiled: int

    failed: int

    files: int

    warnings: list[str]

###############################################################################
# Health Monitor
###############################################################################


class ProjectHealthMonitor:
    """
    Enterprise project health monitor.
    """

    def __init__(
        self,
    ) -> None:

        logger.info(
            "Project Health Monitor initialized."
        )
        ###############################################################################
# Score
###############################################################################

    def calculate_score(
        self,
    ) -> int:
        """
        Calculate overall project health score.
        """

        report = compile_recovery.report()

        files = report["files"]

        failed = report["failed"]

        if files == 0:

            return 0

        score = int(

            ((files - failed) / files)

            * 100

        )

        return max(
            0,
            min(
                score,
                100,
            ),
        )

###############################################################################
# Status
###############################################################################

    def health_status(
        self,
        score: int,
    ) -> str:
        """
        Return project health status.
        """

        if score >= 95:

            return "Excellent"

        if score >= 85:

            return "Healthy"

        if score >= 70:

            return "Warning"

        return "Critical"

###############################################################################
# Warnings
###############################################################################

    def collect_warnings(
        self,
    ) -> list[str]:
        """
        Collect project warnings.
        """

        warnings: list[str] = []

        report = compile_recovery.report()

        if report["failed"]:

            warnings.append(

                f"{report['failed']} compile errors detected."

            )

        try:

            if dependency_graph.has_cycle():

                warnings.append(

                    "Circular dependencies detected."

                )

        except Exception:

            logger.exception(

                "Dependency analysis failed."

            )

        return warnings
        ###############################################################################
# Build
###############################################################################

    def build(
        self,
    ) -> ProjectHealth:
        """
        Build project health information.
        """

        compile_report = (
            compile_recovery.report()
        )

        score = self.calculate_score()

        return ProjectHealth(

            score=score,

            status=self.health_status(
                score,
            ),

            compiled=compile_report[
                "compiled"
            ],

            failed=compile_report[
                "failed"
            ],

            files=compile_report[
                "files"
            ],

            warnings=self.collect_warnings(),

        )

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return complete health report.
        """

        health = self.build()

        return {

            "health": asdict(
                health,
            ),

            "project": (
                project_analyzer.statistics()
            ),

            "symbols": (
                symbol_indexer.statistics()
            ),

            "semantic": (
                semantic_indexer.statistics()
            ),

            "dependencies": (
                dependency_graph.statistics()
            ),

        }

###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, Any]:
        """
        Return diagnostics.
        """

        report = self.report()

        return {

            "engine": (
                "ProjectHealthMonitor"
            ),

            "version": "3.2.0",

            "healthy": (

                report["health"]["failed"]

                == 0

            ),

            "report": report,

        }
        ###############################################################################
# Export JSON
###############################################################################

    def export_json(
        self,
        file_path: str,
    ) -> None:
        """
        Export health report as JSON.
        """

        import json
        from pathlib import Path

        Path(file_path).write_text(

            json.dumps(

                self.report(),

                indent=4,

                ensure_ascii=False,

            ),

            encoding="utf-8",

        )

        logger.info(

            "Project health exported: %s",

            file_path,

        )

###############################################################################
# Representation
###############################################################################

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        health = self.build()

        return (

            f"ProjectHealthMonitor("

            f"score={health.score}, "

            f"status='{health.status}')"

        )

###############################################################################
# Global Instance
###############################################################################

project_health = ProjectHealthMonitor()

###############################################################################
# Exports
###############################################################################

__all__ = [

    "ProjectHealth",

    "ProjectHealthMonitor",

    "project_health",

]