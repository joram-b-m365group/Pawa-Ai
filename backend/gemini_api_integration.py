"""
Google Gemini API Integration for Pawa AI
Provides 2 MILLION token context window for FREE!
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import google.generativeai as genai
from datetime import datetime

router = APIRouter(prefix="/gemini", tags=["gemini"])

# Gemini API client (lazy initialization)
_gemini_configured = False


def configure_gemini():
    """Configure Gemini API"""
    global _gemini_configured
    if not _gemini_configured:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=500,
                detail="GOOGLE_API_KEY not found in environment variables. Get free key from https://aistudio.google.com/"
            )
        genai.configure(api_key=api_key)
        _gemini_configured = True


class GeminiMessage(BaseModel):
    role: str  # 'user' or 'model'
    content: str


class GeminiChatRequest(BaseModel):
    message: str
    conversation_history: List[GeminiMessage] = []
    model: str = "gemini-2.0-flash"  # Gemini 2.0 Flash - fast and modern
    temperature: float = 0.7
    system_prompt: Optional[str] = None


class GeminiChatResponse(BaseModel):
    response: str
    model: str
    usage: Dict[str, int]
    timestamp: str


@router.post("/chat", response_model=GeminiChatResponse)
async def gemini_chat(request: GeminiChatRequest):
    """
    Chat with Google Gemini (2 MILLION token context - FREE!)

    Automatically falls back to Groq if Gemini quota exceeded.

    Available Models:
    - gemini-2.0-flash: 1M tokens, fast and reliable
    - gemini-1.5-pro-latest: 2M tokens context, best quality
    - gemini-1.5-flash-latest: 1M tokens, faster
    """

    # Try multiple models in order if quota exceeded
    models_to_try = [
        request.model,  # User's requested model
        "gemini-1.5-flash",  # Fallback 1
        "gemini-1.5-pro",  # Fallback 2
    ]

    last_error = None

    for model_name in models_to_try:
        try:
            configure_gemini()

            # Initialize model
            generation_config = {
                "temperature": request.temperature,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192,
            }

            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]

            model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=generation_config,
                safety_settings=safety_settings,
                system_instruction=request.system_prompt or "You are Pawa AI, an intelligent coding assistant."
            )

            # Build conversation history
            history = []
            for msg in request.conversation_history:
                history.append({
                    "role": msg.role,
                    "parts": [msg.content]
                })

            # Start chat
            chat = model.start_chat(history=history)

            # Send message
            response = chat.send_message(request.message)

            # Count tokens (approximate)
            prompt_tokens = len(request.message.split()) * 1.3  # Rough estimate
            completion_tokens = len(response.text.split()) * 1.3

            return GeminiChatResponse(
                response=response.text,
                model=model_name,
                usage={
                    "prompt_tokens": int(prompt_tokens),
                    "completion_tokens": int(completion_tokens),
                    "total_tokens": int(prompt_tokens + completion_tokens)
                },
                timestamp=datetime.now().isoformat()
            )

        except Exception as e:
            last_error = e
            error_str = str(e).lower()

            # Check if it's a quota error
            if "quota" in error_str or "429" in error_str or "resource exhausted" in error_str:
                print(f"⚠️ Model {model_name} quota exceeded, trying next model...")
                continue

            # If not a quota error, raise immediately
            if "API_KEY" in str(e):
                raise HTTPException(
                    status_code=500,
                    detail=f"Gemini API key error. Get free key from https://aistudio.google.com/. Error: {str(e)}"
                )

            # Other errors should try next model
            print(f"⚠️ Model {model_name} failed: {str(e)}, trying next model...")
            continue

    # If all Gemini models failed, fall back to Groq
    try:
        from groq import Groq
        print("🔄 All Gemini models failed, falling back to Groq...")

        groq_client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

        # Build messages for Groq
        messages = [{"role": "system", "content": request.system_prompt or "You are Pawa AI, an intelligent coding assistant."}]

        # Add conversation history
        for msg in request.conversation_history:
            messages.append({
                "role": msg.role if msg.role in ["user", "assistant"] else "user",
                "content": msg.content
            })

        # Add current message
        messages.append({"role": "user", "content": request.message})

        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=request.temperature,
            max_tokens=8192,
        )

        response_text = completion.choices[0].message.content

        return GeminiChatResponse(
            response=response_text,
            model="groq-llama-3.3-70b (fallback)",
            usage={
                "prompt_tokens": completion.usage.prompt_tokens if hasattr(completion.usage, 'prompt_tokens') else 0,
                "completion_tokens": completion.usage.completion_tokens if hasattr(completion.usage, 'completion_tokens') else 0,
                "total_tokens": completion.usage.total_tokens if hasattr(completion.usage, 'total_tokens') else 0
            },
            timestamp=datetime.now().isoformat()
        )

    except Exception as groq_error:
        # If Groq also fails, raise the original Gemini error
        raise HTTPException(
            status_code=500,
            detail=f"All AI models failed. Gemini error: {str(last_error)}. Groq error: {str(groq_error)}"
        )


@router.post("/analyze-large-codebase")
async def analyze_large_codebase(
    files: Dict[str, str],  # filename: content
    question: str
):
    """
    Analyze entire codebase at once (up to 2M tokens!)

    Example:
    {
        "files": {
            "app.py": "...",
            "models.py": "...",
            "utils.py": "..."
        },
        "question": "How does the authentication system work?"
    }
    """
    try:
        configure_gemini()

        # Combine all files into one context
        codebase_context = "# Complete Codebase\n\n"
        for filename, content in files.items():
            codebase_context += f"## File: {filename}\n```\n{content}\n```\n\n"

        # Add question
        full_prompt = f"{codebase_context}\n\n# Question:\n{question}"

        # Use Gemini
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(full_prompt)

        return {
            "answer": response.text,
            "files_analyzed": len(files),
            "total_tokens": len(full_prompt.split()) * 1.3  # Rough estimate
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/analyze-long-document")
async def analyze_long_document(
    document: str,
    question: str
):
    """
    Analyze very long documents (up to 1500 pages!)

    Example:
    {
        "document": "...very long document...",
        "question": "Summarize the main points"
    }
    """
    try:
        configure_gemini()

        prompt = f"Document:\n\n{document}\n\nQuestion: {question}"

        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)

        return {
            "answer": response.text,
            "document_length": len(document),
            "estimated_tokens": len(document.split()) * 1.3
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/models")
async def list_gemini_models():
    """List available Gemini models"""
    return {
        "models": [
            {
                "id": "gemini-2.5-pro",
                "name": "Gemini 2.5 Pro",
                "context_window": 2000000,  # 2 MILLION!
                "description": "Latest Pro model with massive 2M token context",
                "cost": "FREE (15 req/min, 1500 req/day)",
                "strengths": ["long documents", "entire codebases", "complex analysis"]
            },
            {
                "id": "gemini-2.5-flash",
                "name": "Gemini 2.5 Flash",
                "context_window": 1000000,  # 1 MILLION
                "description": "Latest Flash model - ultra fast with 1M context",
                "cost": "FREE",
                "strengths": ["speed", "large documents", "real-time responses"]
            },
            {
                "id": "gemini-2.0-flash",
                "name": "Gemini 2.0 Flash",
                "context_window": 1000000,
                "description": "Fast and reliable - default model",
                "cost": "FREE",
                "strengths": ["speed", "balanced performance", "reliability"]
            }
        ]
    }


@router.post("/code-review-full-project")
async def code_review_full_project(
    project_files: Dict[str, str]
):
    """
    Review an entire project at once!
    No need to split into chunks - Gemini handles it all!
    """
    try:
        configure_gemini()

        # Build complete project view
        project_context = "# Complete Project for Review\n\n"
        for filename, content in project_files.items():
            project_context += f"## {filename}\n```\n{content}\n```\n\n"

        prompt = f"""{project_context}

