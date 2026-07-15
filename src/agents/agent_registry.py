"""
==============================================================================
GEETA AI Engine

File        : agent_registry.py
Package     : agents
Description : Agent Registry

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Type

from agents.agent_orchestrator import (
    agent_orchestrator,
)
from agents.base_agent import BaseAgent
from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Agent Registry
###############################################################################


class AgentRegistry:
    """
    Central registry for AI agents.

    Responsibilities

    - Agent registration
    - Dynamic creation
    - Plugin support
    - Agent discovery
    - Lifecycle management
    """

    def __init__(self) -> None:

        self._registry: dict[
            str,
            Type[BaseAgent],
        ] = {}

        logger.info(
            "Agent Registry initialized."
        )

    ###########################################################################

    def register(
        self,
        name: str,
        agent_class: Type[BaseAgent],
    ) -> None:
        """
        Register an agent class.
        """

        self._registry[
            name
        ] = agent_class

        logger.info(
            "Registered agent class: %s",
            name,
        )

    ###########################################################################

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check whether an agent exists.
        """

        return name in self._registry

    ###########################################################################

    def create(
        self,
        name: str,
        **kwargs,
    ) -> BaseAgent:
        """
        Create an agent instance.
        """

        agent_class = self._registry[
            name
        ]

        return agent_class(
            **kwargs,
        )

    ###########################################################################

    def register_instance(
        self,
        name: str,
        **kwargs,
    ) -> None:
        """
        Create and register an agent instance.
        """

        agent = self.create(
            name,
            **kwargs,
        )

        if not agent_orchestrator.exists(
            agent.name,
        ):

            agent_orchestrator.register(
                agent,
            )
###############################################################################
# Registry Queries
###############################################################################

    def agents(
        self,
    ) -> list[str]:
        """
        Return registered agent names.
        """

        return sorted(
            self._registry.keys()
        )

    ###########################################################################

    def count(
        self,
    ) -> int:
        """
        Return registered agent count.
        """

        return len(
            self._registry
        )

###############################################################################
# Initialization
###############################################################################

    def initialize(
        self,
    ) -> None:
        """
        Register built-in agent classes.

        Built-in agents are registered by the
        application during startup.
        """

        logger.info(
            "Initialized Agent Registry."
        )

    ###########################################################################

    def create_all(
        self,
    ) -> None:
        """
        Instantiate every registered agent.
        """

        for name in self.agents():

            self.register_instance(
                name,
            )

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return registry report.
        """

        return {
            "registered_agents": self.count(),
            "agents": self.agents(),
        }

###############################################################################
# Global Registry
###############################################################################

agent_registry = AgentRegistry()

###############################################################################
# Helper Functions
###############################################################################

def initialize_agents() -> None:
    """
    Initialize agent registry.
    """

    agent_registry.initialize()


def available_agents() -> list[str]:
    """
    Return available agent names.
    """

    return agent_registry.agents()


###############################################################################
# Exports
###############################################################################

__all__ = [
    "AgentRegistry",
    "agent_registry",
    "initialize_agents",
    "available_agents",
]