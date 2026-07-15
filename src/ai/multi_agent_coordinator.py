"""
==============================================================================
GEETA AI IDE

File        : multi_agent_coordinator.py
Package     : ai
Description : Enterprise Multi-Agent Coordinator

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Agent State
###############################################################################


class AgentState(str, Enum):

    IDLE = "idle"

    BUSY = "busy"

    WAITING = "waiting"

    FAILED = "failed"

    OFFLINE = "offline"

###############################################################################
# Registered Agent
###############################################################################


@dataclass(slots=True)
class RegisteredAgent:
    """
    Registered AI Agent.
    """

    name: str

    instance: object

    state: AgentState = AgentState.IDLE

    priority: int = 100

    last_activity: datetime = field(
        default_factory=datetime.utcnow
    )

###############################################################################
# Agent Message
###############################################################################


@dataclass(slots=True)
class AgentMessage:
    """
    Inter-agent message.
    """

    sender: str

    receiver: str

    event: str

    payload: dict = field(
        default_factory=dict
    )

###############################################################################
# Multi-Agent Coordinator
###############################################################################


class MultiAgentCoordinator:
    """
    Enterprise Multi-Agent Coordinator.

    Responsibilities

    - Agent registry
    - Task delegation
    - Shared context
    - Event broadcasting
    - Parallel coordination
    - Failure recovery
    """

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._agents: dict[
            str,
            RegisteredAgent
        ] = {}

        self._messages: list[
            AgentMessage
        ] = []

        logger.info(
            "Multi-Agent Coordinator initialized."
        )

###############################################################################
# Register Agent
###############################################################################

    def register(
        self,
        agent: RegisteredAgent,
    ) -> None:
        """
        Register an AI agent.
        """

        self._agents[
            agent.name
        ] = agent

###############################################################################
# Lookup Agent
###############################################################################

    def agent(
        self,
        name: str,
    ) -> RegisteredAgent | None:
        """
        Return registered agent.
        """

        return self._agents.get(
            name
        )

###############################################################################
# Send Message
###############################################################################

    def send(
        self,
        message: AgentMessage,
    ) -> None:
        """
        Send message to another agent.
        """

        self._messages.append(
            message
        )

        logger.info(
            "%s -> %s (%s)",
            message.sender,
            message.receiver,
            message.event,
        )
###############################################################################
# Broadcast Event
###############################################################################

    def broadcast(
        self,
        sender: str,
        event: str,
        payload: dict | None = None,
    ) -> None:
        """
        Broadcast an event to all registered agents.
        """

        payload = payload or {}

        for agent in self._agents.values():

            if agent.name == sender:

                continue

            self.send(
                AgentMessage(
                    sender=sender,
                    receiver=agent.name,
                    event=event,
                    payload=payload,
                ),
            )

###############################################################################
# Delegate Task
###############################################################################

    def delegate(
        self,
        agent_name: str,
        task: str,
        payload: dict | None = None,
    ) -> bool:
        """
        Delegate a task to an agent.
        """

        agent = self.agent(
            agent_name,
        )

        if agent is None:

            return False

        agent.state = AgentState.BUSY

        agent.last_activity = (
            datetime.utcnow()
        )

        logger.info(
            "Delegated '%s' to %s",
            task,
            agent_name,
        )

        return True

###############################################################################
# Resolve Conflict
###############################################################################

    def resolve_conflict(
        self,
        first: str,
        second: str,
    ) -> str:
        """
        Resolve execution conflict using priority.
        """

        agent_a = self.agent(first)

        agent_b = self.agent(second)

        if agent_a is None:

            return second

        if agent_b is None:

            return first

        if (
            agent_a.priority
            <= agent_b.priority
        ):

            return first

        return second

###############################################################################
# Health Check
###############################################################################

    def health(
        self,
    ) -> dict[str, str]:
        """
        Return health of every agent.
        """

        return {
            name: agent.state.value
            for name, agent
            in self._agents.items()
        }

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Coordinator statistics.
        """

        return {
            "agents": len(
                self._agents
            ),
            "messages": len(
                self._messages
            ),
            "busy": sum(
                1
                for agent
                in self._agents.values()
                if agent.state
                == AgentState.BUSY
            ),
            "idle": sum(
                1
                for agent
                in self._agents.values()
                if agent.state
                == AgentState.IDLE
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return coordinator report.
        """

        return {
            "statistics": self.statistics(),
            "health": self.health(),
            "registered_agents": sorted(
                self._agents.keys()
            ),
        }

###############################################################################
# Global Coordinator
###############################################################################

multi_agent_coordinator: (
    MultiAgentCoordinator | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "AgentState",
    "RegisteredAgent",
    "AgentMessage",
    "MultiAgentCoordinator",
    "multi_agent_coordinator",
]