"""Enhanced Groq API server with model selection, rate limiting, and advanced features"""

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

app = FastAPI(title="Genius AI API", version="2.0")

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

# Rate limiting storage (IP -> list of request timestamps)
rate_limit_store = defaultdict(list)
RATE_LIMIT_REQUESTS = 60  # Max requests per minute
RATE_LIMIT_WINDOW = 60  # Seconds

# Available models
AVAILABLE_MODELS = {
    "llama-3.3-70b-versatile": {
        "name": "Llama 3.3 70B",
        "description": "Most intelligent, best for complex tasks",
        "context": 8192,
        "type": "text"
    },
    "llama-3.1-8b-instant": {
        "name": "Llama 3.1 8B Instant",
        "description": "Super fast responses",
        "context": 8192,
        "type": "text"
    },
    "mixtral-8x7b-32768": {
        "name": "Mixtral 8x7B",
        "description": "Long context window (32k tokens)",
        "context": 32768,
        "type": "text"
    },
    "gemma2-9b-it": {
        "name": "Gemma 2 9B",
        "description": "Balanced speed and quality",
        "context": 8192,
        "type": "text"
    },
    "llama-3.2-90b-vision-preview": {
        "name": "Llama 3.2 90B Vision",
        "description": "Image analysis and understanding",
        "context": 8192,
        "type": "vision"
    }
}

class ChatRequest(BaseModel):
    message: str
    model: Optional[str] = "llama-3.3-70b-versatile"
    temperature: Optional[float] = 0.8  # Slightly higher for more creative responses
    max_tokens: Optional[int] = 8192  # Increased for longer, more detailed responses
    system_prompt: Optional[str] = None
    image_data: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    model: str
    tokens_used: Optional[int] = None
    analyzed_file: Optional[str] = None
    processing_time: Optional[float] = None

class ModelInfo(BaseModel):
    id: str
    name: str
    description: str
    context: int
    type: str

