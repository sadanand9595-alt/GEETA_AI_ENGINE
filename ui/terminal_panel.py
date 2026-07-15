"""
GEETA AI ENGINE
Integrated Terminal
"""

from __future__ import annotations

import os
import platform
import logging

from PySide6.QtCore import (
    QProcess,
    Slot,
)

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPlainTextEdit,
    QLineEdit,
    QPushButton,
)

logger = logging.getLogger(__name__)


class TerminalPanel(QWidget):
    """
    Professional Integrated Terminal
    """

    ##################################################################

    def __init__(
        self,
        parent=None,
    ) -> None:

        super().__init__(parent)

        self.current_directory = os.getcwd()

        self.command_history: list[str] = []

        self.history_index = -1

        self.process = QProcess(self)

        self.setup_ui()

        self.setup_process()

    ##################################################################

    def setup_ui(
        self,
    ) -> None:

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            2,
            2,
            2,
            2,
        )

        self.output = QPlainTextEdit()

        self.output.setReadOnly(True)

        self.output.setLineWrapMode(
            QPlainTextEdit.NoWrap,
        )

        self.input = QLineEdit()

        self.input.setPlaceholderText(
            "Enter command..."
        )

        button_layout = QHBoxLayout()

        self.run_button = QPushButton("Run")

        self.stop_button = QPushButton("Stop")

        self.clear_button = QPushButton("Clear")

        button_layout.addWidget(
            self.run_button,
        )

        button_layout.addWidget(
            self.stop_button,
        )

        button_layout.addStretch()

        button_layout.addWidget(
            self.clear_button,
        )

        layout.addWidget(
            self.output,
        )

        layout.addLayout(
            button_layout,
        )

        layout.addWidget(
            self.input,
        )

        self.output.appendPlainText(
            "======================================"
        )

        self.output.appendPlainText(
            "GEETA AI ENGINE Terminal"
        )

        self.output.appendPlainText(
            f"OS : {platform.system()}"
        )

        self.output.appendPlainText(
            f"Working Directory : {self.current_directory}"
        )

        self.output.appendPlainText(
            "======================================"
        )

        self.input.returnPressed.connect(
            self.execute_command,
        )

        self.run_button.clicked.connect(
            self.execute_command,
        )

        self.clear_button.clicked.connect(
            self.output.clear,
        )

        self.stop_button.clicked.connect(
            self.stop_process,
        )

    ##################################################################

    def setup_process(
        self,
    ) -> None:

        self.process.readyReadStandardOutput.connect(
            self.read_stdout,
        )

        self.process.readyReadStandardError.connect(
            self.read_stderr,
        )

        self.process.finished.connect(
            self.process_finished,
        )
        ##################################################################
    # Execute Command
    ##################################################################

    @Slot()
    def execute_command(
        self,
    ) -> None:

        command = self.input.text().strip()

        if not command:
            return

        self.command_history.append(command)
        self.history_index = len(self.command_history)

        self.output.appendPlainText(
            f"\n{self.current_directory}> {command}"
        )

        self.input.clear()

        ##############################################################
        # Built-in Commands
        ##############################################################

        if command.lower() in ("cls", "clear"):

            self.output.clear()

            return

        if command.lower() == "pwd":

            self.output.appendPlainText(
                self.current_directory,
            )

            return

        if command.startswith("cd "):

            folder = command[3:].strip()

            if not os.path.isabs(folder):

                folder = os.path.join(
                    self.current_directory,
                    folder,
                )

            folder = os.path.abspath(folder)

            if os.path.isdir(folder):

                self.current_directory = folder

                self.output.appendPlainText(
                    self.current_directory,
                )

            else:

                self.output.appendPlainText(
                    "Directory not found.",
                )

            return

        ##############################################################
        # Execute External Command
        ##############################################################

        self.process.setWorkingDirectory(
            self.current_directory,
        )

        if platform.system() == "Windows":

            self.process.start(
                "cmd",
                [
                    "/c",
                    command,
                ],
            )

        else:

            self.process.start(
                "/bin/bash",
                [
                    "-c",
                    command,
                ],
            )

    ##################################################################
    # Output
    ##################################################################

    @Slot()
    def read_stdout(
        self,
    ) -> None:

        text = bytes(
            self.process.readAllStandardOutput(),
        ).decode(
            errors="ignore",
        )

        if text:

            self.output.appendPlainText(
                text.rstrip(),
            )

    ##################################################################

    @Slot()
    def read_stderr(
        self,
    ) -> None:

        text = bytes(
            self.process.readAllStandardError(),
        ).decode(
            errors="ignore",
        )

        if text:

            self.output.appendPlainText(
                text.rstrip(),
            )
            ##################################################################
    # Process Finished
    ##################################################################

    @Slot(
        int,
        QProcess.ExitStatus,
    )
    def process_finished(
        self,
        exit_code: int,
        exit_status,
    ) -> None:

        self.output.appendPlainText(
            f"\n[Process Finished : Exit Code {exit_code}]"
        )

        logger.info(
            "Process finished (%s)",
            exit_code,
        )

    ##################################################################
    # Stop Process
    ##################################################################

    def stop_process(
        self,
    ) -> None:

        if self.process.state() != QProcess.NotRunning:

            self.process.kill()

            self.output.appendPlainText(
                "[Process Terminated]"
            )

    ##################################################################
    # Clear Terminal
    ##################################################################

    def clear_terminal(
        self,
    ) -> None:

        self.output.clear()

    ##################################################################
    # Run From Code
    ##################################################################

    def run_command(
        self,
        command: str,
    ) -> None:

        self.input.setText(
            command,
        )

        self.execute_command()