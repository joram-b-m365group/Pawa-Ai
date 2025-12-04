"""
AI Model Selection System
Allows users to choose between different AI providers and models
Supports: OpenAI (GPT-4), Anthropic (Claude), Groq (Llama)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
from groq import Groq
import httpx
from datetime import datetime

router = APIRouter(prefix="/ai-models", tags=["AI Models"])

# API Keys (should be from environment variables in production)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Initialize clients
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model_provider: str  # openai, anthropic, groq
    model_name: str
    temperature: float = 0.7
    max_tokens: int = 4000
    system_prompt: Optional[str] = None


class ChatResponse(BaseModel):
    content: str
    model_used: str
    provider: str
    tokens_used: Optional[int] = None
    cost_estimate: Optional[float] = None
    latency_ms: Optional[int] = None


class ModelInfo(BaseModel):
    provider: str
    model_id: str
    display_name: str
    description: str
    context_window: int
    cost_per_1k_tokens: Dict[str, float]  # input and output
    features: List[str]
    available: bool


# Available models configuration
AVAILABLE_MODELS = {
    "groq": [
        {
            "provider": "groq",
            "model_id": "llama-3.3-70b-versatile",
            "display_name": "Llama 3.3 70B Versatile",
            "description": "Fast, versatile model great for general tasks",
            "context_window": 128000,
            "cost_per_1k_tokens": {"input": 0.00059, "output": 0.00079},
            "features": ["Fast inference", "Large context", "Code generation", "Function calling"],
            "available": True
        },
        {
            "provider": "groq",
            "model_id": "llama-3.1-70b-versatile",
            "display_name": "Llama 3.1 70B Versatile",
            "description": "Stable version with excellent performance",
            "context_window": 128000,
            "cost_per_1k_tokens": {"input": 0.00059, "output": 0.00079},
            "features": ["Reliable", "Large context", "Multi-language"],
            "available": True
        },
        {
            "provider": "groq",
            "model_id": "mixtral-8x7b-32768",
            "display_name": "Mixtral 8x7B",
            "description": "Mixture of experts model, excellent for reasoning",
            "context_window": 32768,
            "cost_per_1k_tokens": {"input": 0.00024, "output": 0.00024},
            "features": ["Reasoning", "Multi-task", "Cost-effective"],
            "available": True
        }
    ],
    "openai": [
        {
            "provider": "openai",
            "model_id": "gpt-4-turbo-preview",
            "display_name": "GPT-4 Turbo",
            "description": "Most capable GPT-4 model with 128k context",
            "context_window": 128000,
            "cost_per_1k_tokens": {"input": 0.01, "output": 0.03},
            "features": ["Most capable", "Vision support", "JSON mode", "Function calling"],
            "available": bool(OPENAI_API_KEY)
        },
        {
            "provider": "openai",
            "model_id": "gpt-4",
            "display_name": "GPT-4",
            "description": "Original GPT-4 model, highly capable",
            "context_window": 8192,
            "cost_per_1k_tokens": {"input": 0.03, "output": 0.06},
            "features": ["High quality", "Reliable", "Well-tested"],
            "available": bool(OPENAI_API_KEY)
        },
        {
            "provider": "openai",
            "model_id": "gpt-3.5-turbo",
            "display_name": "GPT-3.5 Turbo",
            "description": "Fast and cost-effective",
            "context_window": 16384,
            "cost_per_1k_tokens": {"input": 0.0005, "output": 0.0015},
            "features": ["Fast", "Cost-effective", "Function calling"],
            "available": bool(OPENAI_API_KEY)
        }
    ],
    "anthropic": [
        {
            "provider": "anthropic",
            "model_id": "claude-3-opus-20240229",
            "display_name": "Claude 3 Opus",
            "description": "Most capable Claude model for complex tasks",
            "context_window": 200000,
            "cost_per_1k_tokens": {"input": 0.015, "output": 0.075},
            "features": ["Largest context", "Most capable", "Advanced reasoning"],
            "available": bool(ANTHROPIC_API_KEY)
        },
        {
            "provider": "anthropic",
            "model_id": "claude-3-sonnet-20240229",
            "display_name": "Claude 3 Sonnet",
            "description": "Balanced performance and speed",
            "context_window": 200000,
            "cost_per_1k_tokens": {"input": 0.003, "output": 0.015},
            "features": ["Large context", "Balanced", "Good value"],
            "available": bool(ANTHROPIC_API_KEY)
        },
        {
            "provider": "anthropic",
            "model_id": "claude-3-haiku-20240307",
            "display_name": "Claude 3 Haiku",
            "description": "Fastest Claude model",
            "context_window": 200000,
            "cost_per_1k_tokens": {"input": 0.00025, "output": 0.00125},
            "features": ["Fastest", "Cost-effective", "Large context"],
            "available": bool(ANTHROPIC_API_KEY)
        }
    ]
}


async def call_groq_model(messages: List[ChatMessage], model_name: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
    """Call Groq API"""
    if not groq_client:
        raise HTTPException(status_code=500, detail="Groq API key not configured")

    start_time = datetime.now()

    try:
        response = groq_client.chat.completions.create(
            model=model_name,
            messages=[{"role": msg.role, "content": msg.content} for msg in messages],
            temperature=temperature,
            max_tokens=max_tokens
        )

        latency = (datetime.now() - start_time).total_seconds() * 1000

        return {
            "content": response.choices[0].message.content,
            "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else None,
            "latency_ms": int(latency)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq API error: {str(e)}")


async def call_openai_model(messages: List[ChatMessage], model_name: str, temperature: float, max_tokens: int) -> Dict[str, Any]:
    """Call OpenAI API"""
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")

    start_time = datetime.now()

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model_name,
                    "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
                    "temperature": temperature,
                    "max_tokens": max_tokens
                },
                timeout=60.0
            )

            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)

            data = response.json()
            latency = (datetime.now() - start_time).total_seconds() * 1000

            return {
                "content": data["choices"][0]["message"]["content"],
                "tokens_used": data.get("usage", {}).get("total_tokens"),
                "latency_ms": int(latency)
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")


async def call_anthropic_model(messages: List[ChatMessage], model_name: str, temperature: float, max_tokens: int, system_prompt: Optional[str] = None) -> Dict[str, Any]:
    """Call Anthropic API"""
    if not ANTHROPIC_API_KEY:
        raise HTTPException(status_code=500, detail="Anthropic API key not configured")

    start_time = datetime.now()

    try:
        # Convert messages format for Anthropic
        anthropic_messages = []
        for msg in messages:
            if msg.role != "system":  # System messages handled separately
                anthropic_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

        async with httpx.AsyncClient() as client:
            payload = {
                "model": model_name,
                "messages": anthropic_messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }

            if system_prompt:
                payload["system"] = system_prompt

            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=60.0
            )

            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=response.text)

            data = response.json()
            latency = (datetime.now() - start_time).total_seconds() * 1000

            return {
                "content": data["content"][0]["text"],
                "tokens_used": data.get("usage", {}).get("input_tokens", 0) + data.get("usage", {}).get("output_tokens", 0),
                "latency_ms": int(latency)
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Anthropic API error: {str(e)}")


def calculate_cost(tokens: int, model_provider: str, model_name: str) -> float:
    """Calculate estimated cost based on tokens used"""
    for provider_models in AVAILABLE_MODELS.get(model_provider, []):
        if provider_models["model_id"] == model_name:
            # Rough estimate: assume 50/50 input/output split
            input_cost = (tokens * 0.5 / 1000) * provider_models["cost_per_1k_tokens"]["input"]
            output_cost = (tokens * 0.5 / 1000) * provider_models["cost_per_1k_tokens"]["output"]
            return round(input_cost + output_cost, 6)
    return 0.0


@router.get("/list", response_model=List[ModelInfo])
async def list_available_models():
    """Get list of all available AI models"""
    all_models = []
    for provider, models in AVAILABLE_MODELS.items():
        for model in models:
            all_models.append(ModelInfo(**model))
    return all_models


@router.post("/chat", response_model=ChatResponse)
async def chat_with_model(request: ChatRequest):
    """
    Send a chat message to the selected AI model
    """
    try:
        # Route to appropriate provider
        if request.model_provider == "groq":
            result = await call_groq_model(
                request.messages,
                request.model_name,
                request.temperature,
                request.max_tokens
            )
        elif request.model_provider == "openai":
            result = await call_openai_model(
                request.messages,
                request.model_name,
                request.temperature,
                request.max_tokens
            )
        elif request.model_provider == "anthropic":
            result = await call_anthropic_model(
                request.messages,
                request.model_name,
                request.temperature,
                request.max_tokens,
                request.system_prompt
            )
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported provider: {request.model_provider}")

        # Calculate cost
        cost = calculate_cost(
            result.get("tokens_used", 0),
            request.model_provider,
            request.model_name
        ) if result.get("tokens_used") else None

        return ChatResponse(
            content=result["content"],
            model_used=request.model_name,
            provider=request.model_provider,
            tokens_used=result.get("tokens_used"),
            cost_estimate=cost,
            latency_ms=result.get("latency_ms")
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process chat request: {str(e)}"
        )


@router.get("/compare")
async def compare_models(prompt: str):
    """
    Compare responses from multiple models for the same prompt
    Useful for testing which model works best for specific tasks
    """
    messages = [ChatMessage(role="user", content=prompt)]

    # Test with one model from each available provider
    test_models = []
    if GROQ_API_KEY:
        test_models.append(("groq", "llama-3.3-70b-versatile"))
    if OPENAI_API_KEY:
        test_models.append(("openai", "gpt-3.5-turbo"))
    if ANTHROPIC_API_KEY:
        test_models.append(("anthropic", "claude-3-haiku-20240307"))

    results = []
    for provider, model in test_models:
        try:
            if provider == "groq":
                result = await call_groq_model(messages, model, 0.7, 1000)
            elif provider == "openai":
                result = await call_openai_model(messages, model, 0.7, 1000)
            elif provider == "anthropic":
                result = await call_anthropic_model(messages, model, 0.7, 1000)

            results.append({
                "provider": provider,
                "model": model,
                "response": result["content"][:500],  # First 500 chars
                "latency_ms": result.get("latency_ms"),
                "tokens": result.get("tokens_used")
            })
        except Exception as e:
            results.append({
                "provider": provider,
                "model": model,
                "error": str(e)
            })

    return {"prompt": prompt, "comparisons": results}


@router.get("/status")
async def get_provider_status():
    """Check which AI providers are configured and available"""
    return {
        "groq": {
            "available": bool(GROQ_API_KEY),
            "models_count": len(AVAILABLE_MODELS["groq"])
        },
        "openai": {
            "available": bool(OPENAI_API_KEY),
            "models_count": len(AVAILABLE_MODELS["openai"]) if OPENAI_API_KEY else 0
        },
        "anthropic": {
            "available": bool(ANTHROPIC_API_KEY),
            "models_count": len(AVAILABLE_MODELS["anthropic"]) if ANTHROPIC_API_KEY else 0
        }
    }
