"""
Creative Genius Agent
Handles creative writing, brainstorming, storytelling
"""

from typing import Optional, Dict
from .base_agent import BaseAgent, AgentResponse


class CreativeAgent(BaseAgent):
    """
    Expert in creative content - stories, poems, ideas, brainstorming
    """

    def __init__(self, core_intelligence):
        super().__init__("CreativeAgent", core_intelligence)
        self.expertise_keywords = [
            "write", "story", "poem", "creative", "imagine", "brainstorm",
            "idea", "invent", "design", "create", "compose", "draft",
            "narrative", "character", "plot", "theme", "metaphor",
            "essay", "article", "blog", "content"
        ]

    async def can_handle(self, message: str) -> float:
        """
        Check if this is a creative request
        """
        msg_lower = message.lower()

        # High confidence creative phrases
        creative_phrases = [
            "write a story", "write a poem", "create a character",
            "help me brainstorm", "give me ideas", "be creative",
            "imagine", "what if", "tell me a story", "compose"
        ]

        if any(phrase in msg_lower for phrase in creative_phrases):
            return 0.95

        # Check for creative content types
        content_types = [
            "story", "poem", "essay", "article", "blog post",
            "script", "dialogue", "narrative", "tale"
        ]

        if any(ctype in msg_lower for ctype in content_types):
            if any(word in msg_lower for word in ["write", "create", "compose", "draft"]):
                return 0.9

        # Standard keyword matching
        return self._calculate_keyword_confidence(message)

    async def process(self, message: str, context: Optional[Dict] = None) -> AgentResponse:
        """
        Process creative request

        Handles:
        - Story writing
        - Poetry
        - Brainstorming
        - Content creation
        - Creative problem-solving
        """
        msg_lower = message.lower()

        # Detect creative type
        if "poem" in msg_lower or "poetry" in msg_lower:
            creative_type = "poetry"
            system_prompt = """You are a masterful poet. Create beautiful, meaningful poetry that:
- Uses vivid imagery and metaphors
- Has rhythm and flow
- Evokes emotion
- Conveys deep meaning
- Demonstrates literary artistry"""

        elif "story" in msg_lower or "narrative" in msg_lower or "tale" in msg_lower:
            creative_type = "storytelling"
            system_prompt = """You are a brilliant storyteller. Craft engaging narratives that:
- Have compelling characters
- Include vivid descriptions
- Build tension and interest
- Have clear structure (beginning, middle, end)
- Engage the reader emotionally"""

        elif "brainstorm" in msg_lower or "ideas" in msg_lower:
            creative_type = "brainstorming"
            system_prompt = """You are a creative genius for brainstorming. Generate ideas that are:
- Original and innovative
- Practical and actionable
- Diverse in perspective
- Well-explained
- Inspiring and thought-provoking"""

        else:
            creative_type = "general_creative"
            system_prompt = """You are a creative expert. Produce creative content that:
- Is original and imaginative
- Engages the audience
- Shows artistic flair
- Communicates effectively
- Demonstrates mastery of the craft"""

        # Generate creative content
        full_prompt = f"""{system_prompt}

**Creative Task**: {message}

**Create something amazing:**"""

        response = await self.core.creative_mode(full_prompt)

        return AgentResponse(
            content=response,
            confidence=0.85,
            agent_name=self.name,
            reasoning="Used creative intelligence and artistic expertise",
            metadata={"creative_type": creative_type}
        )
