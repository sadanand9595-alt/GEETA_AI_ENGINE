"""
==============================================================================
GEETA AI Engine

File        : database.py
Package     : database
Description : SQLite Database Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator, Optional

from config.logger import get_logger
from config.paths import DATABASE_STORAGE_DIR

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Database Configuration
###############################################################################

DATABASE_STORAGE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_FILE: Path = DATABASE_STORAGE_DIR / "geeta_ai_engine.db"

###############################################################################
# Database Manager
###############################################################################


class DatabaseManager:
    """
    Thread-safe SQLite database manager.

    Responsible for:

    - Database connection
    - Transaction management
    - Query execution
    - Result fetching
    """

    _instance: Optional["DatabaseManager"] = None

    _lock = threading.Lock()

    def __new__(cls) -> "DatabaseManager":
        """
        Singleton implementation.
        """

        if cls._instance is None:

            with cls._lock:

                if cls._instance is None:

                    cls._instance = super().__new__(cls)

        return cls._instance

    ###########################################################################

    def __init__(self) -> None:

        if hasattr(self, "_initialized"):
            return

        self._connection: sqlite3.Connection | None = None

        self._initialized = True

    ###########################################################################

    def connect(self) -> sqlite3.Connection:
        """
        Create or return database connection.
        """

        if self._connection is None:

            logger.info("Connecting database...")

            self._connection = sqlite3.connect(
                DATABASE_FILE,
                check_same_thread=False,
            )

            self._connection.row_factory = sqlite3.Row

            self._connection.execute(
                "PRAGMA foreign_keys = ON;"
            )

            logger.info("Database connected.")

        return self._connection

    ###########################################################################

    def disconnect(self) -> None:
        """
        Close database connection.
        """

        if self._connection is not None:

            logger.info("Closing database connection.")

            self._connection.close()

            self._connection = None

    ###########################################################################

    @property
    def connection(self) -> sqlite3.Connection:
        """
        Return active connection.
        """

        return self.connect()
###########################################################################
    # Execute
    ###########################################################################

    def execute(
        self,
        query: str,
        parameters: tuple[Any, ...] = (),
    ) -> sqlite3.Cursor:
        """
        Execute SQL query.
        """

        cursor = self.connection.cursor()

        cursor.execute(query, parameters)

        self.connection.commit()

        return cursor

    ###########################################################################
    # Execute Many
    ###########################################################################

    def executemany(
        self,
        query: str,
        parameters: list[tuple[Any, ...]],
    ) -> sqlite3.Cursor:
        """
        Execute multiple SQL statements.
        """

        cursor = self.connection.cursor()

        cursor.executemany(query, parameters)

        self.connection.commit()

        return cursor

    ###########################################################################
    # Fetch One
    ###########################################################################

    def fetch_one(
        self,
        query: str,
        parameters: tuple[Any, ...] = (),
    ) -> sqlite3.Row | None:
        """
        Fetch one row.
        """

        cursor = self.connection.cursor()

        cursor.execute(query, parameters)

        return cursor.fetchone()

    ###########################################################################
    # Fetch All
    ###########################################################################

    def fetch_all(
        self,
        query: str,
        parameters: tuple[Any, ...] = (),
    ) -> list[sqlite3.Row]:
        """
        Fetch all rows.
        """

        cursor = self.connection.cursor()

        cursor.execute(query, parameters)

        return cursor.fetchall()

    ###########################################################################
    # Transactions
    ###########################################################################

    def commit(self) -> None:
        """
        Commit current transaction.
        """

        self.connection.commit()

    def rollback(self) -> None:
        """
        Rollback current transaction.
        """

        self.connection.rollback()

    ###########################################################################
    # Context Manager
    ###########################################################################

    @contextmanager
    def transaction(self) -> Generator[sqlite3.Cursor, None, None]:
        """
        Database transaction context manager.
        """

        cursor = self.connection.cursor()

        try:

            yield cursor

            self.connection.commit()

        except Exception:

            self.connection.rollback()

            raise

        finally:

            cursor.close()


###############################################################################
# Global Database Instance
###############################################################################

database = DatabaseManager()

###############################################################################
# Exports
###############################################################################

__all__ = [
    "DatabaseManager",
    "database",
    "DATABASE_FILE",
]