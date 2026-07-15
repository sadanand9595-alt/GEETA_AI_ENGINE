"""
==============================================================================
GEETA AI Engine

File        : runtime_diagnostics.py
Package     : runtime
Description : Runtime Diagnostics

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Any

from config.logger import get_logger

from runtime.environment_manager import environment_manager
from runtime.execution_engine import execution_engine
from runtime.profiler import runtime_profiler
from runtime.runtime_manager import runtime_manager
from runtime.runtime_monitor import runtime_monitor

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Runtime Diagnostics
###############################################################################


class RuntimeDiagnostics:
    """
    Runtime diagnostics service.

    Responsibilities

    - Runtime health
    - Environment validation
    - Dependency verification
    - Performance diagnostics
    - Resource diagnostics
    - AI-ready summaries
    """

    def __init__(self) -> None:

        logger.info(
            "Runtime Diagnostics initialized."
        )

    ###########################################################################

    def health_check(
        self,
    ) -> dict[str, Any]:
        """
        Perform runtime health checks.
        """

        return {
            "runtime": (
                runtime_manager.statistics()
            ),
            "environment": (
                environment_manager.statistics()
            ),
            "monitor": (
                runtime_monitor.statistics()
            ),
            "profiler": (
                runtime_profiler.statistics()
            ),
        }

    ###########################################################################

    def validate_environment(
        self,
    ) -> dict[str, Any]:
        """
        Validate runtime environment.
        """

        return {
            "python": (
                environment_manager.python_interpreter()
            ),
            "virtual_environment": (
                environment_manager.virtual_environment()
                is not None
            ),
            "environment_variables": (
                environment_manager.statistics()[
                    "environment_variables"
                ]
            ),
        }

    ###########################################################################

    def performance_summary(
        self,
    ) -> dict[str, Any]:
        """
        Return performance summary.
        """

        return {
            "monitor": (
                runtime_monitor.latest_metrics()
            ),
            "profiler": (
                runtime_profiler.statistics()
            ),
        }

    ###########################################################################

    def execution_summary(
        self,
    ) -> dict[str, Any]:
        """
        Return execution summary.
        """

        return execution_engine.statistics()
###############################################################################
# Recommendations
###############################################################################

    def recommendations(
        self,
    ) -> list[str]:
        """
        Generate runtime recommendations.
        """

        recommendations: list[str] = []

        monitor = runtime_monitor.statistics()

        if not monitor["running"]:

            recommendations.append(
                "Start Runtime Monitor."
            )

        if (
            not environment_manager.virtual_environment()
        ):

            recommendations.append(
                "Use a Python virtual environment."
            )

        alerts = runtime_monitor.alerts()

        recommendations.extend(
            alerts,
        )

        if not recommendations:

            recommendations.append(
                "Runtime environment is healthy."
            )

        return recommendations

###############################################################################
# Diagnostics Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return diagnostics statistics.
        """

        return {
            "health_checks": 4,
            "recommendations": len(
                self.recommendations()
            ),
            "monitor_running": (
                runtime_monitor.statistics()[
                    "running"
                ]
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return complete diagnostics report.
        """

        return {
            "health": self.health_check(),
            "environment": (
                self.validate_environment()
            ),
            "performance": (
                self.performance_summary()
            ),
            "execution": (
                self.execution_summary()
            ),
            "recommendations": (
                self.recommendations()
            ),
            "statistics": (
                self.statistics()
            ),
        }

###############################################################################
# Global Diagnostics
###############################################################################

runtime_diagnostics = RuntimeDiagnostics()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "RuntimeDiagnostics",
    "runtime_diagnostics",
]