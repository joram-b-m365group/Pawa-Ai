"""
Agent Orchestrator
Routes requests to the best agent and combines their expertise
"""

from typing import List, Dict, Optional, Any
import asyncio
from .core_intelligence import CoreIntelligence, Message
from .agents import (
    ReasoningAgent,
    MathAgent,
    VisionAgent,
    CodeAgent,
    CreativeAgent
)
from .agents.base_agent import AgentResponse


class AgentOrchestrator:
    """
    Orchestrates multiple specialized agents to provide the best response
    """

    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "llama3.2"):
        # Initialize core intelligence
        self.core = CoreIntelligence(ollama_url, model)

        # Initialize all specialized agents
        self.agents = [
            MathAgent(self.core),           # Math gets priority (most specific)
            CodeAgent(self.core),           # Code second (also specific)
            VisionAgent(self.core),         # Vision third (for images)
            CreativeAgent(self.core),       # Creative fourth
            ReasoningAgent(self.core),      # Reasoning last (catches everything else)
        ]

        # Conversation memory
        self.conversations: Dict[str, List[Message]] = {}

    async def process_message(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        images: Optional[List[str]] = None,
        temperature: float = 0.8
    ) -> Dict[str, Any]:
        """
        Process a message by routing to the best agent

        Args:
            message: User's message
            conversation_id: Optional conversation ID for context
            images: Optional images (base64 encoded)
            temperature: Response creativity

        Returns:
            Response dictionary with content and metadata
        """
        # Get conversation history
        history = self.conversations.get(conversation_id, []) if conversation_id else []

        # Check for simple social responses first (human-like conversation)
        social_response = self._handle_social_message(message)
        if social_response:
            # Add to history
            if conversation_id:
                self._add_to_history(conversation_id, message, social_response, "user")

            return {
                "response": social_response,
                "agent": "SocialAgent",
                "confidence": 1.0,
                "type": "social"
            }

        # Build context for agents
        context = {
            "history": history,
            "images": images or [],
            "temperature": temperature
        }

        # If images are present, boost vision agent confidence
        if images:
            # Ask all agents if they can handle this
            agent_scores = await asyncio.gather(*[
                agent.can_handle(message) for agent in self.agents
            ])

            # Boost vision agent score if images present
            for i, agent in enumerate(self.agents):
                if isinstance(agent, VisionAgent):
                    agent_scores[i] = max(agent_scores[i], 0.8)

        else:
            # Ask all agents if they can handle this
            agent_scores = await asyncio.gather(*[
                agent.can_handle(message) for agent in self.agents
            ])

        # Find the best agent
        best_agent_idx = agent_scores.index(max(agent_scores))
        best_agent = self.agents[best_agent_idx]
        best_confidence = agent_scores[best_agent_idx]

        # If no agent is confident enough, use general reasoning
        if best_confidence < 0.3:
            # Use core intelligence directly for general chat
            response_text = await self.core.chat(
                message,
                history=history,
                images=images,
                temperature=temperature
            )

            agent_response = AgentResponse(
                content=response_text,
                confidence=0.5,
                agent_name="GeneralAgent",
                reasoning="General conversation mode"
            )

        else:
            # Let the best agent handle it
            agent_response = await best_agent.process(message, context)

        # Add to conversation history
        if conversation_id:
            self._add_to_history(conversation_id, message, agent_response.content, "user")

        return {
            "response": agent_response.content,
            "agent": agent_response.agent_name,
            "confidence": agent_response.confidence,
            "reasoning": agent_response.reasoning,
            "metadata": agent_response.metadata or {},
            "all_agent_scores": {
                agent.name: score for agent, score in zip(self.agents, agent_scores)
            }
        }

    def _handle_social_message(self, message: str) -> Optional[str]:
        """
        Handle simple social messages for human-like conversation

        Returns response if it's a social message, None otherwise
        """
        msg_lower = message.lower().strip()

        # Greetings
        greetings = {
            "hi": "Hey! How can I help you today?",
            "hello": "Hello! What can I do for you?",
            "hey": "Hey there! What's on your mind?",
            "good morning": "Good morning! How can I assist you today?",
            "good afternoon": "Good afternoon! What can I help you with?",
            "good evening": "Good evening! How may I help you?"
        }

        for greeting, response in greetings.items():
            if msg_lower == greeting or msg_lower == greeting + "!":
                return response

        # How are you variations
        how_are_you = [
            "how are you", "how are you?", "how r u", "how are u",
            "how's it going", "how is it going", "what's up", "whats up",
            "sup", "how you doing"
        ]
        if msg_lower in how_are_you:
            return "I'm doing great, thanks for asking! I'm excited to help you with whatever you need. What's on your mind today?"

        # Thank you
        thanks = ["thank you", "thanks", "thx", "ty", "thank u", "thank you!", "thanks!"]
        if msg_lower in thanks:
            return "You're very welcome! Happy to help anytime. Is there anything else you'd like to explore?"

        # Affirmations
        affirmations = ["ok", "okay", "cool", "nice", "great", "awesome", "perfect"]
        if msg_lower in affirmations or msg_lower in [a + "!" for a in affirmations]:
            return "Sounds good! Anything else I can help you with?"

        # Goodbye
        goodbyes = ["bye", "goodbye", "see you", "see ya", "later", "bye!"]
        if msg_lower in goodbyes:
            return "Goodbye! Feel free to come back anytime you need help. Have a great day!"

        # Simple yes/no
        if msg_lower in ["yes", "yeah", "yep", "yup", "sure"]:
            return "Great! What would you like to do?"

        if msg_lower in ["no", "nope", "nah"]:
            return "No problem! Let me know if you need anything else."

        return None

    def _add_to_history(
        self,
        conversation_id: str,
        user_message: str,
        assistant_response: str,
        role: str = "user"
    ):
        """Add message to conversation history"""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []

        # Add user message
        self.conversations[conversation_id].append(
            Message(role="user", content=user_message)
        )

        # Add assistant response
        self.conversations[conversation_id].append(
            Message(role="assistant", content=assistant_response)
        )

        # Keep only last 50 messages to manage memory
        if len(self.conversations[conversation_id]) > 50:
            self.conversations[conversation_id] = self.conversations[conversation_id][-50:]

    def get_health_status(self) -> Dict[str, Any]:
        """
        Get system health status

        Returns:
            Health information for the system
        """
        core_health = self.core.check_health()

        return {
            "system": "Ultimate Genius AI",
            "core_intelligence": core_health,
            "agents": [agent.name for agent in self.agents],
            "agent_count": len(self.agents),
            "conversations_active": len(self.conversations)
        }

    def clear_conversation(self, conversation_id: str):
        """Clear conversation history"""
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
