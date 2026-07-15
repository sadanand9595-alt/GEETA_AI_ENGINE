"""
==============================================================================
GEETA AI IDE

File        : document_sync.py
Package     : lsp
Description : LSP Document Synchronization

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from config.logger import get_logger
from lsp.lsp_client import LSPClient

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Document
###############################################################################


@dataclass(slots=True)
class TextDocument:
    """
    Represents an opened document.
    """

    uri: str

    language_id: str

    version: int

    text: str

###############################################################################
# Document Sync
###############################################################################


class DocumentSync:
    """
    LSP document synchronization.

    Responsibilities

    - didOpen
    - didChange
    - didSave
    - didClose
    - Version tracking
    """

    ###########################################################################

    def __init__(
        self,
        client: LSPClient,
    ) -> None:

        self._client = client

        self._documents: dict[
            str,
            TextDocument,
        ] = {}

        logger.info(
            "Document Sync initialized."
        )

###############################################################################
# URI
###############################################################################

    @staticmethod
    def file_uri(
        path: str | Path,
    ) -> str:
        """
        Convert file path to URI.
        """

        return Path(
            path
        ).resolve().as_uri()

###############################################################################
# Open
###############################################################################

    def open(
        self,
        path: str | Path,
        language: str,
        text: str,
    ) -> None:
        """
        Send didOpen.
        """

        uri = self.file_uri(
            path,
        )

        document = TextDocument(
            uri=uri,
            language_id=language,
            version=1,
            text=text,
        )

        self._documents[
            uri
        ] = document

        self._client.send_notification(
            "textDocument/didOpen",
            {
                "textDocument": {
                    "uri": uri,
                    "languageId": language,
                    "version": 1,
                    "text": text,
                }
            },
        )

###############################################################################
# Change
###############################################################################

    def change(
        self,
        path: str | Path,
        text: str,
    ) -> None:
        """
        Send didChange.
        """

        uri = self.file_uri(
            path,
        )

        document = self._documents[
            uri
        ]

        document.version += 1

        document.text = text

        self._client.send_notification(
            "textDocument/didChange",
            {
                "textDocument": {
                    "uri": uri,
                    "version": document.version,
                },
                "contentChanges": [
                    {
                        "text": text,
                    }
                ],
            },
        )

###############################################################################
# Save
###############################################################################

    def save(
        self,
        path: str | Path,
    ) -> None:
        """
        Send didSave.
        """

        uri = self.file_uri(
            path,
        )

        document = self._documents[
            uri
        ]

        self._client.send_notification(
            "textDocument/didSave",
            {
                "textDocument": {
                    "uri": uri,
                },
                "text": document.text,
            },
        )
###############################################################################
# Close
###############################################################################

    def close(
        self,
        path: str | Path,
    ) -> None:
        """
        Send didClose.
        """

        uri = self.file_uri(
            path,
        )

        if uri not in self._documents:

            return

        self._client.send_notification(
            "textDocument/didClose",
            {
                "textDocument": {
                    "uri": uri,
                }
            },
        )

        del self._documents[
            uri
        ]

###############################################################################
# Lookup
###############################################################################

    def document(
        self,
        path: str | Path,
    ) -> TextDocument | None:
        """
        Return tracked document.
        """

        return self._documents.get(
            self.file_uri(path),
        )

###############################################################################
# Documents
###############################################################################

    def documents(
        self,
    ) -> list[TextDocument]:
        """
        Return all tracked documents.
        """

        return list(
            self._documents.values()
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return synchronization statistics.
        """

        return {
            "tracked_documents": len(
                self._documents
            ),
            "versions": sum(
                document.version
                for document
                in self._documents.values()
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Return synchronization report.
        """

        return {
            "statistics": self.statistics(),
            "documents": [
                {
                    "uri": document.uri,
                    "language": document.language_id,
                    "version": document.version,
                }
                for document
                in self._documents.values()
            ],
        }

###############################################################################
# Exports
###############################################################################

__all__ = [
    "TextDocument",
    "DocumentSync",
]