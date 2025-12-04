"""
Groq API Integration - FREE 70B Parameter AI!

This module provides integration with Groq's FREE API for Llama 3.1 70B.
Intelligence level: 8.5/10 (Near GPT-4!)
Cost: $0 (FREE!)
"""

import os
from typing import Optional
from groq import Groq


class GroqChat:
    """Groq API chat handler using Llama 3.1 70B"""

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")

        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"  # 70 BILLION parameters! (Latest model)

    async def chat(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """
        Send a message to Groq's Llama 3.1 70B model

        Args:
            message: User's message
            system_prompt: Optional system prompt
            temperature: Response randomness (0-1)
            max_tokens: Maximum response length

        Returns:
            AI response text
        """

        messages = []

        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
            # Default system prompt
            messages.append({
                "role": "system",
                "content": (
                    "You are Genius AI, an intelligent and helpful assistant. "
                    "Provide clear, accurate, and comprehensive responses. "
                    "Explain complex topics simply when needed. "
                    "Be friendly, professional, and knowledgeable."
                )
            })

        # Add user message
        messages.append({"role": "user", "content": message})

        try:
            # Call Groq API
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            # Extract response
            response = completion.choices[0].message.content

            return response

        except Exception as e:
            # If Groq fails, raise exception so caller can fallback to local model
            raise Exception(f"Groq API error: {str(e)}")

    def test_connection(self) -> bool:
        """Test if Groq API connection works"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10,
            )
            return True
        except Exception:
            return False


# Create singleton instance
groq_chat = GroqChat()


async def chat_with_groq(
    message: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> str:
    """
    Convenience function to chat with Groq

    Usage:
        response = await chat_with_groq("What is biology?")
    """
    return await groq_chat.chat(
        message=message,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
    )
