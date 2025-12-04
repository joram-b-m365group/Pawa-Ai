"""
Core Intelligence Layer
Manages the base AI model (LLaMA 3.2) and orchestrates agent communication
"""

import requests
import json
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import asyncio


@dataclass
class Message:
    """Represents a message in the conversation"""
    role: str  # 'user', 'assistant', 'system'
    content: str
    images: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class CoreIntelligence:
    """
    The brain of the system - manages base AI model and coordinates agents
    """

    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "llama3.2"):
        self.ollama_url = ollama_url
        self.model = model
        self.conversation_history: List[Message] = []

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.8,
        max_tokens: int = 2000,
        images: Optional[List[str]] = None
    ) -> str:
        """
        Generate response using the base AI model

        Args:
            prompt: The user's input
            system_prompt: Optional system instructions
            temperature: Creativity level (0.0 - 1.0)
            max_tokens: Maximum response length
            images: Optional list of base64 encoded images

        Returns:
            Generated response text
        """
        try:
            # Build the full prompt with system instructions
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\nUser: {prompt}\n\nAssistant:"

            # Prepare request payload
            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                }
            }

            # Add images if provided (for multimodal models)
            if images:
                payload["images"] = images

            # Call Ollama API
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=120
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                return f"Error: AI model returned status {response.status_code}"

        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to AI model. Please ensure Ollama is running."
        except Exception as e:
            return f"Error generating response: {str(e)}"

    async def chat(
        self,
        message: str,
        history: Optional[List[Message]] = None,
        images: Optional[List[str]] = None,
        temperature: float = 0.8
    ) -> str:
        """
        Chat interface that maintains conversation context

        Args:
            message: User's message
            history: Previous conversation messages
            images: Optional images for this message
            temperature: Response creativity

        Returns:
            AI response
        """
        # Build context from history
        context = ""
        if history:
            for msg in history[-10:]:  # Keep last 10 messages for context
                context += f"{msg.role.capitalize()}: {msg.content}\n"

        # Add current message
        full_prompt = f"{context}User: {message}\nAssistant:"

        # Generate response
        response = await self.generate(
            full_prompt,
            temperature=temperature,
            images=images
        )

        return response

    async def think_deeply(self, problem: str) -> Dict[str, Any]:
        """
        Deep thinking mode - breaks down complex problems

        Args:
            problem: Complex problem to analyze

        Returns:
            Dictionary with reasoning steps and conclusion
        """
        system_prompt = """You are a deep thinking AI. Break down complex problems into steps:
1. Understand the problem
2. Identify key components
3. Analyze each component
4. Synthesize a solution
5. Verify the solution

Think step by step and show your reasoning."""

        response = await self.generate(
            problem,
            system_prompt=system_prompt,
            temperature=0.7
        )

        return {
            "problem": problem,
            "reasoning": response,
            "mode": "deep_thinking"
        }

    async def creative_mode(self, prompt: str) -> str:
        """
        Creative generation mode - for writing, brainstorming, etc.

        Args:
            prompt: Creative prompt

        Returns:
            Creative output
        """
        system_prompt = """You are a creative genius. Generate imaginative, original, and engaging content.
Be creative, think outside the box, and produce high-quality creative work."""

        return await self.generate(
            prompt,
            system_prompt=system_prompt,
            temperature=0.95  # Higher temperature for creativity
        )

    async def analyze_mode(self, content: str) -> Dict[str, Any]:
        """
        Analytical mode - for deep analysis and insights

        Args:
            content: Content to analyze

        Returns:
            Analysis results
        """
        system_prompt = """You are an analytical expert. Provide deep, insightful analysis:
- Identify patterns and trends
- Extract key insights
- Provide actionable conclusions
- Support with evidence and reasoning"""

        analysis = await self.generate(
            f"Analyze this:\n{content}",
            system_prompt=system_prompt,
            temperature=0.6  # Lower temperature for precision
        )

        return {
            "content": content,
            "analysis": analysis,
            "mode": "analytical"
        }

    def check_health(self) -> Dict[str, Any]:
        """
        Check if the AI model is available and healthy

        Returns:
            Health status information
        """
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_available = any(m.get("name", "").startswith(self.model) for m in models)

                return {
                    "status": "healthy",
                    "ollama_running": True,
                    "model_available": model_available,
                    "model_name": self.model,
                    "available_models": [m.get("name") for m in models]
                }
            else:
                return {
                    "status": "unhealthy",
                    "ollama_running": True,
                    "model_available": False,
                    "error": f"Unexpected status: {response.status_code}"
                }
        except requests.exceptions.ConnectionError:
            return {
                "status": "unhealthy",
                "ollama_running": False,
                "model_available": False,
                "error": "Cannot connect to Ollama. Please ensure it's running."
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "ollama_running": False,
                "model_available": False,
                "error": str(e)
            }
