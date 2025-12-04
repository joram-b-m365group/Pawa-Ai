"""Conversation memory management."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from genius_ai.core.config import settings
from genius_ai.core.logger import logger


class MessageRole(str, Enum):
    """Message roles in conversation."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"


@dataclass
class Message:
    """Represents a message in conversation."""

    role: MessageRole
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
            "id": self.id,
        }


@dataclass
class ConversationSummary:
    """Summary of conversation history."""

    summary: str
    message_count: int
    timestamp: datetime = field(default_factory=datetime.now)


class ConversationMemory:
    """Manages conversation history with summarization."""

    def __init__(
        self,
        max_messages: int | None = None,
        system_prompt: str | None = None,
    ):
        """Initialize conversation memory.

        Args:
            max_messages: Maximum messages to keep in memory
            system_prompt: System prompt to prepend
        """
        self.max_messages = max_messages or settings.max_conversation_history
        self.system_prompt = system_prompt
        self._messages: list[Message] = []
        self._summaries: list[ConversationSummary] = []

    def add_message(
        self,
        role: MessageRole,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> Message:
        """Add a message to conversation history.

        Args:
            role: Message role
            content: Message content
            metadata: Optional metadata

        Returns:
            Created message
        """
        message = Message(
            role=role,
            content=content,
            metadata=metadata or {},
        )

        self._messages.append(message)

        # Trim if exceeding max
        if len(self._messages) > self.max_messages:
            self._trim_history()

        logger.debug(f"Added {role.value} message to conversation")
        return message

    def add_user_message(self, content: str, metadata: dict[str, Any] | None = None) -> Message:
        """Add user message."""
        return self.add_message(MessageRole.USER, content, metadata)

    def add_assistant_message(
        self, content: str, metadata: dict[str, Any] | None = None
    ) -> Message:
        """Add assistant message."""
        return self.add_message(MessageRole.ASSISTANT, content, metadata)

    def add_system_message(self, content: str, metadata: dict[str, Any] | None = None) -> Message:
        """Add system message."""
        return self.add_message(MessageRole.SYSTEM, content, metadata)

    def get_messages(
        self,
        limit: int | None = None,
        role: MessageRole | None = None,
    ) -> list[Message]:
        """Get conversation messages.

        Args:
            limit: Maximum number of messages
            role: Filter by role

        Returns:
            List of messages
        """
        messages = self._messages

        if role:
            messages = [m for m in messages if m.role == role]

        if limit:
            messages = messages[-limit:]

        return messages

    def get_formatted_history(
        self,
        limit: int | None = None,
        include_system: bool = True,
    ) -> list[dict[str, str]]:
        """Get formatted conversation history for model.

        Args:
            limit: Maximum number of messages
            include_system: Include system prompt

        Returns:
            List of formatted messages
        """
        formatted = []

        # Add system prompt
        if include_system and self.system_prompt:
            formatted.append({
                "role": "system",
                "content": self.system_prompt,
            })

        # Add summaries as context
        for summary in self._summaries:
            formatted.append({
                "role": "system",
                "content": f"Previous conversation summary: {summary.summary}",
            })

        # Add messages
        messages = self.get_messages(limit=limit)
        for message in messages:
            formatted.append({
                "role": message.role.value,
                "content": message.content,
            })

        return formatted

    def _trim_history(self) -> None:
        """Trim history when exceeding max messages."""
        if len(self._messages) <= self.max_messages:
            return

        # Keep most recent messages
        excess = len(self._messages) - self.max_messages
        removed_messages = self._messages[:excess]
        self._messages = self._messages[excess:]

        logger.info(f"Trimmed {excess} messages from conversation history")

        # Note: In a full implementation, we would summarize removed messages
        # For now, just track that they were removed

    def clear(self) -> None:
        """Clear conversation history."""
        self._messages.clear()
        self._summaries.clear()
        logger.info("Cleared conversation memory")

    def get_stats(self) -> dict[str, Any]:
        """Get memory statistics."""
        return {
            "total_messages": len(self._messages),
            "user_messages": len([m for m in self._messages if m.role == MessageRole.USER]),
            "assistant_messages": len(
                [m for m in self._messages if m.role == MessageRole.ASSISTANT]
            ),
            "summaries": len(self._summaries),
        }

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "messages": [m.to_dict() for m in self._messages],
            "summaries": [
                {
                    "summary": s.summary,
                    "message_count": s.message_count,
                    "timestamp": s.timestamp.isoformat(),
                }
                for s in self._summaries
            ],
            "stats": self.get_stats(),
        }
