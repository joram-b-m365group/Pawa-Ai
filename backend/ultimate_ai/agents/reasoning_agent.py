"""
Deep Reasoning Agent
Handles complex logical problems, philosophy, deep thinking
"""

from typing import Optional, Dict
from .base_agent import BaseAgent, AgentResponse


class ReasoningAgent(BaseAgent):
    """
    Expert in logical reasoning, philosophy, complex problem-solving
    """

    def __init__(self, core_intelligence):
        super().__init__("ReasoningAgent", core_intelligence)
        self.expertise_keywords = [
            "why", "how", "explain", "reason", "logic", "philosophy",
            "meaning", "consciousness", "existence", "think", "analyze",
            "understand", "concept", "idea", "theory", "hypothesis",
            "argument", "paradox", "dilemma", "ethics", "morality"
        ]

    async def can_handle(self, message: str) -> float:
        """
        Check if this is a reasoning/philosophical question

        Returns confidence score
        """
        msg_lower = message.lower()

        # High confidence indicators
        if any(phrase in msg_lower for phrase in [
            "why is", "why does", "why do", "how does", "how do",
            "what is the meaning", "what is consciousness", "what is reality",
            "explain why", "explain how", "help me understand"
        ]):
            return 0.95

        # Check for philosophical concepts
        philosophy_terms = [
            "consciousness", "free will", "reality", "existence", "meaning of life",
            "ethics", "morality", "truth", "knowledge", "perception", "mind",
            "soul", "purpose", "destiny", "fate"
        ]
        if any(term in msg_lower for term in philosophy_terms):
            return 0.9

        # Standard keyword matching
        return self._calculate_keyword_confidence(message)

    async def process(self, message: str, context: Optional[Dict] = None) -> AgentResponse:
        """
        Process using deep reasoning

        Uses chain-of-thought reasoning to break down complex problems
        """
        # System prompt for deep reasoning
        system_prompt = """You are a deep reasoning expert. When answering questions:

1. **Break down the question**: Identify what's really being asked
2. **Consider multiple perspectives**: Look at it from different angles
3. **Build logical chains**: Connect ideas step by step
4. **Address complexity**: Don't oversimplify, but be clear
5. **Provide insights**: Go beyond the obvious

Think deeply, reason carefully, and provide thoughtful, nuanced answers.
Be conversational but intellectually rigorous."""

        # Generate response using deep thinking mode
        result = await self.core.think_deeply(f"{system_prompt}\n\nQuestion: {message}")

        reasoning_text = result.get("reasoning", "")

        # Extract key insights for metadata
        metadata = {
            "thinking_mode": "chain_of_thought",
            "complexity": "high",
            "type": "reasoning"
        }

        return AgentResponse(
            content=reasoning_text,
            confidence=0.9,
            agent_name=self.name,
            reasoning="Used deep chain-of-thought reasoning to analyze the question",
            metadata=metadata
        )
