"""
==============================================================================
GEETA AI IDE

File        : lsp_engine.py
Package     : lsp
Description : Enterprise LSP Engine

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from config.logger import get_logger

from lsp.lsp_client import LSPClient
from lsp.lsp_server_manager import LSPServerManager
from lsp.document_sync import DocumentSync

from lsp.hover_provider import HoverProvider
from lsp.definition_provider import DefinitionProvider
from lsp.reference_provider import ReferenceProvider
from lsp.rename_provider import RenameProvider
from lsp.code_action_provider import CodeActionProvider
from lsp.signature_help_provider import SignatureHelpProvider
from lsp.semantic_tokens_provider import SemanticTokensProvider
from lsp.document_symbols_provider import (
    DocumentSymbolsProvider,
)
from lsp.workspace_symbols_provider import (
    WorkspaceSymbolsProvider,
)
from lsp.implementation_provider import (
    ImplementationProvider,
)
from lsp.type_definition_provider import (
    TypeDefinitionProvider,
)
from lsp.call_hierarchy_provider import (
    CallHierarchyProvider,
)
from lsp.inlay_hint_provider import (
    InlayHintProvider,
)
from lsp.code_lens_provider import (
    CodeLensProvider,
)
from lsp.folding_range_provider import (
    FoldingRangeProvider,
)
from lsp.selection_range_provider import (
    SelectionRangeProvider,
)
from lsp.linked_editing_provider import (
    LinkedEditingProvider,
)
from lsp.color_provider import (
    ColorProvider,
)
from lsp.moniker_provider import (
    MonikerProvider,
)
from lsp.progress_manager import (
    ProgressManager,
)
from lsp.workspace_diagnostics import (
    WorkspaceDiagnostics,
)

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Enterprise LSP Engine
###############################################################################


class LSPEngine:
    """
    Central Language Intelligence Engine.

    Responsibilities

    - LSP lifecycle
    - Provider registry
    - Request routing
    - Background synchronization
    - Diagnostics
    - Progress
    - Workspace integration
    """

    ###########################################################################

    def __init__(self) -> None:

        logger.info(
            "Initializing Enterprise LSP Engine..."
        )

        #######################################################
        # Core
        #######################################################

        self.server_manager = LSPServerManager()

        self.client = LSPClient()

        self.document_sync = DocumentSync(
            self.client,
        )

        #######################################################
        # Providers
        #######################################################

        self.hover = HoverProvider(self.client)

        self.definition = DefinitionProvider(
            self.client,
        )

        self.reference = ReferenceProvider(
            self.client,
        )

        self.rename = RenameProvider(
            self.client,
        )

        self.code_action = CodeActionProvider(
            self.client,
        )

        self.signature_help = (
            SignatureHelpProvider(
                self.client,
            )
        )

        self.semantic_tokens = (
            SemanticTokensProvider(
                self.client,
            )
        )

        self.document_symbols = (
            DocumentSymbolsProvider(
                self.client,
            )
        )

        self.workspace_symbols = (
            WorkspaceSymbolsProvider(
                self.client,
            )
        )

        self.implementation = (
            ImplementationProvider(
                self.client,
            )
        )

        self.type_definition = (
            TypeDefinitionProvider(
                self.client,
            )
        )

        self.call_hierarchy = (
            CallHierarchyProvider(
                self.client,
            )
        )

        self.inlay_hint = (
            InlayHintProvider(
                self.client,
            )
        )
        self.code_lens = (
            CodeLensProvider(
                self.client,
            )
        )

        self.folding = (
            FoldingRangeProvider(
                self.client,
            )
        )

        self.selection = (
            SelectionRangeProvider(
                self.client,
            )
        )

        self.linked_editing = (
            LinkedEditingProvider(
                self.client,
            )
        )

        self.color = (
            ColorProvider(
                self.client,
            )
        )

        self.moniker = (
            MonikerProvider(
                self.client,
            )
        )

        #######################################################
        # Managers
        #######################################################

        self.progress = ProgressManager()

        self.workspace_diagnostics = (
            WorkspaceDiagnostics()
        )

        #######################################################
        # Provider Registry
        #######################################################

        self.providers = {
            "hover": self.hover,
            "definition": self.definition,
            "reference": self.reference,
            "rename": self.rename,
            "code_action": self.code_action,
            "signature_help": self.signature_help,
            "semantic_tokens": self.semantic_tokens,
            "document_symbols": self.document_symbols,
            "workspace_symbols": self.workspace_symbols,
            "implementation": self.implementation,
            "type_definition": self.type_definition,
            "call_hierarchy": self.call_hierarchy,
            "inlay_hint": self.inlay_hint,
            "code_lens": self.code_lens,
            "folding": self.folding,
            "selection": self.selection,
            "linked_editing": self.linked_editing,
            "color": self.color,
            "moniker": self.moniker,
        }

        logger.info(
            "LSP Engine initialized."
        )

###############################################################################
# Start
###############################################################################

    def start(
        self,
    ) -> None:
        """
        Start the LSP Engine.
        """

        logger.info(
            "Starting LSP Engine..."
        )

        self.server_manager.start_all()

###############################################################################
# Shutdown
###############################################################################

    def shutdown(
        self,
    ) -> None:
        """
        Shutdown the LSP Engine.
        """

        logger.info(
            "Stopping LSP Engine..."
        )

        self.server_manager.stop_all()

###############################################################################
# Restart
###############################################################################

    def restart(
        self,
    ) -> None:
        """
        Restart the LSP Engine.
        """

        logger.info(
            "Restarting LSP Engine..."
        )

        self.shutdown()

        self.start()

###############################################################################
# Health Check
###############################################################################

    def health(
        self,
    ) -> dict[str, object]:
        """
        Return engine health.
        """

        return {
            "providers": len(
                self.providers,
            ),
            "running": (
                self.server_manager
                is not None
            ),
            "diagnostics": (
                self.workspace_diagnostics
                .statistics()
            ),
            "progress": (
                self.progress
                .statistics()
            ),
        }
        self.code_lens = (
            CodeLensProvider(
                self.client,
            )
        )

        self.folding = (
            FoldingRangeProvider(
                self.client,
            )
        )

        self.selection = (
            SelectionRangeProvider(
                self.client,
            )
        )

        self.linked_editing = (
            LinkedEditingProvider(
                self.client,
            )
        )

        self.color = (
            ColorProvider(
                self.client,
            )
        )

        self.moniker = (
            MonikerProvider(
                self.client,
            )
        )

        #######################################################
        # Managers
        #######################################################

        self.progress = ProgressManager()

        self.workspace_diagnostics = (
            WorkspaceDiagnostics()
        )

        #######################################################
        # Provider Registry
        #######################################################

        self.providers = {
            "hover": self.hover,
            "definition": self.definition,
            "reference": self.reference,
            "rename": self.rename,
            "code_action": self.code_action,
            "signature_help": self.signature_help,
            "semantic_tokens": self.semantic_tokens,
            "document_symbols": self.document_symbols,
            "workspace_symbols": self.workspace_symbols,
            "implementation": self.implementation,
            "type_definition": self.type_definition,
            "call_hierarchy": self.call_hierarchy,
            "inlay_hint": self.inlay_hint,
            "code_lens": self.code_lens,
            "folding": self.folding,
            "selection": self.selection,
            "linked_editing": self.linked_editing,
            "color": self.color,
            "moniker": self.moniker,
        }

        logger.info(
            "LSP Engine initialized."
        )

###############################################################################
# Start
###############################################################################

    def start(
        self,
    ) -> None:
        """
        Start the LSP Engine.
        """

        logger.info(
            "Starting LSP Engine..."
        )

        self.server_manager.start_all()

###############################################################################
# Shutdown
###############################################################################

    def shutdown(
        self,
    ) -> None:
        """
        Shutdown the LSP Engine.
        """

        logger.info(
            "Stopping LSP Engine..."
        )

        self.server_manager.stop_all()

###############################################################################
# Restart
###############################################################################

    def restart(
        self,
    ) -> None:
        """
        Restart the LSP Engine.
        """

        logger.info(
            "Restarting LSP Engine..."
        )

        self.shutdown()

        self.start()

###############################################################################
# Health Check
###############################################################################

    def health(
        self,
    ) -> dict[str, object]:
        """
        Return engine health.
        """

        return {
            "providers": len(
                self.providers,
            ),
            "running": (
                self.server_manager
                is not None
            ),
            "diagnostics": (
                self.workspace_diagnostics
                .statistics()
            ),
            "progress": (
                self.progress
                .statistics()
            ),
        }