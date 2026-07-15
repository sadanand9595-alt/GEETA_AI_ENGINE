"""
==============================================================================
GEETA AI Engine

File        : git_events.py
Package     : git
Description : Git Event Bus

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from time import time
from typing import Any, Callable

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Git Event
###############################################################################


@dataclass(slots=True)
class GitEvent:
    """
    Git event.
    """

    event_type: str

    payload: dict[str, Any] = field(
        default_factory=dict,
    )

    timestamp: float = field(
        default_factory=time,
    )

###############################################################################
# Git Event Bus
###############################################################################


class GitEventBus:
    """
    Publish/Subscribe event bus for Git.

    Responsibilities

    - Publish events
    - Subscribe handlers
    - Remove handlers
    - Broadcast Git activity
    """

    def __init__(self) -> None:

        self._subscribers: dict[
            str,
            list[Callable[[GitEvent], None]]
        ] = defaultdict(list)

        logger.info(
            "Git Event Bus initialized."
        )

    ###########################################################################

    def subscribe(
        self,
        event_type: str,
        callback: Callable[[GitEvent], None],
    ) -> None:
        """
        Subscribe to an event.
        """

        self._subscribers[
            event_type
        ].append(callback)

    ###########################################################################

    def unsubscribe(
        self,
        event_type: str,
        callback: Callable[[GitEvent], None],
    ) -> bool:
        """
        Remove an event subscriber.
        """

        handlers = self._subscribers.get(
            event_type,
        )

        if not handlers:

            return False

        if callback in handlers:

            handlers.remove(
                callback,
            )

            return True

        return False

    ###########################################################################

    def publish(
        self,
        event_type: str,
        **payload: Any,
    ) -> None:
        """
        Publish a Git event.
        """

        event = GitEvent(
            event_type=event_type,
            payload=payload,
        )

        logger.info(
            "Git event: %s",
            event_type,
        )

        for callback in self._subscribers.get(
            event_type,
            [],
        ):

            callback(
                event,
            )
###############################################################################
# Event Types
###############################################################################

    def event_types(
        self,
    ) -> list[str]:
        """
        Return registered event types.
        """

        return sorted(
            self._subscribers.keys()
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return Git event bus statistics.
        """

        subscriber_count = sum(
            len(callbacks)
            for callbacks
            in self._subscribers.values()
        )

        return {
            "event_types": len(
                self._subscribers
            ),
            "subscribers": subscriber_count,
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Return Git event report.
        """

        return {
            "statistics": self.statistics(),
            "events": {
                event: len(callbacks)
                for event, callbacks
                in self._subscribers.items()
            },
        }

###############################################################################
# Global Git Event Bus
###############################################################################

git_events = GitEventBus()

###############################################################################
# Standard Git Events
###############################################################################

REPOSITORY_OPENED = "repository.opened"
REPOSITORY_INITIALIZED = "repository.initialized"

BRANCH_CREATED = "branch.created"
BRANCH_DELETED = "branch.deleted"
BRANCH_SWITCHED = "branch.switched"

COMMIT_CREATED = "commit.created"
COMMIT_AMENDED = "commit.amended"

DIFF_GENERATED = "diff.generated"

MERGE_STARTED = "merge.started"
MERGE_COMPLETED = "merge.completed"
MERGE_ABORTED = "merge.aborted"

REBASE_STARTED = "rebase.started"
REBASE_COMPLETED = "rebase.completed"
REBASE_ABORTED = "rebase.aborted"

REMOTE_FETCH = "remote.fetch"
REMOTE_PULL = "remote.pull"
REMOTE_PUSH = "remote.push"

STASH_CREATED = "stash.created"
STASH_APPLIED = "stash.applied"
STASH_DROPPED = "stash.dropped"

TAG_CREATED = "tag.created"
TAG_DELETED = "tag.deleted"

RELEASE_CREATED = "release.created"

###############################################################################
# Exports
###############################################################################

__all__ = [
    "GitEvent",
    "GitEventBus",
    "git_events",
    "REPOSITORY_OPENED",
    "REPOSITORY_INITIALIZED",
    "BRANCH_CREATED",
    "BRANCH_DELETED",
    "BRANCH_SWITCHED",
    "COMMIT_CREATED",
    "COMMIT_AMENDED",
    "DIFF_GENERATED",
    "MERGE_STARTED",
    "MERGE_COMPLETED",
    "MERGE_ABORTED",
    "REBASE_STARTED",
    "REBASE_COMPLETED",
    "REBASE_ABORTED",
    "REMOTE_FETCH",
    "REMOTE_PULL",
    "REMOTE_PUSH",
    "STASH_CREATED",
    "STASH_APPLIED",
    "STASH_DROPPED",
    "TAG_CREATED",
    "TAG_DELETED",
    "RELEASE_CREATED",
]