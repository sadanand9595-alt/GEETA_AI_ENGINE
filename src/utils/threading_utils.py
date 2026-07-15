"""
==============================================================================
GEETA AI Engine

File        : threading_utils.py
Package     : utils
Description : Threading Utility Functions

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import threading
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Thread Pool
###############################################################################

_DEFAULT_WORKERS = 4

_executor = ThreadPoolExecutor(
    max_workers=_DEFAULT_WORKERS,
    thread_name_prefix="GEETA",
)

###############################################################################
# Thread Helpers
###############################################################################


def create_thread(
    target: Callable[..., Any],
    *args: Any,
    daemon: bool = True,
    name: str | None = None,
    **kwargs: Any,
) -> threading.Thread:
    """
    Create a thread.
    """

    thread = threading.Thread(
        target=target,
        args=args,
        kwargs=kwargs,
        daemon=daemon,
        name=name,
    )

    logger.debug(
        "Thread created: %s",
        thread.name,
    )

    return thread


def start_thread(
    target: Callable[..., Any],
    *args: Any,
    daemon: bool = True,
    name: str | None = None,
    **kwargs: Any,
) -> threading.Thread:
    """
    Create and start a thread.
    """

    thread = create_thread(
        target,
        *args,
        daemon=daemon,
        name=name,
        **kwargs,
    )

    thread.start()

    logger.debug(
        "Thread started: %s",
        thread.name,
    )

    return thread


###############################################################################
# Thread Pool Helpers
###############################################################################


def submit(
    function: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> Future:
    """
    Submit a task to the thread pool.
    """

    logger.debug(
        "Submitting task: %s",
        function.__name__,
    )

    return _executor.submit(
        function,
        *args,
        **kwargs,
    )


def map_tasks(
    function: Callable[..., Any],
    iterable,
):
    """
    Execute function over iterable.
    """

    return list(
        _executor.map(
            function,
            iterable,
        )
    )


###############################################################################
# Thread Information
###############################################################################


def current_thread() -> threading.Thread:
    """
    Return current thread.
    """

    return threading.current_thread()


def active_thread_count() -> int:
    """
    Return active thread count.
    """

    return threading.active_count()
###############################################################################
# Synchronization
###############################################################################


def create_lock() -> threading.Lock:
    """
    Create a thread lock.
    """

    return threading.Lock()


def create_rlock() -> threading.RLock:
    """
    Create a reentrant lock.
    """

    return threading.RLock()


def create_event() -> threading.Event:
    """
    Create a thread event.
    """

    return threading.Event()


###############################################################################
# Timer
###############################################################################


def create_timer(
    interval: float,
    function: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> threading.Timer:
    """
    Create a timer.
    """

    timer = threading.Timer(
        interval,
        function,
        args=args,
        kwargs=kwargs,
    )

    logger.debug(
        "Timer created (%s sec).",
        interval,
    )

    return timer


def start_timer(
    interval: float,
    function: Callable[..., Any],
    *args: Any,
    **kwargs: Any,
) -> threading.Timer:
    """
    Create and start a timer.
    """

    timer = create_timer(
        interval,
        function,
        *args,
        **kwargs,
    )

    timer.start()

    return timer


###############################################################################
# Executor
###############################################################################


def shutdown_executor(
    wait: bool = True,
) -> None:
    """
    Shutdown thread pool executor.
    """

    logger.info(
        "Shutting down thread pool."
    )

    _executor.shutdown(
        wait=wait,
    )


###############################################################################
# Wait Helpers
###############################################################################


def join_thread(
    thread: threading.Thread,
    timeout: float | None = None,
) -> None:
    """
    Wait for thread completion.
    """

    thread.join(timeout)


def is_alive(
    thread: threading.Thread,
) -> bool:
    """
    Return thread state.
    """

    return thread.is_alive()


###############################################################################
# Exports
###############################################################################

__all__ = [
    "create_thread",
    "start_thread",
    "submit",
    "map_tasks",
    "current_thread",
    "active_thread_count",
    "create_lock",
    "create_rlock",
    "create_event",
    "create_timer",
    "start_timer",
    "shutdown_executor",
    "join_thread",
    "is_alive",
]