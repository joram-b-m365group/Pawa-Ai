"""
Quick Demo Server for Genius AI
This is a simplified version that runs immediately without heavy ML dependencies.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any
import uvicorn
import asyncio
from uuid import uuid4

# Create FastAPI app
app = FastAPI(
    title="Genius AI Demo API",
    description="Quick demo of the Genius AI system",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
conversations = {}

# Request/Response Models
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_id: str | None = None
    use_rag: bool = True
    temperature: float = 0.7
    max_tokens: int = 2048

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    model: str = "demo-mode"
    tokens_used: int = 0
    metadata: dict[str, Any] = {}
    timestamp: datetime = Field(default_factory=datetime.now)

class HealthResponse(BaseModel):
    status: str
    version: str
    model_loaded: bool
    timestamp: datetime = Field(default_factory=datetime.now)

# Demo response generator
def generate_demo_response(message: str, use_rag: bool = False) -> str:
    """Generate a demo response simulating the multi-agent system."""

    message_lower = message.lower()

    # Simulate reasoning about different topics
    if any(word in message_lower for word in ["quantum", "physics", "science"]):
        return """**Genius AI Response:**

*[Reasoning Agent Analysis]*
You've asked about a complex scientific topic. Let me break this down systematically.

*[Planning Agent Strategy]*
I'll approach this by:
1. Explaining the core concept
2. Providing practical examples
3. Discussing real-world applications

**Answer:**
Quantum computing leverages quantum mechanical phenomena like superposition and entanglement to process information in fundamentally different ways than classical computers.

Key principles:
- **Superposition**: Qubits can exist in multiple states simultaneously
- **Entanglement**: Qubits can be correlated in ways classical bits cannot
- **Quantum Gates**: Operations that manipulate quantum states

**Real-world applications:**
- Drug discovery and molecular simulation
- Cryptography and security
- Optimization problems
- Machine learning acceleration

*[Reflection Agent Review]*
This explanation covers the fundamentals while remaining accessible. For deeper understanding, I recommend exploring specific quantum algorithms like Shor's algorithm or Grover's algorithm.

Would you like me to elaborate on any specific aspect?"""

    elif any(word in message_lower for word in ["code", "program", "python", "function"]):
        return """**Genius AI Response:**

*[Reasoning Agent Analysis]*
You're asking for code assistance. I'll provide a well-structured, documented solution.

*[Planning Agent Strategy]*
Steps to create a quality solution:
1. Understand the requirements
2. Design the algorithm
3. Implement with best practices
4. Add documentation and examples

**Code Solution:**

```python
def fibonacci(n: int) -> int:
    \"\"\"
    Calculate the nth Fibonacci number using dynamic programming.

    Args:
        n: The position in the Fibonacci sequence (0-indexed)

    Returns:
        The nth Fibonacci number

    Example:
        >>> fibonacci(10)
        55
    \"\"\"
    if n <= 1:
        return n

    # Use dynamic programming for efficiency
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr

    return curr

# Usage examples
print(fibonacci(0))   # Output: 0
print(fibonacci(1))   # Output: 1
print(fibonacci(10))  # Output: 55
```

**Explanation:**
- Time Complexity: O(n)
- Space Complexity: O(1)
- Uses iterative approach for efficiency
- Includes type hints and docstring

*[Reflection Agent Review]*
The solution is efficient and well-documented. For very large values of n, consider using memoization or matrix exponentiation for even better performance.

Need help with anything else?"""

    elif any(word in message_lower for word in ["plan", "strategy", "how to", "steps"]):
        return """**Genius AI Response:**

*[Reasoning Agent Analysis]*
This requires strategic planning and systematic thinking.

*[Planning Agent Strategy]*
Let me create a comprehensive action plan:

**Strategic Plan:**

**Phase 1: Preparation & Analysis** (Week 1-2)
- Research and gather requirements
- Identify stakeholders and resources
- Define success criteria
- Risk assessment

**Phase 2: Design & Architecture** (Week 3-4)
- Create detailed specifications
- Design system architecture
- Plan technology stack
- Establish development workflow

**Phase 3: Implementation** (Week 5-8)
- Set up development environment
- Build core functionality
- Implement features iteratively
- Regular testing and code reviews

**Phase 4: Testing & Refinement** (Week 9-10)
- Comprehensive testing (unit, integration, E2E)
- Performance optimization
- Bug fixes and improvements
- Documentation completion

**Phase 5: Deployment & Launch** (Week 11-12)
- Staging environment testing
- Production deployment
- Monitoring and analytics setup
- User training and onboarding

