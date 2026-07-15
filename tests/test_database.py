"""
==============================================================================
GEETA AI Engine

File        : test_database.py
Package     : tests
Description : Unit Tests for Database Manager

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import unittest

from database.database import DatabaseManager
from database.migrations import initialize_database


class TestDatabaseManager(unittest.TestCase):
    """
    Unit tests for DatabaseManager.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Initialize database before running tests.
        """

        initialize_database()

        cls.database = DatabaseManager()

    ###########################################################################

    def test_connection(self) -> None:
        """
        Verify database connection.
        """

        connection = self.database.connection

        self.assertIsNotNone(connection)

    ###########################################################################

    def test_execute(self) -> None:
        """
        Execute simple SQL statement.
        """

        cursor = self.database.execute(
            "SELECT 1;"
        )

        self.assertIsNotNone(cursor)

    ###########################################################################

    def test_fetch_one(self) -> None:
        """
        Test fetch_one().
        """

        row = self.database.fetch_one(
            "SELECT 1 AS value;"
        )

        self.assertEqual(
            row["value"],
            1,
        )

    ###########################################################################

    def test_fetch_all(self) -> None:
        """
        Test fetch_all().
        """

        rows = self.database.fetch_all(
            """
            SELECT
                1 AS value
            UNION ALL
            SELECT
                2;
            """
        )

        self.assertEqual(
            len(rows),
            2,
        )

    ###########################################################################

    def test_transaction(self) -> None:
        """
        Verify transaction context manager.
        """

        with self.database.transaction() as cursor:

            cursor.execute(
                "SELECT 1;"
            )

        self.assertTrue(True)

    ###########################################################################

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Cleanup.
        """

        cls.database.disconnect()


###############################################################################
# Entry Point
###############################################################################

if __name__ == "__main__":
    unittest.main(verbosity=2)