"""
==============================================================================
GEETA AI Engine

File        : symbol_memory.py
Package     : memory
Description : Symbol Memory

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from typing import Any

from config.logger import get_logger
from memory.base_memory import BaseMemory

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Symbol Memory
###############################################################################


class SymbolMemory(BaseMemory):
    """
    Stores project symbols.

    Responsibilities:

    - Classes
    - Functions
    - Methods
    - Variables
    - Imports
    - Constants
    - References
    - Symbol Lookup
    """

    def __init__(self) -> None:

        super().__init__(
            name="symbol_memory",
        )

        self._symbols: dict[
            str,
            dict[str, Any],
        ] = {}

    ###########################################################################

    def store(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store symbol.
        """

        self._symbols[key] = value

    ###########################################################################

    def retrieve(
        self,
        key: str,
    ) -> Any:
        """
        Retrieve symbol.
        """

        return self._symbols.get(key)

    ###########################################################################

    def delete(
        self,
        key: str,
    ) -> None:
        """
        Delete symbol.
        """

        self._symbols.pop(
            key,
            None,
        )

    ###########################################################################

    def clear(
        self,
    ) -> None:
        """
        Clear symbol memory.
        """

        self._symbols.clear()

        logger.info(
            "Symbol memory cleared."
        )

    ###########################################################################

    def add_symbol(
        self,
        name: str,
        symbol_type: str,
        file: str,
        line: int,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Add symbol to memory.
        """

        self.store(
            name,
            {
                "name": name,
                "type": symbol_type,
                "file": file,
                "line": line,
                "metadata": metadata or {},
            },
        )

        logger.info(
            "Indexed symbol: %s",
            name,
        )
###############################################################################
# Symbol Lookup
###############################################################################

    def find(
        self,
        name: str,
    ) -> dict[str, Any] | None:
        """
        Find symbol by name.
        """

        return self.retrieve(
            name,
        )

    ###########################################################################

    def find_by_type(
        self,
        symbol_type: str,
    ) -> list[dict[str, Any]]:
        """
        Return all symbols of the specified type.
        """

        return [
            symbol
            for symbol in self._symbols.values()
            if symbol.get("type") == symbol_type
        ]

    ###########################################################################

    def all_symbols(
        self,
    ) -> list[dict[str, Any]]:
        """
        Return every indexed symbol.
        """

        return list(
            self._symbols.values()
        )

###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, Any]:
        """
        Return symbol memory statistics.
        """

        data = super().statistics()

        data.update(
            {
                "symbols": len(
                    self._symbols
                ),
                "classes": len(
                    self.find_by_type(
                        "class"
                    )
                ),
                "functions": len(
                    self.find_by_type(
                        "function"
                    )
                ),
            }
        )

        return data

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, Any]:
        """
        Build symbol memory report.
        """

        return {
            "metadata": self.metadata(),
            "statistics": self.statistics(),
            "symbols": self.all_symbols(),
        }


###############################################################################
# Exports
###############################################################################

__all__ = [
    "SymbolMemory",
]