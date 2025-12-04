"""FastAPI server with chat endpoints."""

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uvicorn

from genius_ai import __version__
from genius_ai.agents.orchestrator import OrchestratorAgent
from genius_ai.api.schemas import (
    ChatRequest,
    ChatResponse,
    DocumentUpload,
    DocumentResponse,
    HealthResponse,
    ErrorResponse,
    FeedbackRequest,
    FeedbackResponse,
    LearningInsightsResponse,
)
from genius_ai.core.config import settings
from genius_ai.core.logger import logger
from genius_ai.memory.conversation import ConversationMemory, MessageRole
from genius_ai.memory.learning import learning_system
from genius_ai.models.base import ModelFactory, ModelType, GenerationConfig
from genius_ai.rag.retriever import RAGRetriever


# Global state
app_state = {
    "model": None,
    "orchestrator": None,
    "rag_retriever": None,
    "conversations": {},  # conversation_id -> ConversationMemory
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup
    logger.info("Starting Genius AI server...")

    try:
        # Initialize model - Use our custom trained model!
        logger.info("Loading custom trained model...")
        from genius_ai.models.custom_trained import CustomTrainedModel

        model = CustomTrainedModel(
            model_path="../genius_model_enhanced",
            device=settings.device,
        )
        await model.initialize()
        app_state["model"] = model
        logger.info("Custom trained model loaded successfully")
        logger.info(f"Model info: {model.get_model_info()}")

        # Initialize RAG retriever first
        rag_retriever = RAGRetriever()
        await rag_retriever.initialize()
        app_state["rag_retriever"] = rag_retriever
        logger.info("RAG retriever initialized")

        # Initialize orchestrator with RAG and tools enabled
        orchestrator = OrchestratorAgent(
            model=model,
            enable_reflection=True,
            enable_tools=True,
            rag_retriever=rag_retriever,
        )
        app_state["orchestrator"] = orchestrator
        logger.info("Orchestrator initialized with RAG and tools")

        logger.info("Genius AI server started successfully")

    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down Genius AI server...")
    if app_state["model"]:
        await app_state["model"].cleanup()
    logger.info("Server shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="Genius AI API",
    description="Advanced conversational AI with multi-agent reasoning",
    version=__version__,
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=dict)
async def root():
    """Root endpoint."""
    return {
        "name": "Genius AI API",
        "version": __version__,
        "status": "running",
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=__version__,
        model_loaded=app_state["model"] is not None,
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Chat endpoint - Uses Groq FREE 70B AI first, then fallback to local model."""
    try:
        # Get or create conversation
        conversation_id = request.conversation_id or str(uuid4())
        if conversation_id not in app_state["conversations"]:
            app_state["conversations"][conversation_id] = ConversationMemory()

        conversation = app_state["conversations"][conversation_id]

        # Add user message
        conversation.add_user_message(request.message)

        # TRY GROQ FIRST (FREE 70B AI!)
        try:
            from genius_ai.api.groq_chat import chat_with_groq

            logger.info("Using Groq Llama 3.1 70B (FREE!)")

            # Get conversation history for context
            history = conversation.get_formatted_history(limit=10)
            system_prompt = (
                "You are Genius AI, an intelligent and helpful assistant. "
                "Provide clear, accurate, and comprehensive responses. "
                f"\n\nConversation history:\n{history}"
            )

            # Use Groq's FREE 70B AI!
            response_text = await chat_with_groq(
                message=request.message,
                system_prompt=system_prompt,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            )

            # Add response to conversation
            conversation.add_assistant_message(response_text)

            # Rough token count
            tokens_used = len(request.message.split()) + len(response_text.split())

            return ChatResponse(
                response=response_text,
                conversation_id=conversation_id,
                model="Llama 3.1 70B (FREE via Groq!)",
                tokens_used=tokens_used,
                metadata={
                    "source": "groq",
                    "intelligence": "8.5/10",
                    "cost": "$0 (FREE!)",
                },
            )

        except Exception as groq_error:
            # Groq failed, fallback to local model
            logger.warning(f"Groq failed, using local model: {groq_error}")

            # Prepare context
            context = {}

            # Use RAG if enabled
            if request.use_rag and app_state["rag_retriever"]:
                retrieved_context = await app_state["rag_retriever"].retrieve_context(
                    request.message
                )
                if retrieved_context:
                    context["knowledge"] = retrieved_context

            # Add conversation history
            context["history"] = conversation.get_formatted_history(limit=10)

            # Process with orchestrator (local model)
            orchestrator = app_state["orchestrator"]
            agent_response = await orchestrator.process(
                request.message,
                context=context,
            )

            # Add assistant response to conversation
            conversation.add_assistant_message(agent_response.content)

            # Count tokens (rough estimate)
            model = app_state["model"]
            tokens_used = model.count_tokens(request.message) + model.count_tokens(
                agent_response.content
            )

            return ChatResponse(
                response=agent_response.content,
                conversation_id=conversation_id,
                model=f"{settings.base_model_name} (local fallback)",
                tokens_used=tokens_used,
                metadata={
                    "source": "local",
                    "confidence": agent_response.confidence,
                    "thoughts_count": len(agent_response.thoughts),
                    **agent_response.metadata,
                },
            )

    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest) -> StreamingResponse:
    """Streaming chat endpoint."""

    async def generate_stream() -> AsyncIterator[str]:
        try:
            # Get or create conversation
            conversation_id = request.conversation_id or str(uuid4())
            if conversation_id not in app_state["conversations"]:
                app_state["conversations"][conversation_id] = ConversationMemory()

            conversation = app_state["conversations"][conversation_id]
            conversation.add_user_message(request.message)

            # Build prompt with context
            history = conversation.get_formatted_history(limit=10)
            prompt = f"{history}\n\nUser: {request.message}\nAssistant:"

            # Stream response
            model = app_state["model"]
            config = GenerationConfig(
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                stream=True,
            )

            full_response = ""
            async for chunk in model.generate_stream(prompt, config):
                full_response += chunk
                yield f"data: {chunk}\n\n"

            # Add response to conversation
            conversation.add_assistant_message(full_response)

            yield "data: [DONE]\n\n"

        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield f"data: [ERROR] {str(e)}\n\n"

    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream",
    )


@app.post("/documents", response_model=DocumentResponse)
async def add_document(document: DocumentUpload) -> DocumentResponse:
    """Add document to knowledge base."""
    try:
        rag_retriever = app_state["rag_retriever"]
        if not rag_retriever:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="RAG retriever not available",
            )

        from genius_ai.rag.retriever import Document

        doc = Document(
            content=document.content,
            metadata=document.metadata,
        )

        chunks_added = await rag_retriever.add_documents([doc])

        return DocumentResponse(
            success=True,
            chunks_added=chunks_added,
            message=f"Successfully added {chunks_added} chunks to knowledge base",
        )

    except Exception as e:
        logger.error(f"Document upload error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@app.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation."""
    if conversation_id in app_state["conversations"]:
        del app_state["conversations"][conversation_id]
        return {"message": "Conversation deleted"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Conversation not found",
    )


@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history."""
    if conversation_id not in app_state["conversations"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    conversation = app_state["conversations"][conversation_id]
    return conversation.to_dict()


@app.post("/chat/thoughts")
async def chat_with_thoughts(request: ChatRequest) -> StreamingResponse:
    """Chat endpoint with streaming agent thoughts."""

    async def generate_thought_stream() -> AsyncIterator[str]:
        import json

        try:
            # Get or create conversation
            conversation_id = request.conversation_id or str(uuid4())
            if conversation_id not in app_state["conversations"]:
                app_state["conversations"][conversation_id] = ConversationMemory()

            conversation = app_state["conversations"][conversation_id]
            conversation.add_user_message(request.message)

            # Prepare context
            context = {}
            context["history"] = conversation.get_formatted_history(limit=10)

            # Create callback for streaming thoughts
            async def thought_callback(thought):
                thought_data = {
                    "type": "thought",
                    "agent": thought.agent_role.value,
                    "content": thought.content,
                    "timestamp": thought.timestamp.isoformat(),
                }
                yield f"data: {json.dumps(thought_data)}\n\n"

            # Set callback on orchestrator
            orchestrator = app_state["orchestrator"]
            orchestrator.set_thought_stream_callback(thought_callback)

            # Process with orchestrator
            agent_response = await orchestrator.process(
                request.message,
                context=context,
            )

            # Send final response
            final_data = {
                "type": "response",
                "content": agent_response.content,
                "metadata": agent_response.metadata,
                "conversation_id": conversation_id,
            }
            yield f"data: {json.dumps(final_data)}\n\n"

            # Add to conversation
            conversation.add_assistant_message(agent_response.content)

            yield "data: [DONE]\n\n"

        except Exception as e:
            logger.error(f"Thought streaming error: {e}")
            error_data = {"type": "error", "message": str(e)}
            yield f"data: {json.dumps(error_data)}\n\n"

    return StreamingResponse(
        generate_thought_stream(),
        media_type="text/event-stream",
    )


@app.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(feedback: FeedbackRequest) -> FeedbackResponse:
    """Submit feedback on a response."""
    try:
        learning_system.record_feedback(
            conversation_id=feedback.conversation_id,
            message_id=feedback.message_id,
            rating=feedback.rating,
            comment=feedback.comment,
        )

        return FeedbackResponse(
            success=True,
            message="Feedback recorded successfully. Thank you for helping us improve!",
        )

    except Exception as e:
        logger.error(f"Feedback error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@app.get("/learning/insights", response_model=LearningInsightsResponse)
async def get_learning_insights() -> LearningInsightsResponse:
    """Get learning system insights."""
    try:
        insights = learning_system.get_insights()

        # Get suggestions for each problem type
        problem_types = ["question", "problem", "task", "analysis"]
        suggestions = {}
        for pt in problem_types:
            suggestions[pt] = learning_system.suggest_improvements(pt)

        return LearningInsightsResponse(
            total_strategies=insights["total_strategies"],
            total_feedback=insights["total_feedback"],
            positive_feedback_rate=insights["positive_feedback_rate"],
            problem_type_success_rates=insights["problem_type_success_rates"],
            best_performing_type=insights["best_performing_type"],
            suggestions=suggestions,
        )

    except Exception as e:
        logger.error(f"Learning insights error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@app.get("/learning/stats/{problem_type}")
async def get_problem_type_stats(problem_type: str):
    """Get statistics for a specific problem type."""
    try:
        stats = learning_system.get_problem_type_stats(problem_type)
        return stats

    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


def main():
    """Run the server."""
    uvicorn.run(
        "genius_ai.api.server:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
