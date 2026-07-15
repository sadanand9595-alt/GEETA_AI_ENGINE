"""
GEETA AI ENGINE
Application Entry Point
"""

from __future__ import annotations

import logging
import signal
import sys
from pathlib import Path

from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication, QMessageBox

from core.bootstrap import Bootstrap


APP_NAME = "GEETA AI ENGINE"
APP_VERSION = "3.0"


def configure_logging() -> None:
    """
    Configure application logging.
    """

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(
                log_dir / "geeta.log",
                encoding="utf-8",
            ),
            logging.StreamHandler(),
        ],
    )


def install_exception_handler() -> None:
    """
    Install global exception handler.
    """

    logger = logging.getLogger("geeta")

    def handle_exception(exc_type, exc_value, exc_traceback):

        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(
                exc_type,
                exc_value,
                exc_traceback,
            )
            return

        logger.exception(
            "Unhandled exception",
            exc_info=(
                exc_type,
                exc_value,
                exc_traceback,
            ),
        )

        QMessageBox.critical(
            None,
            APP_NAME,
            str(exc_value),
        )

    sys.excepthook = handle_exception


def main() -> int:

    configure_logging()

    install_exception_handler()

    load_dotenv()

    app = QApplication(sys.argv)

    app.setApplicationName(APP_NAME)

    app.setApplicationVersion(APP_VERSION)

    bootstrap = Bootstrap()

    app.aboutToQuit.connect(bootstrap.shutdown)

    window = bootstrap.initialize()

    window.show()

    signal.signal(
        signal.SIGINT,
        signal.SIG_DFL,
    )

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
