"""
==============================================================================
GEETA AI Engine

File        : agent_orchestrator.py
Package     : agents
Description : Agent Orchestrator

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from typing import Any

from agents.base_agent import BaseAgent
from config.logger import get_logger
from memory.memory_manager import memory_manager
from providers.provider_manager import provider_manager
from workspace.context_builder import context_builder

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Agent Orchestrator
###############################################################################


class AgentOrchestrator:
    """
    Central AI orchestration engine.

    Responsibilities

    - Agent routing
    - Context injection
    - Provider selection
    - Memory synchronization
    - Multi-agent execution
    - Result aggregation
    """

    def __init__(self) -> None:

        self._agents: dict[
            str,
            BaseAgent,
        ] = {}

        self._executor = ThreadPoolExecutor(
            max_workers=8,
            thread_name_prefix="GEETA-Agent",
        )

        logger.info(
            "Agent Orchestrator initialized."
        )

    ###########################################################################

    def register(
        self,
        agent: BaseAgent,
    ) -> None:
        """
        Register an AI agent.
        """

        self._agents[
            agent.name
        ] = agent

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

        self._agents.pop(
            name,
            None,
        )

    ###########################################################################

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check agent existence.
        """

        return name in self._agents

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

    def execute(
        self,
        agent_name: str,
        request: str,
        **kwargs: Any,
    ) -> Any:
        """
        Execute a single AI agent.
        """

        logger.info(
            "Executing agent: %s",
            agent_name,
        )

        agent = self.get(
            agent_name,
        )

        context = context_builder.build(
            request,
        )

        provider = (
            provider_manager.active_provider()
        )

        return agent.execute(
            request=request,
            context=context,
            provider=provider,
            memory=memory_manager,
            **kwargs,
        )
###############################################################################
# Parallel Execution
###############################################################################

    def execute_parallel(
        self,
        requests: list[tuple[str, str]],
    ) -> dict[str, Any]:
        """
        Execute multiple agents in parallel.

        Args:
            requests:
                List of (agent_name, request) tuples.
        """

        futures = {}

        for agent_name, request in requests:

            future = self._executor.submit(
                self.execute,
                agent_name,
                request,
            )

            futures[future] = agent_name

        results: dict[str, Any] = {}

        for future, agent_name in futures.items():

            try:

                results[agent_name] = future.result()

            except Exception as exc:

                logger.exception(
                    "Agent '%s' failed.",
                    agent_name,
                )

                results[agent_name] = exc

        return results


###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return orchestrator statistics.
        """

        return {
            "registered_agents": len(
                self._agents
            ),
            "agents": sorted(
                self._agents.keys()
            ),
            "max_workers": 8,
        }


###############################################################################
# Shutdown
###############################################################################

    def shutdown(
        self,
        wait: bool = True,
    ) -> None:
        """
        Shutdown orchestrator.
        """

        logger.info(
            "Shutting down Agent Orchestrator..."
        )

        self._executor.shutdown(
            wait=wait,
        )


###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return orchestrator report.
        """

        return {
            "statistics": self.statistics(),
            "providers": (
                provider_manager.providers()
            ),
            "memories": (
                memory_manager.memories()
            ),
        }


###############################################################################
# Global Orchestrator
###############################################################################

agent_orchestrator = AgentOrchestrator()


###############################################################################
# Exports
###############################################################################

__all__ = [
    "AgentOrchestrator",
    "agent_orchestrator",
]