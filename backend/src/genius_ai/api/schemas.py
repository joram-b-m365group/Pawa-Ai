"""API request and response schemas."""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Chat message schema."""

    role: str = Field(..., description="Message role (user, assistant, system)")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Chat request schema."""

    message: str = Field(..., description="User message", min_length=1)
    conversation_id: str | None = Field(None, description="Conversation ID for continuity")
    stream: bool = Field(False, description="Enable streaming response")
    use_rag: bool = Field(True, description="Use RAG for knowledge retrieval")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="Generation temperature")
    max_tokens: int = Field(2048, ge=1, le=4096, description="Maximum tokens to generate")


class ChatResponse(BaseModel):
    """Chat response schema."""

    response: str = Field(..., description="Assistant response")
    conversation_id: str = Field(..., description="Conversation ID")
    model: str = Field(..., description="Model used")
    tokens_used: int = Field(..., description="Total tokens used")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    timestamp: datetime = Field(default_factory=datetime.now)


class DocumentUpload(BaseModel):
    """Document upload schema."""

    content: str = Field(..., description="Document content")
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Document metadata (source, author, etc.)",
    )


class DocumentResponse(BaseModel):
    """Document upload response."""

    success: bool = Field(..., description="Upload success")
    chunks_added: int = Field(..., description="Number of chunks added")
    message: str = Field(..., description="Status message")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    model_loaded: bool = Field(..., description="Whether model is loaded")
    timestamp: datetime = Field(default_factory=datetime.now)


class ErrorResponse(BaseModel):
    """Error response schema."""

    error: str = Field(..., description="Error message")
    detail: str | None = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.now)


class FeedbackRequest(BaseModel):
    """Feedback request schema."""

    conversation_id: str = Field(..., description="Conversation ID")
    message_id: str = Field(..., description="Message ID")
    rating: int = Field(..., ge=1, le=5, description="Rating (1-5)")
    comment: str | None = Field(None, description="Optional feedback comment")


class FeedbackResponse(BaseModel):
    """Feedback response schema."""

    success: bool = Field(..., description="Feedback recorded successfully")
    message: str = Field(..., description="Confirmation message")


class LearningInsightsResponse(BaseModel):
    """Learning insights response schema."""

    total_strategies: int = Field(..., description="Total strategies learned")
    total_feedback: int = Field(..., description="Total feedback received")
    positive_feedback_rate: float = Field(..., description="Positive feedback rate")
    problem_type_success_rates: dict[str, float] = Field(..., description="Success rates by problem type")
    best_performing_type: str | None = Field(None, description="Best performing problem type")
    suggestions: dict[str, list[str]] = Field(default_factory=dict, description="Improvement suggestions by type")
