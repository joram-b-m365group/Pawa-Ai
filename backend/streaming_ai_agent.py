"""
Streaming AI Agent with Real-time Response
Provides token-by-token streaming for better UX and perceived intelligence
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, AsyncGenerator
import json
import os
from groq import Groq
import asyncio

router = APIRouter(prefix="/streaming", tags=["Streaming AI"])

# Initialize Groq
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class StreamingChatMessage(BaseModel):
    role: str
    content: str


class StreamingChatRequest(BaseModel):
    messages: List[StreamingChatMessage]
    model: str = "llama-3.3-70b-versatile"
    temperature: float = 0.7
    max_tokens: int = 8000
    project_path: Optional[str] = None
    session_id: Optional[str] = None
    enable_tools: bool = False


async def stream_groq_response(request: StreamingChatRequest) -> AsyncGenerator[str, None]:
    """
    Stream responses from Groq API token by token
    """
    try:
        # Convert messages to Groq format
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]

        # Create streaming completion
        stream = groq_client.chat.completions.create(
            model=request.model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=True
        )

        # Stream each chunk
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content

                # Send as SSE format
                yield f"data: {json.dumps({'type': 'content', 'content': content})}\n\n"

                # Small delay to prevent overwhelming the client
                await asyncio.sleep(0.001)

        # Send completion signal
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    except Exception as e:
        error_data = json.dumps({'type': 'error', 'error': str(e)})
        yield f"data: {error_data}\n\n"


async def stream_with_thinking(request: StreamingChatRequest) -> AsyncGenerator[str, None]:
    """
    Stream responses with visible chain-of-thought reasoning
    """
    try:
        # Add system prompt for chain-of-thought
        enhanced_messages = [
            {
                "role": "system",
                "content": """You are an expert AI coding assistant. Before providing your answer, think through the problem step by step.

Format your response like this:
<thinking>
1. [First, analyze what the user is asking]
2. [Consider the approach and potential solutions]
3. [Think about edge cases and best practices]
</thinking>

<answer>
[Your detailed answer here]
</answer>

Always show your reasoning process in the <thinking> section."""
            }
        ]

        enhanced_messages.extend([{"role": msg.role, "content": msg.content} for msg in request.messages])

        # Create streaming completion
        stream = groq_client.chat.completions.create(
            model=request.model,
            messages=enhanced_messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=True
        )

        in_thinking = False
        in_answer = False
        buffer = ""

        # Stream each chunk with section detection
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                buffer += content

                # Detect section changes
                if "<thinking>" in buffer:
                    in_thinking = True
                    yield f"data: {json.dumps({'type': 'thinking_start'})}\n\n"
                    buffer = buffer.split("<thinking>", 1)[1] if "<thinking>" in buffer else buffer

                if "</thinking>" in buffer:
                    in_thinking = False
                    yield f"data: {json.dumps({'type': 'thinking_end'})}\n\n"
                    buffer = buffer.split("</thinking>", 1)[1] if "</thinking>" in buffer else ""

                if "<answer>" in buffer:
                    in_answer = True
                    yield f"data: {json.dumps({'type': 'answer_start'})}\n\n"
                    buffer = buffer.split("<answer>", 1)[1] if "<answer>" in buffer else buffer

                if "</answer>" in buffer:
                    in_answer = False
                    buffer = buffer.split("</answer>", 1)[0] if "</answer>" in buffer else buffer

                # Send content with appropriate type
                if buffer:
                    if in_thinking:
                        yield f"data: {json.dumps({'type': 'thinking', 'content': buffer})}\n\n"
                    elif in_answer:
                        yield f"data: {json.dumps({'type': 'content', 'content': buffer})}\n\n"
                    else:
                        yield f"data: {json.dumps({'type': 'content', 'content': buffer})}\n\n"

                    buffer = ""

                await asyncio.sleep(0.001)

        # Send any remaining content
        if buffer:
            yield f"data: {json.dumps({'type': 'content', 'content': buffer})}\n\n"

        # Send completion signal
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    except Exception as e:
        error_data = json.dumps({'type': 'error', 'error': str(e)})
        yield f"data: {error_data}\n\n"


@router.post("/chat")
async def stream_chat(request: StreamingChatRequest):
    """
    Stream chat responses in real-time using Server-Sent Events (SSE)
    """
    return StreamingResponse(
        stream_groq_response(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )


@router.post("/chat-with-thinking")
async def stream_chat_with_thinking(request: StreamingChatRequest):
    """
    Stream chat responses with visible chain-of-thought reasoning
    Shows the AI's thinking process before the final answer
    """
    return StreamingResponse(
        stream_with_thinking(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@router.post("/code-agent-stream")
async def stream_code_agent(request: StreamingChatRequest):
    """
    Stream code agent responses with tool calling
    This combines streaming with the AI agent's tool execution
    """
    async def generate():
        try:
            # Import here to avoid circular dependency
            from ai_agent_tools import AIAgentTools

            # Initialize agent tools
            agent = AIAgentTools(project_root=request.project_path)
            tools = agent.get_available_tools() if request.enable_tools else None

            # Add system prompt for coding
            messages = [
                {
                    "role": "system",
                    "content": """You are an expert AI coding assistant with access to tools for reading, writing, and analyzing code.

When you need to perform actions:
1. First, explain what you're going to do
2. Then use the appropriate tools
3. Finally, explain what you did and the results

Be thorough but concise. Always show your reasoning."""
                }
            ]

            messages.extend([{"role": msg.role, "content": msg.content} for msg in request.messages])

            # Send initial status
            yield f"data: {json.dumps({'type': 'status', 'status': 'thinking'})}\n\n"

            # Create streaming completion
            stream = groq_client.chat.completions.create(
                model=request.model,
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                tools=tools,
                tool_choice="auto" if tools else None,
                stream=True
            )

            current_content = ""
            tool_calls = []

            # Stream response
            for chunk in stream:
                delta = chunk.choices[0].delta

                # Handle content
                if delta.content:
                    current_content += delta.content
                    yield f"data: {json.dumps({'type': 'content', 'content': delta.content})}\n\n"
                    await asyncio.sleep(0.001)

                # Handle tool calls
                if hasattr(delta, 'tool_calls') and delta.tool_calls:
                    for tool_call in delta.tool_calls:
                        if tool_call.function:
                            yield f"data: {json.dumps({'type': 'tool_call', 'tool': tool_call.function.name, 'status': 'executing'})}\n\n"

                            # Execute tool (in production, this should be async and properly handled)
                            try:
                                tool_args = json.loads(tool_call.function.arguments)
                                result = agent.execute_tool(tool_call.function.name, tool_args)

                                yield f"data: {json.dumps({'type': 'tool_result', 'tool': tool_call.function.name, 'result': result, 'status': 'success'})}\n\n"
                            except Exception as e:
                                yield f"data: {json.dumps({'type': 'tool_result', 'tool': tool_call.function.name, 'error': str(e), 'status': 'error'})}\n\n"

            # Send completion
            yield f"data: {json.dumps({'type': 'done', 'content': current_content})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@router.get("/health")
async def streaming_health():
    """Check if streaming is available"""
    return {
        "status": "healthy",
        "streaming_enabled": True,
        "model": "llama-3.3-70b-versatile"
    }
