"""
==============================================================================
GEETA AI Engine

File        : agent_manager.py
Package     : agents
Description : AI Agent Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Any

from agents.base_agent import BaseAgent
from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Agent Manager
###############################################################################


class AgentManager:
    """
    Central manager for all AI agents.

    Responsibilities:

    - Register agents
    - Remove agents
    - Execute agents
    - Route requests
    - Health monitoring
    """

    def __init__(self) -> None:

        self._agents: dict[str, BaseAgent] = {}

        logger.info(
            "Agent Manager initialized."
        )

    ###########################################################################

    def register(
        self,
        agent: BaseAgent,
    ) -> None:
        """
        Register an AI agent.
        """

        if agent.name in self._agents:

            raise ValueError(
                f"Agent '{agent.name}' already exists."
            )

        agent.initialize()

        self._agents[agent.name] = agent

        logger.info(
            "Registered agent: %s",
            agent.name,
        )

    ###########################################################################

    def unregister(
        self,
        name: str,
    ) -> None:
        """
        Remove an agent.
        """

        agent = self._agents.pop(
            name,
            None,
        )

        if agent is None:
            return

        agent.shutdown()

        logger.info(
            "Removed agent: %s",
            name,
        )

    ###########################################################################

    def get(
        self,
        name: str,
    ) -> BaseAgent:
        """
        Return registered agent.
        """

        return self._agents[name]

    ###########################################################################

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check whether an agent exists.
        """

        return name in self._agents

    ###########################################################################

    def list_agents(
        self,
    ) -> list[str]:
        """
        Return registered agent names.
        """

        return sorted(
            self._agents.keys()
        )
###############################################################################
# Agent Execution
###############################################################################

    def execute(
        self,
        name: str,
        context: dict[str, Any],
    ) -> Any:
        """
        Execute a specific agent.
        """

        agent = self.get(name)

        if not agent.enabled:

            raise RuntimeError(
                f"Agent '{name}' is disabled."
            )

        logger.info(
            "Executing agent: %s",
            name,
        )

        return agent.execute(context)

    ###########################################################################

    def find_handler(
        self,
        context: dict[str, Any],
    ) -> BaseAgent | None:
        """
        Find the first capable agent.
        """

        for agent in self._agents.values():

            if not agent.enabled:
                continue

            if agent.can_handle(context):

                return agent

        return None

    ###########################################################################

    def execute_best_agent(
        self,
        context: dict[str, Any],
    ) -> Any:
        """
        Automatically select and execute
        the most suitable agent.
        """

        agent = self.find_handler(context)

        if agent is None:

            raise RuntimeError(
                "No suitable agent found."
            )

        logger.info(
            "Selected agent: %s",
            agent.name,
        )

        return agent.execute(context)

###############################################################################
# Management
###############################################################################

    def shutdown_all(self) -> None:
        """
        Shutdown every registered agent.
        """

        for agent in self._agents.values():

            agent.shutdown()

        logger.info(
            "All agents shut down."
        )

    ###########################################################################

    def clear(self) -> None:
        """
        Remove every registered agent.
        """

        self.shutdown_all()

        self._agents.clear()

        logger.info(
            "Agent manager cleared."
        )

    ###########################################################################

    def count(self) -> int:
        """
        Return number of registered agents.
        """

        return len(self._agents)


###############################################################################
# Global Manager
###############################################################################

agent_manager = AgentManager()

###############################################################################
# Helper Functions
###############################################################################


def register_agent(
    agent: BaseAgent,
) -> None:
    """
    Register an AI agent.
    """

    agent_manager.register(agent)


def unregister_agent(
    name: str,
) -> None:
    """
    Remove an AI agent.
    """

    agent_manager.unregister(name)


def execute_agent(
    name: str,
    context: dict[str, Any],
) -> Any:
    """
    Execute a named AI agent.
    """

    return agent_manager.execute(
        name,
        context,
    )


###############################################################################
# Exports
###############################################################################

__all__ = [
    "AgentManager",
    "agent_manager",
    "register_agent",
    "unregister_agent",
    "execute_agent",
]