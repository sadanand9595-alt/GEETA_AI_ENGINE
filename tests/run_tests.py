"""
==============================================================================
GEETA AI Engine

File        : run_tests.py
Package     : tests
Description : Test Runner

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

###############################################################################
# Project Root
###############################################################################

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

###############################################################################
# Test Discovery
###############################################################################


def create_test_suite() -> unittest.TestSuite:
    """
    Discover all test modules.
    """

    loader = unittest.TestLoader()

    suite = loader.discover(
        start_dir=str(Path(__file__).parent),
        pattern="test_*.py",
    )

    return suite


###############################################################################
# Run Tests
###############################################################################


def run() -> bool:
    """
    Execute all unit tests.

    Returns:
        True if all tests pass.
    """

    print("=" * 80)
    print("GEETA AI Engine")
    print("Running Unit Tests")
    print("=" * 80)

    suite = create_test_suite()

    runner = unittest.TextTestRunner(
        verbosity=2,
    )

    result = runner.run(suite)

    print("=" * 80)

    print(f"Tests Run     : {result.testsRun}")
    print(f"Failures      : {len(result.failures)}")
    print(f"Errors        : {len(result.errors)}")
    print(f"Skipped       : {len(result.skipped)}")

    print("=" * 80)

    if result.wasSuccessful():

        print("STATUS : ALL TESTS PASSED")

    else:

        print("STATUS : TEST FAILURES DETECTED")

    print("=" * 80)

    return result.wasSuccessful()


###############################################################################
# Entry Point
###############################################################################

if __name__ == "__main__":

    success = run()

    sys.exit(0 if success else 1)