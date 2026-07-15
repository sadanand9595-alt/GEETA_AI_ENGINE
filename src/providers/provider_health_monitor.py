"""
==============================================================================
GEETA AI Engine

File        : provider_health_monitor.py
Package     : providers
Description : Provider Health Monitor

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from threading import RLock
from typing import Any

from config.logger import get_logger

from providers.provider_factory import provider_factory

logger = get_logger(__name__)


@dataclass(slots=True)
class ProviderHealth:

    provider: str

    healthy: bool = False

    latency_ms: float = 0.0

    last_check: float = 0.0

    failures: int = 0

    metadata: dict[str, Any] | None = None


class ProviderHealthMonitor:

    """
    Monitors every registered AI provider.
    """

    def __init__(self) -> None:

        self._lock = RLock()

        self._health: dict[
            str,
            ProviderHealth,
        ] = {}

        logger.info(
            "Provider Health Monitor initialized."
        )
        ###############################################################################
# Health Check
###############################################################################

    def check(
        self,
        provider_name: str,
    ) -> ProviderHealth:
        """
        Check a single provider.
        """

        with self._lock:

            start = time.perf_counter()

            provider = provider_factory.get(
                provider_name,
            )

            healthy = False

            failures = 0

            try:

                healthy = provider.test_connection()

            except Exception:

                logger.exception(
                    "Health check failed for %s",
                    provider_name,
                )

                failures = 1

            latency = (
                time.perf_counter() - start
            ) * 1000.0

            previous = self._health.get(
                provider_name,
            )

            if previous is not None:

                failures += previous.failures

            report = ProviderHealth(

                provider=provider_name,

                healthy=healthy,

                latency_ms=latency,

                last_check=time.time(),

                failures=(
                    failures
                    if not healthy
                    else 0
                ),

                metadata=provider.metadata(),
            )

            self._health[
                provider_name
            ] = report

            logger.info(
                "Provider %s | Healthy=%s | %.2f ms",
                provider_name,
                healthy,
                latency,
            )

            return report

###############################################################################
# Check All Providers
###############################################################################

    def check_all(
        self,
    ) -> dict[str, ProviderHealth]:
        """
        Check every registered provider.
        """

        for provider_name in provider_factory.providers():

            self.check(
                provider_name,
            )

        return dict(
            self._health,
        )

###############################################################################
# Queries
###############################################################################

    def report(
        self,
        provider_name: str,
    ) -> ProviderHealth | None:

        return self._health.get(
            provider_name,
        )

    ###########################################################################

    def reports(
        self,
    ) -> dict[str, ProviderHealth]:

        return dict(
            self._health,
        )
        ###############################################################################
# Healthy Providers
###############################################################################

    def healthy_providers(
        self,
    ) -> list[str]:
        """
        Return all healthy providers.
        """

        return sorted(
            provider
            for provider, report in self._health.items()
            if report.healthy
        )

###############################################################################
# Best Provider
###############################################################################

    def best_provider(
        self,
    ) -> str | None:
        """
        Return the fastest healthy provider.
        """

        healthy = [
            report
            for report in self._health.values()
            if report.healthy
        ]

        if not healthy:

            return None

        best = min(
            healthy,
            key=lambda item: item.latency_ms,
        )

        return best.provider

###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, Any]:
        """
        Return health monitor diagnostics.
        """

        return {
            "providers": len(self._health),
            "healthy": len(
                self.healthy_providers()
            ),
            "best_provider": self.best_provider(),
            "reports": {
                name: {
                    "healthy": report.healthy,
                    "latency_ms": report.latency_ms,
                    "failures": report.failures,
                    "last_check": report.last_check,
                }
                for name, report in self._health.items()
            },
        }

###############################################################################
# Reset
###############################################################################

    def reset(
        self,
    ) -> None:
        """
        Clear all cached health reports.
        """

        with self._lock:

            self._health.clear()

        logger.info(
            "Provider health cache cleared."
        )

###############################################################################
# Shutdown
###############################################################################

    def shutdown(
        self,
    ) -> None:
        """
        Shutdown health monitor.
        """

        self.reset()

        logger.info(
            "Provider Health Monitor shut down."
        )

###############################################################################
# Global Monitor
###############################################################################

provider_health_monitor = ProviderHealthMonitor()

###############################################################################
# Helper Functions
###############################################################################


def check_provider(
    provider_name: str,
) -> ProviderHealth:
    """
    Check a single provider.
    """

    return provider_health_monitor.check(
        provider_name,
    )


def check_all_providers(
) -> dict[str, ProviderHealth]:
    """
    Check all providers.
    """

    return provider_health_monitor.check_all()


def best_provider(
) -> str | None:
    """
    Return the fastest healthy provider.
    """

    return provider_health_monitor.best_provider()


###############################################################################
# Exports
###############################################################################

__all__ = [
    "ProviderHealth",
    "ProviderHealthMonitor",
    "provider_health_monitor",
    "check_provider",
    "check_all_providers",
    "best_provider",
]