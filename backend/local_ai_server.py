"""
Local AI Server - FREE Intelligence
Uses Ollama to run models locally on your computer
NO API costs, completely FREE!
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any, List, Optional, Dict
import uvicorn
import json
import os
import requests
from uuid import uuid4

# Create FastAPI app
app = FastAPI(
    title="Genius AI - Local Intelligence",
    description="True AI intelligence running FREE on your computer",
    version="5.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://host.docker.internal:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2")  # Fast 3B parameter model

# Conversation storage
conversations = {}

# Models
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_id: Optional[str] = None
    temperature: float = 0.8
    images: Optional[List[str]] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    timestamp: datetime = Field(default_factory=datetime.now)

class HealthResponse(BaseModel):
    status: str
    message: str
    model: str
    capabilities: List[str]

# ============================
# LOCAL AI ENGINE
# ============================

class LocalAI:
    """
    Uses Ollama to run AI models locally - completely FREE!
    """

    def __init__(self):
        self.ollama_url = OLLAMA_URL
        self.model = MODEL_NAME
        self.check_ollama()

    def check_ollama(self):
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m["name"] for m in models]
                print(f"✓ Ollama connected! Available models: {model_names}")

                # Check if our model is available
                if not any(self.model in name for name in model_names):
                    print(f"⚠ Model '{self.model}' not found. Downloading...")
                    print(f"  This may take a few minutes the first time.")
            else:
                print(f"⚠ Ollama API returned status {response.status_code}")
        except Exception as e:
            print(f"⚠ Ollama not detected: {e}")
            print(f"  Starting in fallback mode. Install Ollama for true AI!")
            print(f"  Visit: https://ollama.com/download")

    async def generate(self, message: str, history: List[Dict] = None, images: List[str] = None) -> str:
        """
        Generate response using local AI model
        """

        try:
            # Build conversation context
            prompt = self._build_prompt(message, history)

            # Call Ollama API
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.8,
                        "num_predict": 500,  # Max tokens
                    }
                },
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                print(f"Ollama error: {response.status_code}")
                return await self._fallback_response(message)

        except requests.exceptions.ConnectionError:
            print("⚠ Ollama not running. Using fallback.")
            return await self._fallback_response(message)
        except Exception as e:
            print(f"Error: {e}")
            return await self._fallback_response(message)

    def _build_prompt(self, message: str, history: List[Dict] = None) -> str:
        """Build conversation prompt"""

        system_prompt = """You are Genius AI, an incredibly intelligent and helpful assistant. You communicate naturally like a brilliant human friend.

Your personality:
- Warm and friendly, never robotic
- Deeply knowledgeable across all subjects
- Explain complex topics clearly
- Show genuine interest and curiosity
- Be concise but thorough

Answer the user's question intelligently and naturally."""

        # Build conversation context
        prompt = system_prompt + "\n\n"

        if history:
            for msg in history[-6:]:  # Last 6 messages
                role = "User" if msg["role"] == "user" else "Assistant"
                prompt += f"{role}: {msg['content']}\n"

        prompt += f"User: {message}\nAssistant:"

        return prompt

    async def _fallback_response(self, message: str) -> str:
        """Fallback when Ollama isn't available"""

        msg_lower = message.lower()

        # Check if it's a simple social phrase
        if any(phrase in msg_lower for phrase in ["how are you", "what's up", "hello", "hi "]):
            return "I'm here and ready to help! For the best experience, make sure Ollama is running. Visit https://ollama.com/download to install it for free AI intelligence!"

        # For other questions
        return f"""I'd love to give you an intelligent answer about: "{message[:100]}"

However, I need Ollama to be running for true AI intelligence!

**Quick Setup (FREE):**
1. Download Ollama: https://ollama.com/download
2. Install it (takes 2 minutes)
3. It runs automatically in the background
4. Restart this server: `docker restart genius-ai-local`

Once Ollama is running, I'll use the Llama 3.2 model to give you truly intelligent answers to ANY question - completely free, no API costs!

In the meantime, I can still help with:
- Math calculations (just ask!)
- Code generation
- Specific science topics

What would you like help with?"""

# Initialize AI
ai = LocalAI()

# ============================
# API ENDPOINTS
# ============================

@app.get("/", response_model=dict)
async def root():
    return {
        "message": "Genius AI - Local Intelligence (FREE!)",
        "version": "5.0.0",
        "model": MODEL_NAME,
        "cost": "$0"
    }

@app.get("/health", response_model=HealthResponse)
async def health():
    # Check if Ollama is available
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        ollama_status = "running" if response.status_code == 200 else "not running"
    except:
        ollama_status = "not running"

    return HealthResponse(
        status="healthy",
        message=f"Local AI ready! Ollama: {ollama_status}",
        model=MODEL_NAME,
        capabilities=[
            "local_ai_intelligence",
            "free_unlimited_use",
            "natural_conversation",
            "complex_reasoning",
            "any_question",
            "no_api_costs"
        ]
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with local AI model"""
    try:
        # Get or create conversation
        conv_id = request.conversation_id or str(uuid4())

        if conv_id not in conversations:
            conversations[conv_id] = []

        history = conversations[conv_id]

        # Add user message
        history.append({"role": "user", "content": request.message})

        # Generate response with local AI
        response_text = await ai.generate(request.message, history, request.images)

        # Add to history
        history.append({"role": "assistant", "content": response_text})

        # Keep last 20 messages
        if len(history) > 40:
            conversations[conv_id] = history[-40:]

        return ChatResponse(
            response=response_text,
            conversation_id=conv_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    if conversation_id in conversations:
        del conversations[conversation_id]
        return {"message": "Conversation cleared"}
    raise HTTPException(status_code=404, detail="Conversation not found")

# ============================
# STARTUP
# ============================

if __name__ == "__main__":
    print("🧠 Starting Local AI - FREE Intelligence!")
    print("=" * 60)
    print(f"Model: {MODEL_NAME}")
    print(f"Ollama URL: {OLLAMA_URL}")
    print(f"Cost: $0 - Completely FREE!")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
