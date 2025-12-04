"""
Vision Expert Agent
Handles image analysis, visual understanding
"""

from typing import Optional, Dict, List
from .base_agent import BaseAgent, AgentResponse


class VisionAgent(BaseAgent):
    """
    Expert in understanding images, diagrams, charts, visual content
    """

    def __init__(self, core_intelligence):
        super().__init__("VisionAgent", core_intelligence)
        self.expertise_keywords = [
            "image", "picture", "photo", "diagram", "chart", "graph",
            "visual", "see", "look", "show", "screenshot", "drawing",
            "illustration", "infographic", "plot", "figure"
        ]

    async def can_handle(self, message: str) -> float:
        """
        Check if this requires image understanding
        """
        # If images are present in context, high confidence
        # This will be checked by orchestrator

        msg_lower = message.lower()

        # Phrases indicating image analysis
        vision_phrases = [
            "what is in", "what's in", "describe this", "analyze this image",
            "what do you see", "look at", "in this image", "in this picture",
            "in this photo", "what does this show"
        ]

        if any(phrase in msg_lower for phrase in vision_phrases):
            return 0.95

        # Standard keyword matching
        return self._calculate_keyword_confidence(message)

    async def process(self, message: str, context: Optional[Dict] = None) -> AgentResponse:
        """
        Process image-related question

        Args:
            message: User's question about image
            context: Should contain 'images' key with base64 encoded images
        """
        images = context.get("images", []) if context else []

        if not images:
            return AgentResponse(
                content="I'd be happy to analyze images! Please upload an image and I'll describe what I see.",
                confidence=0.5,
                agent_name=self.name,
                reasoning="No images provided"
            )

        # System prompt for vision analysis
        system_prompt = """You are a vision expert. When analyzing images:

1. **Describe what you see**: Objects, people, scenes, text
2. **Identify key elements**: Important details and features
3. **Understand context**: What's happening, the purpose
4. **Extract information**: Text, data, patterns
5. **Be detailed but clear**: Thorough yet understandable

Provide comprehensive image analysis that helps the user understand the visual content."""

        # For now, provide intelligent fallback
        # In production, this would connect to a vision model (LLaMA 3.2-Vision, LLaVA, etc.)

        response_text = """I can see you've uploaded an image!

**Vision Analysis Coming Soon:**
To fully analyze images, I need a multimodal model like:
- LLaMA 3.2-Vision (11B or 90B)
- LLaVA (Large Language and Vision Assistant)
- Bakllava (Vision + LLaMA)

**For now, I can:**
- Guide you through setting up vision models
- Explain what's in images if you describe them
- Help with image-related questions

**To enable full vision:**
1. Install a vision-capable model:
   ```
   ollama pull llava
   ```
   or
   ```
   ollama pull llama3.2-vision
   ```

2. I'll automatically use it for image analysis!

What would you like to know about the image? Describe it to me and I can provide relevant insights!"""

        return AgentResponse(
            content=response_text,
            confidence=0.7,
            agent_name=self.name,
            reasoning="Vision model not yet configured",
            metadata={"images_count": len(images), "status": "vision_model_needed"}
        )

    async def analyze_with_vision_model(self, message: str, images: List[str]) -> str:
        """
        Analyze images using vision-capable model

        This is a placeholder for when vision models are available

        Args:
            message: User's question
            images: Base64 encoded images

        Returns:
            Vision analysis response
        """
        # This would use llava or llama3.2-vision when available
        system_prompt = """Analyze this image in detail:
- What objects/people do you see?
- What is happening in the scene?
- Any text or important details?
- Context and purpose of the image?"""

        # Call vision model (placeholder)
        response = await self.core.generate(
            f"{system_prompt}\n\nUser question: {message}",
            images=images,
            temperature=0.7
        )

        return response
