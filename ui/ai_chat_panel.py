"""
==============================================================================
GEETA AI IDE

File        : ai_chat_panel.py
Package     : ui
Description : Enterprise AI Chat Panel

Author      : Sadanand Vishwakarma
License     : MIT
==============================================================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4

from config.logger import get_logger

###############################################################################
# Logger
###############################################################################

logger = get_logger(__name__)

###############################################################################
# Chat Provider
###############################################################################


class ChatProvider(str, Enum):

    GPT = "gpt"

    CLAUDE = "claude"

    GEMINI = "gemini"

    OLLAMA = "ollama"

###############################################################################
# Message Role
###############################################################################


class MessageRole(str, Enum):

    SYSTEM = "system"

    USER = "user"

    ASSISTANT = "assistant"

###############################################################################
# Chat Message
###############################################################################


@dataclass(slots=True)
class ChatMessage:

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    role: MessageRole = (
        MessageRole.USER
    )

    content: str = ""

    timestamp: datetime = field(
        default_factory=datetime.utcnow
    )

###############################################################################
# Chat Session
###############################################################################


@dataclass(slots=True)
class ChatSession:

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    title: str = "New Chat"

    provider: ChatProvider = (
        ChatProvider.GPT
    )

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    messages: list[
        ChatMessage
    ] = field(
        default_factory=list
    )

###############################################################################
# AI Chat Panel
###############################################################################


class AIChatPanel:
    """
    Enterprise AI Chat Panel.

    Features

    - Multi-session chat
    - Provider switching
    - Project context
    - Streaming
    - Attachments
    """

    ###########################################################################

    def __init__(
        self,
    ) -> None:

        self._sessions: dict[
            str,
            ChatSession
        ] = {}

        self._active: str | None = None

        logger.info(
            "AI Chat Panel initialized."
        )

###############################################################################
# Create Session
###############################################################################

    def create_session(
        self,
        title: str = "New Chat",
        provider: ChatProvider = (
            ChatProvider.GPT
        ),
    ) -> ChatSession:
        """
        Create chat session.
        """

        session = ChatSession(
            title=title,
            provider=provider,
        )

        self._sessions[
            session.id
        ] = session

        self._active = session.id

        logger.info(
            "Created chat: %s",
            session.id,
        )

        return session

###############################################################################
# Active Session
###############################################################################

    @property
    def active_session(
        self,
    ) -> ChatSession | None:
        """
        Return active session.
        """

        if self._active is None:

            return None

        return self._sessions.get(
            self._active,
        )

###############################################################################
# Switch Session
###############################################################################

    def switch_session(
        self,
        session_id: str,
    ) -> bool:
        """
        Switch active session.
        """

        if session_id not in self._sessions:

            return False

        self._active = session_id

        return True

###############################################################################
# Send Message
###############################################################################

    async def send(
        self,
        text: str,
    ) -> ChatMessage:
        """
        Send user message.
        """

        session = self.active_session

        if session is None:

            session = self.create_session()

        message = ChatMessage(

            role=MessageRole.USER,

            content=text,
        )

        session.messages.append(
            message,
        )

        logger.info(
            "Message added."
        )

        return message
###############################################################################
# Provider Switch
###############################################################################

    def set_provider(
        self,
        provider: ChatProvider,
    ) -> None:
        """
        Change AI provider.
        """

        session = self.active_session

        if session is None:

            return

        session.provider = provider

        logger.info(
            "Provider changed to %s",
            provider.value,
        )

###############################################################################
# Inject Project Context
###############################################################################

    def inject_context(
        self,
        project_name: str,
        file_path: str,
        prompt: str,
    ) -> str:
        """
        Build project-aware prompt.
        """

        return (
            f"Project: {project_name}\n"
            f"File: {file_path}\n\n"
            f"{prompt}"
        )

###############################################################################
# Stream Response
###############################################################################

    async def stream_response(
        self,
        provider: ChatProvider,
        prompt: str,
    ):
        """
        Stream AI response.
        """

        logger.info(
            "Streaming response from %s",
            provider.value,
        )

        # Provider layer will stream tokens.

        yield ""

###############################################################################
# Markdown Renderer
###############################################################################

    def render_markdown(
        self,
        text: str,
    ) -> str:
        """
        Render markdown.

        UI renderer will process markdown.
        """

        return text

###############################################################################
# Code Block Renderer
###############################################################################

    def render_code(
        self,
        language: str,
        code: str,
    ) -> str:
        """
        Render syntax highlighted code.
        """

        return (
            f"```{language}\n"
            f"{code}\n"
            "```"
        )

###############################################################################
# Conversation History
###############################################################################

    def history(
        self,
        session_id: str,
    ) -> list[ChatMessage]:
        """
        Return chat history.
        """

        session = self._sessions.get(
            session_id,
        )

        if session is None:

            return []

        return list(
            session.messages,
        )

###############################################################################
# Token Counter
###############################################################################

    def token_usage(
        self,
        session_id: str,
    ) -> int:
        """
        Estimate token usage.
        """

        session = self._sessions.get(
            session_id,
        )

        if session is None:

            return 0

        return sum(

            len(message.content.split())

            for message
            in session.messages
        )

###############################################################################
# Cost Estimation
###############################################################################

    def estimated_cost(
        self,
        session_id: str,
        price_per_1k_tokens: float,
    ) -> float:
        """
        Estimate provider cost.
        """

        tokens = self.token_usage(
            session_id,
        )

        return (
            tokens
            / 1000.0
        ) * price_per_1k_tokens
###############################################################################
# File Attachment
###############################################################################

    def attach_file(
        self,
        session_id: str,
        file_path: str,
    ) -> bool:
        """
        Attach file to chat session.
        """

        session = self._sessions.get(
            session_id,
        )

        if session is None:

            return False

        if not hasattr(
            session,
            "attachments",
        ):

            session.attachments = []

        session.attachments.append(
            file_path,
        )

        logger.info(
            "Attached file: %s",
            file_path,
        )

        return True

###############################################################################
# Image Attachment
###############################################################################

    def attach_image(
        self,
        session_id: str,
        image_path: str,
    ) -> bool:
        """
        Attach image.
        """

        return self.attach_file(
            session_id,
            image_path,
        )

###############################################################################
# Search Conversation
###############################################################################

    def search(
        self,
        keyword: str,
    ) -> list[ChatMessage]:
        """
        Search all conversations.
        """

        keyword = keyword.lower()

        results = []

        for session in self._sessions.values():

            for message in session.messages:

                if keyword in message.content.lower():

                    results.append(
                        message,
                    )

        return results

###############################################################################
# Prompt Templates
###############################################################################

    def templates(
        self,
    ) -> dict[str, str]:
        """
        Built-in prompt templates.
        """

        return {

            "review":
                "Review this code.",

            "debug":
                "Find and fix bugs.",

            "refactor":
                "Refactor this code.",

            "document":
                "Generate documentation.",

            "test":
                "Generate unit tests.",

            "explain":
                "Explain this code.",
        }

###############################################################################
# Rename Session
###############################################################################

    def rename_session(
        self,
        session_id: str,
        title: str,
    ) -> bool:
        """
        Rename conversation.
        """

        session = self._sessions.get(
            session_id,
        )

        if session is None:

            return False

        session.title = title

        return True

###############################################################################
# Delete Session
###############################################################################

    def delete_session(
        self,
        session_id: str,
    ) -> bool:
        """
        Delete conversation.
        """

        if session_id not in self._sessions:

            return False

        del self._sessions[
            session_id
        ]

        if self._active == session_id:

            self._active = None

        return True

###############################################################################
# Pin Conversation
###############################################################################

    def pin(
        self,
        session_id: str,
    ) -> None:
        """
        Pin conversation.
        """

        if not hasattr(
            self,
            "_pinned",
        ):

            self._pinned = set()

        self._pinned.add(
            session_id,
        )

###############################################################################
# Favorite Conversation
###############################################################################

    def favorite(
        self,
        session_id: str,
    ) -> None:
        """
        Favorite conversation.
        """

        if not hasattr(
            self,
            "_favorites",
        ):

            self._favorites = set()

        self._favorites.add(
            session_id,
        )
###############################################################################
# Conversation Branch
###############################################################################

    def branch_session(
        self,
        session_id: str,
        title: str,
    ) -> ChatSession:
        """
        Create conversation branch.
        """

        source = self._sessions[
            session_id
        ]

        branch = ChatSession(
            title=title,
            provider=source.provider,
        )

        branch.messages.extend(
            source.messages
        )

        self._sessions[
            branch.id
        ] = branch

        logger.info(
            "Created branch: %s",
            branch.id,
        )

        return branch

###############################################################################
# Provider Failover
###############################################################################

    async def provider_failover(
        self,
        providers: list[ChatProvider],
        prompt: str,
    ) -> str:
        """
        Try providers until one succeeds.
        """

        for provider in providers:

            try:

                async for chunk in self.stream_response(
                    provider,
                    prompt,
                ):

                    if chunk:

                        return chunk

            except Exception:

                logger.exception(
                    "Provider failed: %s",
                    provider.value,
                )

        raise RuntimeError(
            "No provider available."
        )

###############################################################################
# Export Markdown
###############################################################################

    def export_markdown(
        self,
        session_id: str,
    ) -> str:
        """
        Export conversation as Markdown.
        """

        session = self._sessions[
            session_id
        ]

        output = [
            f"# {session.title}",
            "",
        ]

        for message in session.messages:

            output.append(
                f"## {message.role.value}"
            )

            output.append(
                message.content
            )

            output.append("")

        return "\n".join(
            output,
        )

###############################################################################
# Export HTML
###############################################################################

    def export_html(
        self,
        session_id: str,
    ) -> str:
        """
        Export conversation as HTML.
        """

        markdown = self.export_markdown(
            session_id,
        )

        return (
            "<html><body><pre>"
            + markdown
            + "</pre></body></html>"
        )

###############################################################################
# Export PDF
###############################################################################

    def export_pdf(
        self,
        session_id: str,
        output_file: str,
    ) -> bool:
        """
        Export conversation as PDF.

        PDF generation will be delegated
        to the reporting module.
        """

        logger.info(
            "Export PDF: %s",
            output_file,
        )

        return True

###############################################################################
# Session Analytics
###############################################################################

    def analytics(
        self,
        session_id: str,
    ) -> dict[str, int]:
        """
        Session analytics.
        """

        session = self._sessions.get(
            session_id,
        )

        if session is None:

            return {}

        return {

            "messages": len(
                session.messages
            ),

            "tokens": self.token_usage(
                session_id,
            ),

            "attachments": len(
                getattr(
                    session,
                    "attachments",
                    [],
                )
            ),
        }

###############################################################################
# Chat Event
###############################################################################

    def emit(
        self,
        event: str,
        session_id: str,
    ) -> None:
        """
        Emit chat event.
        """

        logger.info(
            "[CHAT] %s -> %s",
            event,
            session_id,
        )
###############################################################################
# Statistics
###############################################################################

    def statistics(
        self,
    ) -> dict[str, int]:
        """
        Return chat statistics.
        """

        total_messages = sum(
            len(session.messages)
            for session
            in self._sessions.values()
        )

        return {
            "sessions": len(
                self._sessions
            ),
            "messages": total_messages,
            "pinned": len(
                getattr(
                    self,
                    "_pinned",
                    set(),
                )
            ),
            "favorites": len(
                getattr(
                    self,
                    "_favorites",
                    set(),
                )
            ),
        }

###############################################################################
# Report
###############################################################################

    def report(
        self,
    ) -> dict[str, object]:
        """
        Generate chat report.
        """

        return {
            "statistics": self.statistics(),
            "active_session": self._active,
            "providers": list(
                {
                    session.provider.value
                    for session
                    in self._sessions.values()
                }
            ),
        }

###############################################################################
# Cleanup
###############################################################################

    def cleanup(
        self,
    ) -> None:
        """
        Reset chat panel.
        """

        self._sessions.clear()

        self._active = None

        if hasattr(
            self,
            "_favorites",
        ):
            self._favorites.clear()

        if hasattr(
            self,
            "_pinned",
        ):
            self._pinned.clear()

        logger.info(
            "AI Chat Panel cleaned."
        )

###############################################################################
# VS Code Integration
###############################################################################

    async def sync_vscode(
        self,
    ) -> None:
        """
        Synchronize with VS Code chat view.
        """

        logger.info(
            "Synchronizing AI Chat Panel."
        )

###############################################################################
# AI Agent Integration
###############################################################################

    async def sync_agents(
        self,
    ) -> None:
        """
        Notify AI agent subsystem.
        """

        logger.info(
            "Synchronizing AI agents."
        )

###############################################################################
# Telemetry
###############################################################################

    def telemetry(
        self,
    ) -> dict[str, object]:
        """
        Collect chat telemetry.
        """

        return {
            "statistics": self.statistics(),
            "active": self._active,
            "provider_count": len(
                {
                    session.provider.value
                    for session
                    in self._sessions.values()
                }
            ),
        }

###############################################################################
# Global Chat Panel
###############################################################################

ai_chat_panel: (
    AIChatPanel | None
) = None

###############################################################################
# Exports
###############################################################################

__all__ = [
    "ChatProvider",
    "MessageRole",
    "ChatMessage",
    "ChatSession",
    "AIChatPanel",
    "ai_chat_panel",
]