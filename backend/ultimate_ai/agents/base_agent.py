"""
Base Agent Class
All specialized agents inherit from this
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class AgentResponse:
    """Standard response format for all agents"""
    content: str
    confidence: float  # 0.0 - 1.0
    agent_name: str
    reasoning: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class BaseAgent(ABC):
    """
    Base class for all specialized agents
    """

    def __init__(self, name: str, core_intelligence):
        self.name = name
        self.core = core_intelligence
        self.expertise_keywords = []

    @abstractmethod
    async def can_handle(self, message: str) -> float:
        """
        Determine if this agent can handle the message

        Args:
            message: User's message

        Returns:
            Confidence score (0.0 - 1.0) that this agent should handle it
        """
        pass

    @abstractmethod
    async def process(self, message: str, context: Optional[Dict] = None) -> AgentResponse:
        """
        Process the message and generate response

        Args:
            message: User's message
            context: Optional context (history, images, etc.)

        Returns:
            AgentResponse with the result
        """
        pass

    def _calculate_keyword_confidence(self, message: str) -> float:
        """
        Calculate confidence based on keyword matching

        Args:
            message: User's message

        Returns:
            Confidence score based on keyword presence
        """
        msg_lower = message.lower()
        matches = sum(1 for keyword in self.expertise_keywords if keyword in msg_lower)

        if matches == 0:
            return 0.0
        elif matches == 1:
            return 0.5
        elif matches == 2:
            return 0.7
        else:
            return 0.9
