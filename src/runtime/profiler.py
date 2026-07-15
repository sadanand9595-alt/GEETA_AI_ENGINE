"""
==============================================================================
GEETA AI Engine

File        : profiler.py
Package     : runtime
Description : Runtime Profiler

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import cProfile
import io
import pstats
from pathlib import Path
from typing import Any, Callable

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Runtime Profiler
###############################################################################


class RuntimeProfiler:
    """
    Runtime performance profiler.

    Responsibilities

    - CPU profiling
    - Function profiling
    - Performance reports
    - Hotspot analysis
    - Timeline generation
    """

    def __init__(self) -> None:

        self._profiler = cProfile.Profile()

        self._running = False

        self._last_report = ""

        logger.info(
            "Runtime Profiler initialized."
        )

    ###########################################################################

    def start(
        self,
    ) -> None:
        """
        Start profiling.
        """

        if self._running:

            return

        self._running = True

        self._profiler.enable()

        logger.info(
            "Profiler started."
        )

    ###########################################################################

    def stop(
        self,
    ) -> None:
        """
        Stop profiling.
        """

        if not self._running:

            return

        self._profiler.disable()

        self._running = False

        stream = io.StringIO()

        stats = pstats.Stats(
            self._profiler,
            stream=stream,
        )

        stats.sort_stats(
            "cumulative",
        )

        stats.print_stats()

        self._last_report = (
            stream.getvalue()
        )

        logger.info(
            "Profiler stopped."
        )

    ###########################################################################

    def profile(
        self,
        function: Callable[..., Any],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Profile a callable.
        """

        self.start()

        try:

            return function(
                *args,
                **kwargs,
            )

        finally:

            self.stop()

    ###########################################################################

    def report_text(
        self,
    ) -> str:
        """
        Return profiling report.
        """

        return self._last_report
###############################################################################
# Export
###############################################################################

    def export(
        self,
        destination: str | Path,
    ) -> Path:
        """
        Export the latest profiling report.
        """

        output = Path(destination)

        output.write_text(
            self._last_report,
            encoding="utf-8",
        )

        logger.info(
            "Profiler report exported: %s",
            output,
        )

        return output

###############################################################################
# Hotspot Detection
###############################################################################

    def hotspots(
        self,
        limit: int = 10,
    ) -> list[str]:
        """
        Return the most expensive functions.

        Placeholder implementation.
        Future versions will parse pstats data
        directly instead of report text.
        """

        if not self._last_report:

            return []

        lines = self._last_report.splitlines()

        return lines[:limit]

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return profiler statistics.
        """

        return {
            "running": self._running,
            "report_available": bool(
                self._last_report
            ),
            "hotspots": len(
                self.hotspots()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return profiler report.
        """

        return {
            "statistics": self.statistics(),
            "hotspots": self.hotspots(),
        }

###############################################################################
# Global Profiler
###############################################################################

runtime_profiler = RuntimeProfiler()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "RuntimeProfiler",
    "runtime_profiler",
]