**Key Success Factors:**
✓ Clear milestones and deadlines
✓ Regular progress reviews
✓ Agile methodology for flexibility
✓ Stakeholder communication
✓ Quality assurance throughout

*[Reflection Agent Review]*
This plan provides a solid framework. Adjust timelines based on your specific context and resources. Consider adding contingency buffers for unexpected challenges.

What aspect would you like to explore in more detail?"""

    elif "how are you" in message_lower or "hello" in message_lower or "hi" in message_lower:
        return """**Genius AI Response:**

Hello! 👋 I'm Genius AI - an advanced conversational AI system powered by multi-agent reasoning.

**What makes me special:**
🧠 **Multi-Agent Architecture**: I use specialized reasoning, planning, and reflection agents
📚 **Knowledge Grounding**: I can access and use custom knowledge bases
💭 **Self-Reflection**: I critique and improve my own responses
🎯 **Task Planning**: I break down complex problems systematically

**What I can help with:**
- Complex problem solving and analysis
- Code generation and debugging
- Strategic planning and decision making
- Technical explanations
- Research and learning assistance

*Note: This is a demo mode. The full system includes actual AI models, RAG with vector database, and advanced memory systems.*

Try asking me about:
- "Explain quantum computing"
- "Write a Python function"
- "Create a plan for building a web app"
- "Analyze and solve a complex problem"

What would you like to explore?"""

    else:
        # General response
        return f"""**Genius AI Response:**

*[Reasoning Agent Analysis]*
Let me analyze your question: "{message}"

This is an interesting query that requires thoughtful consideration. Let me break down my thinking:

**Analysis:**
I understand you're asking about {message_lower.split()[0] if message_lower.split() else 'this topic'}. This involves several considerations:

1. **Context**: Understanding the broader context and implications
2. **Approach**: Determining the most effective way to address this
3. **Outcomes**: Considering potential results and next steps

**Key Points:**
- The topic involves multiple perspectives
- There are several approaches to consider
- Practical application depends on your specific needs

*[Planning Agent Input]*
To provide more targeted assistance, I recommend:
1. Clarifying specific aspects you're most interested in
2. Identifying your goals and constraints
3. Determining the level of detail needed

*[Reflection Agent Review]*
I notice this response is somewhat general. For a more specific and valuable answer, please provide additional context about:
- What specific aspect you're most interested in
- Your background or experience level
- What you're hoping to accomplish

**How can I help you further?**
Please feel free to ask more specific questions, and I'll provide detailed, actionable insights!

---
*Note: This is demo mode. The full system uses actual AI models with RAG, advanced memory, and deeper reasoning capabilities.*"""

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Genius AI Demo API",
        "version": "0.1.0",
        "status": "running",
        "mode": "demo",
        "message": "Multi-agent reasoning system (demo mode)"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="0.1.0-demo",
        model_loaded=True,
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Chat endpoint with simulated multi-agent response."""
    try:
        # Get or create conversation
        conversation_id = request.conversation_id or str(uuid4())

        if conversation_id not in conversations:
            conversations[conversation_id] = []

        # Add user message
        conversations[conversation_id].append({
            "role": "user",
            "content": request.message,
            "timestamp": datetime.now()
        })

        # Simulate processing delay
        await asyncio.sleep(0.5)

        # Generate response
        response_text = generate_demo_response(request.message, request.use_rag)

        # Add assistant response
        conversations[conversation_id].append({
            "role": "assistant",
            "content": response_text,
            "timestamp": datetime.now()
        })

        return ChatResponse(
            response=response_text,
            conversation_id=conversation_id,
            model="genius-ai-demo",
            tokens_used=len(request.message.split()) + len(response_text.split()),
            metadata={
                "mode": "demo",
                "agents_used": ["reasoning", "planning", "reflection"],
                "conversation_length": len(conversations[conversation_id])
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history."""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return {
        "conversation_id": conversation_id,
        "messages": conversations[conversation_id],
        "message_count": len(conversations[conversation_id])
    }

@app.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation."""
    if conversation_id in conversations:
        del conversations[conversation_id]
        return {"message": "Conversation deleted"}
    raise HTTPException(status_code=404, detail="Conversation not found")

def main():
    """Run the demo server."""
    print("\n" + "="*60)
    print("🚀 Starting Genius AI Demo Server")
    print("="*60)
    print("\n📝 Note: This is a DEMO version showing the system architecture.")
    print("   The full version includes actual AI models, RAG, and more.\n")
    print("🌐 Server will start at: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("\n💡 Make sure to start the frontend at: http://localhost:3000")
    print("="*60 + "\n")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )

if __name__ == "__main__":
    main()
