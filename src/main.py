"""
==============================================================================
GEETA AI Engine

File        : main.py
Description : Application Entry Point

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

import sys

from config.logger import get_logger
from core.application import application
from core.bootstrap import initialize, shutdown

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Main
###############################################################################


def main() -> int:
    """
    Main application entry point.

    Returns:
        Exit code.
    """

    try:

        logger.info("=" * 80)
        logger.info("Starting GEETA AI Engine")
        logger.info("=" * 80)

        #######################################################################
        # Bootstrap
        #######################################################################

        initialize()

        #######################################################################
        # Start Application
        #######################################################################

        application.run()

        return 0

    except KeyboardInterrupt:

        logger.warning("Application interrupted by user.")

        return 0

    except Exception:

        logger.exception("Fatal application error.")

        return 1

    finally:

        logger.info("Cleaning up application resources...")

        shutdown()

        logger.info("Application shutdown completed.")

        logger.info("=" * 80)


###############################################################################
# Entry Point
###############################################################################

if __name__ == "__main__":
    sys.exit(main())