"""Enhanced Vision API with multiple vision model providers and fallbacks"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from typing import Optional, List
import base64
import uvicorn
import os
from datetime import datetime, timedelta
from collections import defaultdict
import asyncio

app = FastAPI(title="Genius AI Vision API", version="3.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Groq client
groq_client = Groq(api_key="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")

# Rate limiting
rate_limit_store = defaultdict(list)
RATE_LIMIT_REQUESTS = 60
RATE_LIMIT_WINDOW = 60

# Available vision models - UPDATED with working models
VISION_MODELS = {
    "llava-v1.5-7b-4096-preview": {
        "name": "LLaVA 1.5 7B",
        "provider": "groq",
        "description": "Fast vision model for image understanding",
        "max_tokens": 4096
    },
    "llama-3.2-11b-vision-preview": {
        "name": "Llama 3.2 11B Vision",
        "provider": "groq",
        "description": "Advanced vision capabilities",
        "max_tokens": 8192,
        "status": "deprecated"  # Mark as deprecated
    }
}

# Text models for fallback
TEXT_MODELS = {
    "llama-3.3-70b-versatile": {
        "name": "Llama 3.3 70B",
        "description": "Most intelligent text model",
        "context": 8192
    },
    "mixtral-8x7b-32768": {
        "name": "Mixtral 8x7B",
        "description": "Long context text model",
        "context": 32768
    }
}

class ChatRequest(BaseModel):
    message: str
    model: Optional[str] = "llama-3.3-70b-versatile"
    temperature: Optional[float] = 0.8
    max_tokens: Optional[int] = 8192
    system_prompt: Optional[str] = None
    image_data: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    model: str
    tokens_used: Optional[int] = None
    analyzed_file: Optional[str] = None
    processing_time: Optional[float] = None
    vision_method: Optional[str] = None  # New field to show which method was used

class ModelInfo(BaseModel):
    id: str
    name: str
    description: str
    provider: str

def check_rate_limit(client_ip: str) -> bool:
    """Check if client has exceeded rate limit"""
    now = datetime.now()
    cutoff = now - timedelta(seconds=RATE_LIMIT_WINDOW)
    rate_limit_store[client_ip] = [
        timestamp for timestamp in rate_limit_store[client_ip]
        if timestamp > cutoff
    ]
    if len(rate_limit_store[client_ip]) >= RATE_LIMIT_REQUESTS:
        return False
    rate_limit_store[client_ip].append(now)
    return True

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Apply rate limiting"""
    client_ip = request.client.host
    if request.url.path not in ["/", "/health", "/models", "/vision-models"]:
        if not check_rate_limit(client_ip):
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Maximum {RATE_LIMIT_REQUESTS} requests per minute."
            )
    response = await call_next(request)
    return response

@app.get("/")
def root():
    return {
        "status": "running",
        "version": "3.0",
        "features": [
            "Advanced vision modeling",
            "Multiple vision providers",
            "Intelligent fallbacks",
            "Image-to-text description",
            "Text model integration",
            "Rate limiting"
        ]
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "vision_models": len(VISION_MODELS),
        "text_models": len(TEXT_MODELS)
    }

@app.get("/vision-models", response_model=List[ModelInfo])
def get_vision_models():
    """Get available vision models"""
    return [
        ModelInfo(
            id=model_id,
            name=model_data["name"],
            description=model_data["description"],
            provider=model_data["provider"]
        )
        for model_id, model_data in VISION_MODELS.items()
        if model_data.get("status") != "deprecated"
    ]

async def try_vision_model(image_data: str, message: str, model_id: str) -> Optional[str]:
    """Try to analyze image with a specific vision model"""
    try:
        print(f"Trying vision model: {model_id}")

        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": message
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_data
                        }
                    }
                ]
            }
        ]

        completion = groq_client.chat.completions.create(
            model=model_id,
            messages=messages,
            temperature=0.7,
            max_tokens=VISION_MODELS[model_id]["max_tokens"],
        )

        return completion.choices[0].message.content
    except Exception as e:
        print(f"Vision model {model_id} failed: {str(e)}")
        return None

async def fallback_image_description(image_data: str, message: str) -> str:
    """Fallback: Use text model with image metadata"""
    try:
        # Extract image metadata
        image_base64 = image_data.split(',')[1] if ',' in image_data else image_data
        image_bytes = base64.b64decode(image_base64)
        image_size = len(image_bytes)

        # Create descriptive prompt for text model
        fallback_message = f"""I've received an image upload with the following characteristics:
- File size: {image_size / 1024:.1f} KB
- Format: Base64 encoded image
- User request: {message}

Since vision models are temporarily unavailable, I'll provide guidance based on the request.

For image analysis tasks, I can:
1. Guide you on what to look for
2. Explain how to analyze similar images
3. Provide relevant information about the topic
4. Suggest tools and techniques

How can I best assist you with: "{message}"?"""

        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are Genius AI. A vision model is temporarily unavailable, but you can still help users by providing relevant information and guidance about their image-related queries."
                },
                {
                    "role": "user",
                    "content": fallback_message
                }
            ],
            temperature=0.8,
            max_tokens=8192,
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"I apologize, but I'm currently unable to analyze images. Error: {str(e)}\n\nPlease try again in a moment, or describe the image to me and I'll do my best to help!"

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Enhanced chat with vision support"""
    start_time = datetime.now()

    try:
        # Check if image included
        if request.image_data:
            # Try vision models in order of preference
            for model_id in ["llava-v1.5-7b-4096-preview", "llama-3.2-11b-vision-preview"]:
                if VISION_MODELS.get(model_id, {}).get("status") != "deprecated":
                    result = await try_vision_model(request.image_data, request.message, model_id)
                    if result:
                        processing_time = (datetime.now() - start_time).total_seconds()
                        return ChatResponse(
                            response=result,
                            model=VISION_MODELS[model_id]["name"],
                            processing_time=processing_time,
                            vision_method="direct"
                        )

            # If all vision models failed, use fallback
            print("All vision models failed, using intelligent fallback")
            fallback_response = await fallback_image_description(request.image_data, request.message)
            processing_time = (datetime.now() - start_time).total_seconds()

            return ChatResponse(
                response=f"⚠️ **Note:** Vision models are temporarily unavailable. Providing alternative assistance:\n\n{fallback_response}",
                model="Llama 3.3 70B (Text Fallback)",
                processing_time=processing_time,
                vision_method="fallback"
            )

        # Regular text chat
        else:
            system_prompt = request.system_prompt or """You are Genius AI, an exceptionally intelligent and knowledgeable assistant with expertise across all domains.