def check_rate_limit(client_ip: str) -> bool:
    """Check if client has exceeded rate limit"""
    now = datetime.now()
    cutoff = now - timedelta(seconds=RATE_LIMIT_WINDOW)

    # Clean old requests
    rate_limit_store[client_ip] = [
        timestamp for timestamp in rate_limit_store[client_ip]
        if timestamp > cutoff
    ]

    # Check limit
    if len(rate_limit_store[client_ip]) >= RATE_LIMIT_REQUESTS:
        return False

    # Add current request
    rate_limit_store[client_ip].append(now)
    return True

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Apply rate limiting to all requests"""
    client_ip = request.client.host

    # Skip rate limiting for health check
    if request.url.path in ["/", "/health", "/models"]:
        return await call_next(request)

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
        "version": "2.0",
        "features": [
            "Multiple AI models",
            "Image analysis",
            "Document processing",
            "Rate limiting",
            "Code syntax highlighting support",
            "Voice input ready"
        ]
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "models_available": len(AVAILABLE_MODELS),
        "rate_limit": f"{RATE_LIMIT_REQUESTS}/min"
    }

@app.get("/models", response_model=List[ModelInfo])
def get_models():
    """Get list of available models"""
    return [
        ModelInfo(id=model_id, **model_data)
        for model_id, model_data in AVAILABLE_MODELS.items()
    ]

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Enhanced chat endpoint with model selection"""
    start_time = datetime.now()

    try:
        # Validate model
        if request.model not in AVAILABLE_MODELS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid model. Available models: {list(AVAILABLE_MODELS.keys())}"
            )

        model_info = AVAILABLE_MODELS[request.model]

        # Check if image data provided but using text model
        if request.image_data and model_info["type"] != "vision":
            # Switch to vision model automatically
            request.model = "llama-3.2-90b-vision-preview"
            model_info = AVAILABLE_MODELS[request.model]

        # Handle vision model with image
        if request.image_data:
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": request.message
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": request.image_data
                            }
                        }
                    ]
                }
            ]

            completion = groq_client.chat.completions.create(
                model=request.model,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )
        else:
            # Regular text chat
            messages = []

            # Add enhanced system prompt for maximum intelligence
            if request.system_prompt:
                messages.append({
                    "role": "system",
                    "content": request.system_prompt
                })
            else:
                messages.append({
                    "role": "system",
                    "content": """You are Genius AI, an exceptionally intelligent and knowledgeable assistant with expertise across all domains.

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
                })

            messages.append({
                "role": "user",
                "content": request.message
            })

            completion = groq_client.chat.completions.create(
                model=request.model,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens if request.max_tokens else 8192,  # Increased default
            )

        processing_time = (datetime.now() - start_time).total_seconds()

        return ChatResponse(
            response=completion.choices[0].message.content,
            model=model_info["name"],
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
    """Upload and analyze files (images, documents, etc.)"""
    start_time = datetime.now()

    try:
        # Read file
        contents = await file.read()

        # Check file size (20MB limit)
        max_size = 20 * 1024 * 1024  # 20MB
        if len(contents) > max_size:
            raise HTTPException(
                status_code=413,
                detail="File too large. Maximum size is 20MB."
            )

        # Handle images
        if file.content_type and file.content_type.startswith('image/'):
            # Convert to base64
            base64_image = base64.b64encode(contents).decode('utf-8')
            data_url = f"data:{file.content_type};base64,{base64_image}"

            # Analyze with vision model
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{message}\n\nFilename: {file.filename}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": data_url
                            }
                        }
                    ]
                }
            ]

            completion = groq_client.chat.completions.create(
                model="llama-3.2-11b-vision-preview",  # Updated to current vision model
                messages=messages,
                temperature=0.7,
                max_tokens=4096,  # Increased for more detailed responses
            )

            processing_time = (datetime.now() - start_time).total_seconds()

            return ChatResponse(
                response=completion.choices[0].message.content,
                model="Llama 3.2 11B Vision",
                analyzed_file=file.filename,
                processing_time=processing_time
            )

        # Handle text files
        elif file.content_type in ['text/plain', 'application/pdf', 'text/markdown']:
            text_content = contents.decode('utf-8', errors='ignore')[:50000]  # First 50k chars

            full_message = f"{message}\n\nFilename: {file.filename}\n\nFile content:\n{text_content}"

            completion = groq_client.chat.completions.create(
                model=model if model in AVAILABLE_MODELS else "llama-3.3-70b-versatile",
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
                max_tokens=2048,
            )

            processing_time = (datetime.now() - start_time).total_seconds()

            return ChatResponse(
                response=completion.choices[0].message.content,
                model=AVAILABLE_MODELS.get(model, AVAILABLE_MODELS["llama-3.3-70b-versatile"])["name"],
                analyzed_file=file.filename,
                processing_time=processing_time
            )

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file.content_type}. Supported: images (PNG, JPG), text files, PDFs, markdown."
            )

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = f"Error processing file: {str(e)}\n{traceback.format_exc()}"
        print(error_detail)  # Log to console
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
def get_stats():
    """Get API usage statistics"""
    total_requests = sum(len(requests) for requests in rate_limit_store.values())
    active_ips = len(rate_limit_store)

    return {
        "total_requests_last_minute": total_requests,
        "active_clients": active_ips,
        "rate_limit": f"{RATE_LIMIT_REQUESTS}/min",
        "models_available": len(AVAILABLE_MODELS)
    }

if __name__ == "__main__":
    print("=" * 60)
    print("GENIUS AI - ENHANCED API SERVER")
    print("=" * 60)
    print(f"{len(AVAILABLE_MODELS)} AI models loaded")
    print(f"Rate limiting: {RATE_LIMIT_REQUESTS} requests/minute")
    print(f"Max file size: 20MB")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000)
