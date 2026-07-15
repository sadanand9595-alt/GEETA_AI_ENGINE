"""
==============================================================================
GEETA AI Engine

File        : logger.py
Package     : config
Description : Enterprise Logging System

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional

from config.constants import (
    LOG_INFO,
    MAX_LOG_BACKUP_FILES,
    MAX_LOG_FILE_SIZE_MB,
    PROJECT_NAME,
)
from config.path import LOGS_DIR

###############################################################################
# Log Format
###############################################################################

DEFAULT_LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)-30s | "
    "%(filename)s:%(lineno)d | "
    "%(message)s"
)

DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

###############################################################################
# Log File
###############################################################################

LOG_FILE: Path = LOGS_DIR / "geeta_ai_engine.log"

###############################################################################
# Logger Manager
###############################################################################


class LoggerManager:
    """
    Central logging manager.

    Creates and configures application loggers.
    """

    _configured = False

    @classmethod
    def configure(
        cls,
        level: str = LOG_INFO,
    ) -> None:
        """
        Configure global logging.
        """

        if cls._configured:
            return

        LOGS_DIR.mkdir(parents=True, exist_ok=True)

        formatter = logging.Formatter(
            fmt=DEFAULT_LOG_FORMAT,
            datefmt=DEFAULT_DATE_FORMAT,
        )

        root_logger = logging.getLogger()

        root_logger.setLevel(level)

        root_logger.handlers.clear()

        #######################################################################
        # Console Handler
        #######################################################################

        console_handler = logging.StreamHandler(sys.stdout)

        console_handler.setFormatter(formatter)

        console_handler.setLevel(level)

        #######################################################################
        # Rotating File Handler
        #######################################################################

        file_handler = logging.handlers.RotatingFileHandler(
            filename=LOG_FILE,
            maxBytes=MAX_LOG_FILE_SIZE_MB * 1024 * 1024,
            backupCount=MAX_LOG_BACKUP_FILES,
            encoding="utf-8",
        )

        file_handler.setFormatter(formatter)

        file_handler.setLevel(level)

        #######################################################################
        # Register
        #######################################################################

        root_logger.addHandler(console_handler)

        root_logger.addHandler(file_handler)

        cls._configured = True

    ###########################################################################

    @staticmethod
    def get_logger(
        name: Optional[str] = None,
    ) -> logging.Logger:
        """
        Return configured logger.
        """

        return logging.getLogger(name)


###############################################################################
# Helper Functions
###############################################################################


def configure_logging(
    level: str = LOG_INFO,
) -> None:
    """
    Configure application logging.
    """

    LoggerManager.configure(level)


def get_logger(
    name: Optional[str] = None,
) -> logging.Logger:
    """
    Get logger instance.
    """

    return LoggerManager.get_logger(name)


###############################################################################
# Default Logger
###############################################################################

configure_logging()

logger = get_logger(PROJECT_NAME)

###############################################################################
# Logging Utilities
###############################################################################


def set_log_level(level: str) -> None:
    """
    Update log level for all configured handlers.

    Args:
        level:
            Logging level.
    """

    root_logger = logging.getLogger()

    root_logger.setLevel(level)

    for handler in root_logger.handlers:
        handler.setLevel(level)


def shutdown_logging() -> None:
    """
    Shutdown logging system.
    """

    logging.shutdown()


###############################################################################
# Exception Logging
###############################################################################


def log_exception(
    logger: logging.Logger,
    exception: Exception,
    message: str = "Unhandled exception",
) -> None:
    """
    Log an exception with traceback.

    Args:
        logger:
            Logger instance.

        exception:
            Exception object.

        message:
            Message to display.
    """

    logger.exception("%s: %s", message, exception)


###############################################################################
# Startup Logging
###############################################################################

logger.info("=" * 80)
logger.info("GEETA AI Engine")
logger.info("Enterprise AI Coding & Debugging Engine")
logger.info("Logging System Initialized")
logger.info("Log File : %s", LOG_FILE)
logger.info("=" * 80)

###############################################################################
# Exports
###############################################################################

__all__ = [
    "LoggerManager",
    "configure_logging",
    "get_logger",
    "set_log_level",
    "shutdown_logging",
    "log_exception",
    "logger",
]
