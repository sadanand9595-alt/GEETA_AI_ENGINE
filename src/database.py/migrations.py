"""
==============================================================================
GEETA AI Engine

File        : migrations.py
Package     : database
Description : Database Schema Migration Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from pathlib import Path

from config.logger import get_logger
from config.paths import PROJECT_ROOT
from database.database import database

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Schema
###############################################################################

SCHEMA_FILE: Path = (
    PROJECT_ROOT
    / "src"
    / "database"
    / "schema.sql"
)

###############################################################################
# Migration Manager
###############################################################################


class MigrationManager:
    """
    Executes database schema migrations.
    """

    def __init__(self) -> None:

        self._database = database

    ###########################################################################

    def schema_exists(self) -> bool:
        """
        Verify schema.sql exists.
        """

        return SCHEMA_FILE.exists()

    ###########################################################################

    def load_schema(self) -> str:
        """
        Read schema.sql.
        """

        if not self.schema_exists():

            raise FileNotFoundError(
                f"Schema not found: {SCHEMA_FILE}"
            )

        return SCHEMA_FILE.read_text(
            encoding="utf-8"
        )

    ###########################################################################

    def migrate(self) -> None:
        """
        Execute schema migration.
        """

        logger.info("Running database migrations...")

        schema = self.load_schema()

        connection = self._database.connection

        connection.executescript(schema)

        connection.commit()

        logger.info("Database migration completed successfully.")

        ###############################################################################
# Database Initialization
###############################################################################


    def initialize(self) -> None:
        """
        Initialize database.

        Creates the database schema if it has not already been applied.
        """

        logger.info("Initializing database...")

        self.migrate()

        logger.info("Database initialization complete.")


###############################################################################
# Database Reset
###############################################################################


    def reset(self) -> None:
        """
        Reset the database.

        WARNING:
            This permanently removes all data.
        """

        logger.warning("Resetting database...")

        connection = self._database.connection

        cursor = connection.cursor()

        cursor.execute("PRAGMA foreign_keys = OFF;")

        cursor.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table';"
        )

        tables = cursor.fetchall()

        for table in tables:

            table_name = table["name"]

            if table_name == "sqlite_sequence":
                continue

            cursor.execute(
                f"DROP TABLE IF EXISTS {table_name};"
            )

        connection.commit()

        cursor.execute("PRAGMA foreign_keys = ON;")

        self.migrate()

        logger.info("Database reset completed successfully.")


###############################################################################
# Validation
###############################################################################


    def validate(self) -> bool:
        """
        Validate database schema.

        Returns:
            True if schema file exists.
        """

        valid = self.schema_exists()

        if valid:
            logger.info("Schema validation successful.")
        else:
            logger.error("Schema validation failed.")

        return valid


###############################################################################
# Global Instance
###############################################################################

migration_manager = MigrationManager()


###############################################################################
# Helper Functions
###############################################################################


def initialize_database() -> None:
    """
    Initialize the application database.
    """

    migration_manager.initialize()


def reset_database() -> None:
    """
    Reset the application database.
    """

    migration_manager.reset()


###############################################################################
# Exports
###############################################################################

__all__ = [
    "MigrationManager",
    "migration_manager",
    "initialize_database",
    "reset_database",
]