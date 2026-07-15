"""
==============================================================================
GEETA AI Engine

File        : base_agent.py
Package     : agents
Description : Base AI Agent

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Base Agent
###############################################################################


class BaseAgent(ABC):
    """
    Base class for all GEETA AI agents.

    Every agent in the system inherits from this class.

    Examples:
        - DebugAgent
        - ReviewAgent
        - RefactorAgent
        - ClipboardAgent
        - ProjectGeneratorAgent
        - DocumentationAgent
    """

    def __init__(
        self,
        name: str,
        description: str,
    ) -> None:

        self._name = name

        self._description = description

        self._enabled = True

        self._created_at = datetime.utcnow()

        logger.info(
            "Agent initialized: %s",
            self._name,
        )

    ###########################################################################

    @property
    def name(self) -> str:
        """
        Agent name.
        """

        return self._name

    ###########################################################################

    @property
    def description(self) -> str:
        """
        Agent description.
        """

        return self._description

    ###########################################################################

    @property
    def enabled(self) -> bool:
        """
        Return enabled state.
        """

        return self._enabled

    ###########################################################################

    def enable(self) -> None:
        """
        Enable the agent.
        """

        self._enabled = True

        logger.info(
            "Agent enabled: %s",
            self._name,
        )

    ###########################################################################

    def disable(self) -> None:
        """
        Disable the agent.
        """

        self._enabled = False

        logger.info(
            "Agent disabled: %s",
            self._name,
        )

    ###########################################################################

    @abstractmethod
    def execute(
        self,
        context: dict[str, Any],
    ) -> Any:
        """
        Execute the agent.

        Must be implemented by every agent.
        """

    ###########################################################################

    @abstractmethod
    def can_handle(
        self,
        context: dict[str, Any],
    ) -> bool:
        """
        Return True if this agent can handle the request.
        """
###############################################################################
# Metadata
###############################################################################

    @property
    def created_at(self) -> datetime:
        """
        Return agent creation time.
        """

        return self._created_at

    ###########################################################################

    def metadata(self) -> dict[str, Any]:
        """
        Return agent metadata.
        """

        return {
            "name": self.name,
            "description": self.description,
            "enabled": self.enabled,
            "created_at": self.created_at.isoformat(),
        }

###############################################################################
# Lifecycle Hooks
###############################################################################

    def initialize(self) -> None:
        """
        Initialize agent resources.

        Override if needed.
        """

        logger.info(
            "Initializing agent: %s",
            self.name,
        )

    ###########################################################################

    def shutdown(self) -> None:
        """
        Shutdown agent resources.

        Override if needed.
        """

        logger.info(
            "Shutting down agent: %s",
            self.name,
        )

    ###########################################################################

    def reset(self) -> None:
        """
        Reset internal agent state.

        Override if needed.
        """

        logger.info(
            "Resetting agent: %s",
            self.name,
        )

###############################################################################
# Health Check
###############################################################################

    def healthy(self) -> bool:
        """
        Return True if the agent is healthy.
        """

        return self.enabled

###############################################################################
# String Representation
###############################################################################

    def __repr__(self) -> str:
        """
        Developer-friendly representation.
        """

        return (
            f"{self.__class__.__name__}"
            f"(name='{self.name}', "
            f"enabled={self.enabled})"
        )


###############################################################################
# Exports
###############################################################################

__all__ = [
    "BaseAgent",
]