Please review this entire codebase and provide:
1. Overall architecture assessment
2. Code quality issues
3. Security concerns
4. Performance optimization opportunities
5. Best practice violations
6. Suggestions for improvement

Be thorough and specific."""

        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)

        return {
            "review": response.text,
            "files_reviewed": len(project_files),
            "lines_of_code": sum(len(content.split('\n')) for content in project_files.values())
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.get("/health")
async def gemini_health_check():
    """Check if Gemini API is configured and working"""
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return {
                "status": "not_configured",
                "message": "GOOGLE_API_KEY not set. Get free key from https://aistudio.google.com/"
            }

        # Test with minimal request
        configure_gemini()
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content("Hi")

        return {
            "status": "healthy",
            "message": "Gemini API is working! 2M token context available!",
            "test_response": response.text[:50]
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@router.get("/usage-info")
async def gemini_usage_info():
    """Get information about Gemini free tier limits"""
    return {
        "free_tier": {
            "rate_limit": "15 requests per minute",
            "daily_limit": "1500 requests per day",
            "context_window": "2 million tokens",
            "models": ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.0-pro"],
            "cost": "100% FREE",
            "credit_card_required": False
        },
        "paid_tier": {
            "cost": "$7 per million tokens (cheaper than Claude!)",
            "rate_limit": "Much higher",
            "context_window": "Same (2M tokens)",
            "when_to_upgrade": "Only if you need more than 1500 requests/day"
        },
        "comparison": {
            "vs_claude": {
                "context": "Gemini: 2M tokens vs Claude: 200K tokens (10x more!)",
                "cost": "Gemini: FREE vs Claude: $3-15 per million",
                "quality": "Gemini: Excellent vs Claude: Excellent (similar)"
            }
        }
    }
