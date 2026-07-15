"""
==============================================================================
GEETA AI Engine

File        : runtime_monitor.py
Package     : runtime
Description : Runtime Monitor

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import threading
import time
from typing import Any

import psutil

from config.logger import get_logger
from runtime.runtime_events import (
    runtime_events,
)

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Runtime Monitor
###############################################################################


class RuntimeMonitor:
    """
    Runtime monitoring service.

    Responsibilities

    - CPU monitoring
    - Memory monitoring
    - Process monitoring
    - Performance metrics
    - Runtime alerts
    - Event publishing
    """

    def __init__(
        self,
        interval: float = 1.0,
    ) -> None:

        self._interval = interval

        self._running = False

        self._thread: threading.Thread | None = None

        self._latest_metrics: dict[
            str,
            Any,
        ] = {}

        logger.info(
            "Runtime Monitor initialized."
        )

    ###########################################################################

    def start(
        self,
    ) -> None:
        """
        Start monitoring.
        """

        if self._running:

            return

        self._running = True

        self._thread = threading.Thread(
            target=self._loop,
            daemon=True,
            name="RuntimeMonitor",
        )

        self._thread.start()

        logger.info(
            "Runtime Monitor started."
        )

    ###########################################################################

    def stop(
        self,
    ) -> None:
        """
        Stop monitoring.
        """

        self._running = False

        if self._thread:

            self._thread.join()

        logger.info(
            "Runtime Monitor stopped."
        )

    ###########################################################################

    def _loop(
        self,
    ) -> None:
        """
        Monitoring loop.
        """

        while self._running:

            metrics = self.collect()

            self._latest_metrics = metrics

            runtime_events.publish(
                "runtime.metrics",
                metrics=metrics,
            )

            time.sleep(
                self._interval,
            )

    ###########################################################################

    def collect(
        self,
    ) -> dict[str, Any]:
        """
        Collect runtime metrics.
        """

        return {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": (
                psutil.virtual_memory().percent
            ),
            "available_memory": (
                psutil.virtual_memory().available
            ),
            "disk_percent": (
                psutil.disk_usage("/").percent
            ),
            "processes": len(
                psutil.pids()
            ),
        }
###############################################################################
# Metrics
###############################################################################

    def latest_metrics(
        self,
    ) -> dict[str, Any]:
        """
        Return latest runtime metrics.
        """

        return dict(
            self._latest_metrics
        )

###############################################################################
# Alerts
###############################################################################

    def alerts(
        self,
    ) -> list[str]:
        """
        Return runtime alerts.
        """

        alerts: list[str] = []

        metrics = self._latest_metrics

        if not metrics:

            return alerts

        if metrics.get("cpu_percent", 0) > 90:

            alerts.append(
                "High CPU usage detected."
            )

        if metrics.get("memory_percent", 0) > 90:

            alerts.append(
                "High memory usage detected."
            )

        if metrics.get("disk_percent", 0) > 95:

            alerts.append(
                "Disk usage is critically high."
            )

        return alerts

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return monitor statistics.
        """

        return {
            "running": self._running,
            "interval": self._interval,
            "metrics_available": bool(
                self._latest_metrics
            ),
            "alerts": len(
                self.alerts()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return runtime monitor report.
        """

        return {
            "statistics": self.statistics(),
            "metrics": self.latest_metrics(),
            "alerts": self.alerts(),
        }

###############################################################################
# Global Runtime Monitor
###############################################################################

runtime_monitor = RuntimeMonitor()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "RuntimeMonitor",
    "runtime_monitor",
]