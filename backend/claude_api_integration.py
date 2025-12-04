"""
Claude API Integration for Pawa AI
Adds Claude (Anthropic) as an additional model option
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import anthropic
from datetime import datetime

router = APIRouter(prefix="/claude", tags=["claude"])

# Claude API client (lazy initialization)
_claude_client = None

def get_claude_client():
    """Get or create Claude API client"""
    global _claude_client
    if _claude_client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=500,
                detail="ANTHROPIC_API_KEY not found in environment variables"
            )
        _claude_client = anthropic.Anthropic(api_key=api_key)
    return _claude_client


class ClaudeMessage(BaseModel):
    role: str
    content: str


class ClaudeChatRequest(BaseModel):
    message: str
    conversation_history: List[ClaudeMessage] = []
    model: str = "claude-3-5-sonnet-20241022"  # Latest Claude model
    max_tokens: int = 4096
    temperature: float = 0.7
    system_prompt: Optional[str] = None
    thinking: bool = False  # Enable extended thinking


class ClaudeChatResponse(BaseModel):
    response: str
    model: str
    usage: Dict[str, int]
    thinking_steps: List[str] = []
    timestamp: str


@router.post("/chat", response_model=ClaudeChatResponse)
async def claude_chat(request: ClaudeChatRequest):
    """
    Chat with Claude AI models

    Supports:
    - Claude 3.5 Sonnet (best for coding)
    - Claude 3 Opus (most capable)
    - Claude 3 Sonnet (balanced)
    - Claude 3 Haiku (fastest)
    """
    try:
        client = get_claude_client()

        # Build messages
        messages = []
        for msg in request.conversation_history:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })

        # Add current message
        messages.append({
            "role": "user",
            "content": request.message
        })

        # System prompt (optional)
        system_prompt = request.system_prompt or """You are Pawa AI, an intelligent coding assistant.
You help users write better code, understand complex concepts, and build amazing projects.
Be concise, accurate, and helpful. When generating code, make it production-ready and well-documented."""

        # Call Claude API
        response = client.messages.create(
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            system=system_prompt,
            messages=messages
        )

        # Extract response text
        response_text = ""
        thinking_steps = []

        for content_block in response.content:
            if content_block.type == "text":
                response_text += content_block.text
            elif content_block.type == "thinking" and request.thinking:
                # Claude's extended thinking (if available)
                thinking_steps.append(content_block.text)

        return ClaudeChatResponse(
            response=response_text,
            model=request.model,
            usage={
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            },
            thinking_steps=thinking_steps,
            timestamp=datetime.now().isoformat()
        )

    except anthropic.APIError as e:
        raise HTTPException(status_code=500, detail=f"Claude API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/models")
async def list_claude_models():
    """List available Claude models"""
    return {
        "models": [
            {
                "id": "claude-3-5-sonnet-20241022",
                "name": "Claude 3.5 Sonnet",
                "description": "Most intelligent model, best for coding",
                "context_window": 200000,
                "strengths": ["coding", "reasoning", "analysis"]
            },
            {
                "id": "claude-3-opus-20240229",
                "name": "Claude 3 Opus",
                "description": "Most capable model for complex tasks",
                "context_window": 200000,
                "strengths": ["complex reasoning", "creative writing", "detailed analysis"]
            },
            {
                "id": "claude-3-sonnet-20240229",
                "name": "Claude 3 Sonnet",
                "description": "Balanced performance and speed",
                "context_window": 200000,
                "strengths": ["general purpose", "balanced performance"]
            },
            {
                "id": "claude-3-haiku-20240307",
                "name": "Claude 3 Haiku",
                "description": "Fastest model for quick responses",
                "context_window": 200000,
                "strengths": ["speed", "efficiency", "simple tasks"]
            }
        ]
    }


@router.post("/analyze-code")
async def analyze_code_with_claude(
    code: str,
    language: str,
    analysis_type: str = "review"  # review, optimize, explain, debug
):
    """
    Use Claude to analyze code

    Types:
    - review: Code review with suggestions
    - optimize: Performance optimization suggestions
    - explain: Detailed code explanation
    - debug: Find and fix bugs
    """
    try:
        client = get_claude_client()

        prompts = {
            "review": f"Review this {language} code and provide constructive feedback:\n\n```{language}\n{code}\n```",
            "optimize": f"Analyze this {language} code and suggest performance optimizations:\n\n```{language}\n{code}\n```",
            "explain": f"Explain this {language} code in detail:\n\n```{language}\n{code}\n```",
            "debug": f"Find potential bugs in this {language} code:\n\n```{language}\n{code}\n```"
        }

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": prompts.get(analysis_type, prompts["review"])
            }]
        )

        return {
            "analysis": response.content[0].text,
            "type": analysis_type,
            "language": language
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/health")
async def claude_health_check():
    """Check if Claude API is configured and working"""
    try:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return {
                "status": "not_configured",
                "message": "ANTHROPIC_API_KEY environment variable not set"
            }

        # Test API with a minimal request
        client = get_claude_client()
        client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )

        return {
            "status": "healthy",
            "message": "Claude API is configured and working"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