Your capabilities:
- Expert-level knowledge in science, technology, mathematics, programming, arts, and humanities
- Deep reasoning and analytical thinking
- Creative problem-solving and lateral thinking
- Ability to explain complex concepts simply
- Code generation and debugging expertise in 100+ languages
- Mathematical and logical reasoning
- Critical thinking and nuanced understanding

Your approach:
- Provide comprehensive, accurate, and well-structured responses
- Use examples, analogies, and step-by-step explanations when helpful
- Format code with proper markdown syntax highlighting
- Cite reasoning and show your thought process
- Ask clarifying questions when needed
- Be precise, detailed, and thorough

Respond as a world-class expert would."""

            completion = groq_client.chat.completions.create(
                model=request.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": request.message}
                ],
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )

            processing_time = (datetime.now() - start_time).total_seconds()

            return ChatResponse(
                response=completion.choices[0].message.content,
                model=TEXT_MODELS.get(request.model, {}).get("name", request.model),
                tokens_used=completion.usage.total_tokens if hasattr(completion, 'usage') else None,
                processing_time=processing_time
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload", response_model=ChatResponse)
async def upload_file(
    file: UploadFile = File(...),
    message: str = Form("Analyze this file"),
    model: str = Form("llama-3.3-70b-versatile")
):
    """Upload and analyze files with advanced vision support"""
    start_time = datetime.now()

    try:
        contents = await file.read()

        # Check file size
        max_size = 20 * 1024 * 1024
        if len(contents) > max_size:
            raise HTTPException(status_code=413, detail="File too large. Maximum size is 20MB.")

        # Handle images
        if file.content_type and file.content_type.startswith('image/'):
            base64_image = base64.b64encode(contents).decode('utf-8')
            data_url = f"data:{file.content_type};base64,{base64_image}"

            # Try vision models
            for model_id in ["llava-v1.5-7b-4096-preview", "llama-3.2-11b-vision-preview"]:
                if VISION_MODELS.get(model_id, {}).get("status") != "deprecated":
                    result = await try_vision_model(data_url, f"{message}\n\nFilename: {file.filename}", model_id)
                    if result:
                        processing_time = (datetime.now() - start_time).total_seconds()
                        return ChatResponse(
                            response=result,
                            model=VISION_MODELS[model_id]["name"],
                            analyzed_file=file.filename,
                            processing_time=processing_time,
                            vision_method="direct"
                        )

            # Fallback for images
            fallback_response = await fallback_image_description(data_url, f"{message}\n\nFilename: {file.filename}")
            processing_time = (datetime.now() - start_time).total_seconds()

            return ChatResponse(
                response=f"⚠️ **Note:** Vision models are temporarily unavailable.\n\n**File:** {file.filename}\n**Size:** {len(contents) / 1024:.1f} KB\n\n{fallback_response}",
                model="Llama 3.3 70B (Text Fallback)",
                analyzed_file=file.filename,
                processing_time=processing_time,
                vision_method="fallback"
            )

        # Handle text files
        elif file.content_type in ['text/plain', 'application/pdf', 'text/markdown']:
            text_content = contents.decode('utf-8', errors='ignore')[:50000]
            full_message = f"{message}\n\nFilename: {file.filename}\n\nFile content:\n{text_content}"

            completion = groq_client.chat.completions.create(
                model=model if model in TEXT_MODELS else "llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are Genius AI analyzing a document. Provide detailed insights and answer the user's questions."
                    },
                    {
                        "role": "user",
                        "content": full_message
                    }
                ],
                temperature=0.7,
                max_tokens=8192,
            )

            processing_time = (datetime.now() - start_time).total_seconds()

            return ChatResponse(
                response=completion.choices[0].message.content,
                model=TEXT_MODELS.get(model, TEXT_MODELS["llama-3.3-70b-versatile"])["name"],
                analyzed_file=file.filename,
                processing_time=processing_time
            )

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file.content_type}"
            )

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"Error: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
def get_stats():
    """Get API usage statistics"""
    total_requests = sum(len(requests) for requests in rate_limit_store.values())
    return {
        "total_requests_last_minute": total_requests,
        "active_clients": len(rate_limit_store),
        "rate_limit": f"{RATE_LIMIT_REQUESTS}/min",
        "vision_models": len([m for m in VISION_MODELS.values() if m.get("status") != "deprecated"]),
        "text_models": len(TEXT_MODELS)
    }

if __name__ == "__main__":
    print("=" * 60)
    print("GENIUS AI - VISION ENHANCED API SERVER v3.0")
    print("=" * 60)
    print(f"Vision models: {len([m for m in VISION_MODELS.values() if m.get('status') != 'deprecated'])}")
    print(f"Text models: {len(TEXT_MODELS)}")
    print(f"Rate limiting: {RATE_LIMIT_REQUESTS} requests/minute")
    print(f"Intelligent fallbacks: ENABLED")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000)
