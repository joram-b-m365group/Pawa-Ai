"""
Ultimate Genius AI Server
The most advanced AI system with multi-agent intelligence, memory, and learning
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
from datetime import datetime
import uuid

from ultimate_ai.orchestrator import AgentOrchestrator
from ultimate_ai.memory import LongTermMemory
from ultimate_ai.training import FineTuner

# Initialize FastAPI app
app = FastAPI(
    title="Ultimate Genius AI",
    description="Multi-agent AI system with memory, learning, and specialized expertise",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize systems
orchestrator = AgentOrchestrator(
    ollama_url="http://host.docker.internal:11434",
    model="llama3.2"
)
memory = LongTermMemory(db_path="data/memory.db")
fine_tuner = FineTuner()


# Request/Response Models
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User's message")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    images: Optional[List[str]] = Field(None, description="Base64 encoded images")
    temperature: float = Field(0.8, ge=0.0, le=2.0, description="Response creativity")


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    agent_used: str
    confidence: float
    reasoning: Optional[str] = None
    metadata: Dict[str, Any] = {}
    timestamp: str


class MemoryStats(BaseModel):
    total_messages: int
    unique_conversations: int
    learned_facts: int
    knowledge_entries: int
    user_preferences: int


class HealthStatus(BaseModel):
    status: str
    system: str
    agents: List[str]
    memory_stats: MemoryStats
    ollama_status: Dict[str, Any]


class FineTuneRequest(BaseModel):
    model_name: str
    expertise: str
    qualities: List[str]
    temperature: float = 0.8


# API Endpoints

@app.get("/")
async def root():
    """Root endpoint with system information"""
    return {
        "system": "Ultimate Genius AI",
        "version": "1.0.0",
        "description": "Multi-agent AI system with specialized expertise",
        "features": [
            "5 Specialized Agents (Reasoning, Math, Vision, Code, Creative)",
            "Long-term Memory System",
            "Continuous Learning",
            "Model Fine-Tuning",
            "Human-like Conversation",
            "Multimodal (Text + Images)"
        ],
        "endpoints": {
            "chat": "/api/chat",
            "health": "/api/health",
            "memory": "/api/memory/stats",
            "fine_tune": "/api/fine-tune/create"
        }
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - routes to best agent and maintains memory
    """
    try:
        # Generate conversation ID if not provided
        conversation_id = request.conversation_id or str(uuid.uuid4())

        # Process message through orchestrator
        result = await orchestrator.process_message(
            message=request.message,
            conversation_id=conversation_id,
            images=request.images,
            temperature=request.temperature
        )

        # Store in long-term memory
        memory.store_conversation(
            conversation_id=conversation_id,
            user_message=request.message,
            assistant_response=result["response"],
            metadata={
                "agent": result["agent"],
                "confidence": result["confidence"],
                "all_scores": result.get("all_agent_scores", {})
            }
        )

        # Return response
        return ChatResponse(
            response=result["response"],
            conversation_id=conversation_id,
            agent_used=result["agent"],
            confidence=result["confidence"],
            reasoning=result.get("reasoning"),
            metadata=result.get("metadata", {}),
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


@app.get("/api/health", response_model=HealthStatus)
async def health():
    """
    System health check
    """
    try:
        # Get orchestrator health
        system_health = orchestrator.get_health_status()

        # Get memory stats
        mem_stats = memory.get_statistics()

        return HealthStatus(
            status="healthy",
            system=system_health["system"],
            agents=system_health["agents"],
            memory_stats=MemoryStats(**mem_stats),
            ollama_status=system_health["core_intelligence"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@app.get("/api/memory/stats", response_model=MemoryStats)
async def memory_stats():
    """
    Get memory system statistics
    """
    try:
        stats = memory.get_statistics()
        return MemoryStats(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")


@app.get("/api/memory/conversation/{conversation_id}")
async def get_conversation(conversation_id: str, limit: int = 50):
    """
    Retrieve conversation history
    """
    try:
        history = memory.get_conversation_history(conversation_id, limit)
        return {
            "conversation_id": conversation_id,
            "history": history,
            "message_count": len(history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving conversation: {str(e)}")


@app.post("/api/memory/fact")
async def store_fact(
    fact: str,
    category: str = "general",
    confidence: float = 1.0
):
    """
    Store a learned fact
    """
    try:
        memory.store_fact(fact, category, confidence)
        return {"status": "success", "fact": fact, "category": category}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error storing fact: {str(e)}")


@app.get("/api/memory/facts")
async def get_facts(category: Optional[str] = None, limit: int = 10):
    """
    Retrieve learned facts
    """
    try:
        facts = memory.recall_facts(category=category, limit=limit)
        return {
            "facts": facts,
            "count": len(facts),
            "category": category or "all"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving facts: {str(e)}")


@app.post("/api/fine-tune/create")
async def create_fine_tuned_model(request: FineTuneRequest):
    """
    Create a fine-tuned expert model
    """
    try:
        result = fine_tuner.create_custom_expert(
            name=request.model_name,
            expertise=request.expertise,
            qualities=request.qualities,
            temperature=request.temperature
        )

        return {
            "status": "success",
            "model_info": result,
            "instructions": f"Run this command to create your model:\n{result['ollama_command']}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating model: {str(e)}")


@app.get("/api/fine-tune/examples")
async def get_fine_tune_examples():
    """
    Get pre-built expert model examples
    """
    try:
        medical = fine_tuner.create_medical_expert()
        coding = fine_tuner.create_coding_expert()
        writer = fine_tuner.create_creative_writer()

        return {
            "examples": [
                {
                    "name": "Medical Expert",
                    "description": "Expert in medical knowledge and healthcare",
                    "command": medical["ollama_command"]
                },
                {
                    "name": "Coding Expert",
                    "description": "Expert software engineer",
                    "command": coding["ollama_command"]
                },
                {
                    "name": "Creative Writer",
                    "description": "Master storyteller and writer",
                    "command": writer["ollama_command"]
                }
            ],
            "guide": fine_tuner.get_fine_tuning_guide()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting examples: {str(e)}")


@app.delete("/api/memory/conversation/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """
    Clear a conversation from memory
    """
    try:
        orchestrator.clear_conversation(conversation_id)
        return {"status": "success", "conversation_id": conversation_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing conversation: {str(e)}")


# Run server
if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║           🧠 ULTIMATE GENIUS AI SYSTEM 🧠                     ║
    ║                                                               ║
    ║  Multi-Agent Intelligence | Long-Term Memory | Learning       ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝

    Features:
    ✓ 5 Specialized Agents (Reasoning, Math, Vision, Code, Creative)
    ✓ Human-like conversation
    ✓ Long-term memory system
    ✓ Continuous learning
    ✓ Model fine-tuning
    ✓ Multimodal (text + images)

    Server running at: http://localhost:8000
    API Docs: http://localhost:8000/docs

    Agents:
    🧠 Reasoning Agent - Deep thinking & philosophy
    🔢 Math Agent - Calculations & problem-solving
    👁️ Vision Agent - Image understanding
    💻 Code Agent - Programming expert
    ✍️ Creative Agent - Writing & brainstorming
    """)

    uvicorn.run(app, host="0.0.0.0", port=8000)
