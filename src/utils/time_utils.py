"""
==============================================================================
GEETA AI Engine

File        : time_utils.py
Package     : utils
Description : Date & Time Utility Functions

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Current Time
###############################################################################


def now() -> datetime:
    """
    Return current UTC datetime.
    """

    return datetime.now(UTC)


def today() -> datetime:
    """
    Return today's date at midnight (UTC).
    """

    current = now()

    return current.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )


###############################################################################
# Formatting
###############################################################################


def format_datetime(
    value: datetime,
    fmt: str = "%Y-%m-%d %H:%M:%S",
) -> str:
    """
    Format datetime.
    """

    return value.strftime(fmt)


def format_date(
    value: datetime,
) -> str:
    """
    Format date.
    """

    return value.strftime("%Y-%m-%d")


def format_time(
    value: datetime,
) -> str:
    """
    Format time.
    """

    return value.strftime("%H:%M:%S")


###############################################################################
# Parsing
###############################################################################


def parse_datetime(
    value: str,
    fmt: str = "%Y-%m-%d %H:%M:%S",
) -> datetime:
    """
    Parse datetime string.
    """

    return datetime.strptime(
        value,
        fmt,
    )


###############################################################################
# ISO
###############################################################################


def to_iso(
    value: datetime,
) -> str:
    """
    Convert datetime to ISO-8601.
    """

    return value.isoformat()


def from_iso(
    value: str,
) -> datetime:
    """
    Parse ISO-8601 datetime.
    """

    return datetime.fromisoformat(value)


###############################################################################
# Timestamp
###############################################################################


def timestamp() -> float:
    """
    Return current Unix timestamp.
    """

    return now().timestamp()


def from_timestamp(
    value: float,
) -> datetime:
    """
    Convert Unix timestamp to datetime.
    """

    return datetime.fromtimestamp(
        value,
        tz=UTC,
    )


###############################################################################
# Time Difference
###############################################################################


def seconds_between(
    start: datetime,
    end: datetime,
) -> float:
    """
    Return difference in seconds.
    """

    return (end - start).total_seconds()


def minutes_between(
    start: datetime,
    end: datetime,
) -> float:
    """
    Return difference in minutes.
    """

    return seconds_between(
        start,
        end,
    ) / 60
###############################################################################
# Hours / Days
###############################################################################


def hours_between(
    start: datetime,
    end: datetime,
) -> float:
    """
    Return difference in hours.
    """

    return seconds_between(start, end) / 3600


def days_between(
    start: datetime,
    end: datetime,
) -> int:
    """
    Return difference in days.
    """

    return (end - start).days


###############################################################################
# Date Arithmetic
###############################################################################


def add_seconds(
    value: datetime,
    seconds: int,
) -> datetime:
    """
    Add seconds to datetime.
    """

    return value + timedelta(seconds=seconds)


def add_minutes(
    value: datetime,
    minutes: int,
) -> datetime:
    """
    Add minutes to datetime.
    """

    return value + timedelta(minutes=minutes)


def add_hours(
    value: datetime,
    hours: int,
) -> datetime:
    """
    Add hours to datetime.
    """

    return value + timedelta(hours=hours)


def add_days(
    value: datetime,
    days: int,
) -> datetime:
    """
    Add days to datetime.
    """

    return value + timedelta(days=days)


###############################################################################
# Date Subtraction
###############################################################################


def subtract_seconds(
    value: datetime,
    seconds: int,
) -> datetime:
    """
    Subtract seconds from datetime.
    """

    return value - timedelta(seconds=seconds)


def subtract_minutes(
    value: datetime,
    minutes: int,
) -> datetime:
    """
    Subtract minutes from datetime.
    """

    return value - timedelta(minutes=minutes)


def subtract_hours(
    value: datetime,
    hours: int,
) -> datetime:
    """
    Subtract hours from datetime.
    """

    return value - timedelta(hours=hours)


def subtract_days(
    value: datetime,
    days: int,
) -> datetime:
    """
    Subtract days from datetime.
    """

    return value - timedelta(days=days)


###############################################################################
# Elapsed Time
###############################################################################


def elapsed(
    start: datetime,
) -> timedelta:
    """
    Return elapsed time since 'start'.
    """

    return now() - start


###############################################################################
# Exports
###############################################################################

__all__ = [
    "now",
    "today",
    "format_datetime",
    "format_date",
    "format_time",
    "parse_datetime",
    "to_iso",
    "from_iso",
    "timestamp",
    "from_timestamp",
    "seconds_between",
    "minutes_between",
    "hours_between",
    "days_between",
    "add_seconds",
    "add_minutes",
    "add_hours",
    "add_days",
    "subtract_seconds",
    "subtract_minutes",
    "subtract_hours",
    "subtract_days",
    "elapsed",
]