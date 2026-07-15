"""
==============================================================================
GEETA AI Engine

File        : provider_failover.py
Package     : providers
Description : Automatic AI Provider Failover

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from threading import RLock
from typing import Any

from config.logger import get_logger

from providers.provider_health_monitor import (
    provider_health_monitor,
)
from providers.provider_switcher import (
    provider_switcher,
)

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Provider Failover
###############################################################################


class ProviderFailover:
    """
    Automatic AI Provider Failover.

    Features
    --------

    • Automatic provider recovery
    • Runtime failover
    • Fastest healthy provider selection
    • Retry support
    • Thread-safe
    """

    def __init__(self) -> None:

        self._lock = RLock()

        self._enabled = True

        logger.info(
            "Provider Failover initialized."
        )

    ###########################################################################

    @property
    def enabled(
        self,
    ) -> bool:

        return self._enabled

    ###########################################################################

    def enable(
        self,
    ) -> None:

        self._enabled = True

    ###########################################################################

    def disable(
        self,
    ) -> None:

        self._enabled = False

    ###########################################################################

    def failover(
        self,
    ) -> str | None:
        """
        Switch to the best healthy provider.
        """

        if not self.enabled:

            return None

        with self._lock:

            provider_health_monitor.check_all()

            best = (
                provider_health_monitor.best_provider()
            )

            if best is None:

                logger.warning(
                    "No healthy provider available."
                )

                return None

            provider_switcher.switch(
                best,
            )

            logger.info(
                "Automatic failover -> %s",
                best,
            )

            return best
            ###############################################################################
# Preferred Provider
###############################################################################

    def failover_to(
        self,
        provider_name: str,
    ) -> bool:
        """
        Switch to a specific provider if healthy.
        """

        if not self.enabled:

            return False

        report = provider_health_monitor.check(
            provider_name,
        )

        if not report.healthy:

            logger.warning(
                "Provider '%s' is not healthy.",
                provider_name,
            )

            return False

        provider_switcher.switch(
            provider_name,
        )

        logger.info(
            "Switched to provider '%s'.",
            provider_name,
        )

        return True

###############################################################################
# Recovery
###############################################################################

    def recover(
        self,
    ) -> str | None:
        """
        Recover to the preferred provider when available.
        """

        preferred = (
            provider_switcher.active_name()
        )

        if preferred is None:

            return None

        report = provider_health_monitor.check(
            preferred,
        )

        if not report.healthy:

            return self.failover()

        return preferred

###############################################################################
# Retry
###############################################################################

    def retry(
        self,
        attempts: int = 3,
    ) -> str | None:
        """
        Retry automatic failover.
        """

        attempts = max(
            1,
            attempts,
        )

        for _ in range(attempts):

            provider = self.failover()

            if provider is not None:

                return provider

        return None

###############################################################################
# Status
###############################################################################

    def current_provider(
        self,
    ) -> str | None:
        """
        Return active provider name.
        """

        return provider_switcher.active_name()

###############################################################################
# Available Healthy Providers
###############################################################################

    def healthy_providers(
        self,
    ) -> list[str]:
        """
        Return healthy providers.
        """

        provider_health_monitor.check_all()

        return (
            provider_health_monitor
            .healthy_providers()
        )
        ###############################################################################
# Diagnostics
###############################################################################

    def diagnostics(
        self,
    ) -> dict[str, Any]:
        """
        Return failover diagnostics.
        """

        return {
            "enabled": self.enabled,
            "active_provider": self.current_provider(),
            "healthy_providers": self.healthy_providers(),
            "best_provider": (
                provider_health_monitor.best_provider()
            ),
        }

###############################################################################
# Reset
###############################################################################

    def reset(
        self,
    ) -> None:
        """
        Reset failover state.
        """

        logger.info(
            "Resetting Provider Failover."
        )

###############################################################################
# Shutdown
###############################################################################

    def shutdown(
        self,
    ) -> None:
        """
        Shutdown failover service.
        """

        self.disable()

        logger.info(
            "Provider Failover shut down."
        )

###############################################################################
# Global Instance
###############################################################################

provider_failover = ProviderFailover()

###############################################################################
# Helper Functions
###############################################################################


def automatic_failover(
) -> str | None:
    """
    Execute automatic failover.
    """

    return provider_failover.failover()


def retry_failover(
    attempts: int = 3,
) -> str | None:
    """
    Retry failover.
    """

    return provider_failover.retry(
        attempts,
    )


def recover_provider(
) -> str | None:
    """
    Recover preferred provider.
    """

    return provider_failover.recover()


def failover_diagnostics(
) -> dict[str, Any]:
    """
    Return diagnostics.
    """

    return provider_failover.diagnostics()


###############################################################################
# Exports
###############################################################################

__all__ = [
    "ProviderFailover",
    "provider_failover",
    "automatic_failover",
    "retry_failover",
    "recover_provider",
    "failover_diagnostics",
]