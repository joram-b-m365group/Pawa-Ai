"""
AI Code Agent API - Fixed Version
Handles Groq function calling issues with fallback
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from groq import Groq
import json
import re
from ai_agent_tools import AIAgentTools

router = APIRouter(prefix="/ai-agent", tags=["AI Agent"])

# Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

# Store active agent sessions
agent_sessions: Dict[str, AIAgentTools] = {}

AI_AGENT_FALLBACK_PROMPT = """You are Pawa AI Code Agent - an ELITE software architect and engineer with 20 years of experience.

Your mission: Create PRODUCTION-READY, SOPHISTICATED, COMPLEX software that rivals professional development agencies.

========================================
CORE PRINCIPLES - READ CAREFULLY:
========================================

1. **PRODUCTION QUALITY ONLY**
   - Never create toy examples or placeholders
   - Every file must be deployment-ready
   - Include proper error handling, validation, security
   - Add comprehensive comments and documentation

2. **ARCHITECTURE FIRST**
   - Think about scalability, maintainability, performance
   - Use modern best practices and design patterns
   - Implement proper separation of concerns
   - Include configuration, logging, monitoring

3. **COMPLETE FEATURES**
   - Full authentication systems (JWT, sessions, OAuth)
   - Database integration (models, migrations, queries)
   - API design (REST, GraphQL, proper endpoints)
   - Frontend state management (Redux, Zustand, Context)
   - Real-time features (WebSockets, SSE) when needed
   - File uploads, image processing, email sending
   - Testing (unit, integration, E2E)
   - CI/CD configuration
   - Docker/deployment setup

4. **MODERN TECH STACK**
   - React/Next.js with TypeScript for frontend
   - Node.js/Python/Go for backend
   - PostgreSQL/MongoDB for databases
   - Redis for caching
   - AWS/GCP/Azure integrations
   - Modern UI libraries (Tailwind, MUI, Chakra)

========================================
OUTPUT FORMAT:
========================================

FILE: path/to/file.ext
```language
[COMPLETE, PRODUCTION-READY CODE HERE]
```

========================================
EXAMPLE - What GOOD looks like:
========================================

User: "create an e-commerce product management system"

Response:
I'll create a production-ready e-commerce product management system with:
- Complete REST API with authentication
- Database models with relationships
- Admin dashboard with React
- Image upload and processing
- Search and filtering
- Pagination and caching
- Error handling and validation
- API documentation
- Deployment configuration

FILE: backend/src/models/Product.js
```javascript
const mongoose = require('mongoose');

const productSchema = new mongoose.Schema({
  name: {
    type: String,
    required: [true, 'Product name is required'],
    trim: true,
    maxlength: [100, 'Name cannot exceed 100 characters']
  },
  description: {
    type: String,
    required: [true, 'Description is required']
  },
  price: {
    type: Number,
    required: [true, 'Price is required'],
    min: [0, 'Price cannot be negative']
  },
  category: {
    type: String,
    required: true,
    enum: ['Electronics', 'Clothing', 'Books', 'Home', 'Sports']
  },
  images: [{
    url: String,
    alt: String,
    isPrimary: Boolean
  }],
  inventory: {
    quantity: { type: Number, default: 0 },
    lowStockThreshold: { type: Number, default: 10 }
  },
  ratings: {
    average: { type: Number, default: 0 },
    count: { type: Number, default: 0 }
  },
  tags: [String],
  status: {
    type: String,
    enum: ['draft', 'published', 'archived'],
    default: 'draft'
  }
}, {
  timestamps: true,
  toJSON: { virtuals: true }
});

// Indexes for performance
productSchema.index({ name: 'text', description: 'text' });
productSchema.index({ category: 1, status: 1 });

// Virtual for low stock
productSchema.virtual('isLowStock').get(function() {
  return this.inventory.quantity <= this.inventory.lowStockThreshold;
});

module.exports = mongoose.model('Product', productSchema);
```

[... MORE FILES WITH COMPLETE IMPLEMENTATIONS ...]

========================================
YOUR TASK:
========================================

When the user requests software:
1. Analyze requirements thoroughly
2. Design a proper architecture
3. Create ALL necessary files (models, controllers, routes, components, tests, config)
4. Include error handling, validation, security
5. Add documentation and comments
6. Make it production-ready

Now respond to: """


class CodeChatRequest(BaseModel):
    message: str
    project_path: str
    conversation_history: Optional[List[Dict[str, str]]] = []
    session_id: Optional[str] = "default"


class CodeChatResponse(BaseModel):
    response: str
    tool_calls: Optional[List[Dict[str, Any]]] = []
    files_modified: Optional[List[str]] = []
    context_summary: Optional[str] = None


def parse_and_create_files(ai_response: str, agent: AIAgentTools) -> tuple:
    """Parse AI response for FILE: markers and create files"""
    # Pattern to match FILE: path followed by code block
    file_pattern = r'FILE:\s*([^\n]+)\n```(?:\w+\n)?(.*?)```'
    matches = re.findall(file_pattern, ai_response, re.DOTALL)

    tool_calls_made = []
    files_modified = []

    for file_path, content in matches:
        file_path = file_path.strip()
        content = content.strip()

        print(f"📝 Creating file: {file_path} ({len(content)} chars)")

        result = agent.write_file(file_path, content)
        tool_calls_made.append({
            "tool": "write_file",
            "arguments": {"file_path": file_path},
            "result": result
        })

        if result.get("success"):
            files_modified.append(file_path)
            print(f"   ✅ Success: {file_path}")
        else:
            print(f"   ❌ Failed: {result.get('error')}")

    return tool_calls_made, files_modified


@router.post("/chat", response_model=CodeChatResponse)
async def ai_agent_chat(request: CodeChatRequest):
    """AI agent chat with fallback file creation"""
    try:
        # Get or create agent session
        if request.session_id not in agent_sessions:
            agent_sessions[request.session_id] = AIAgentTools(project_root=request.project_path)

        agent = agent_sessions[request.session_id]

        print(f"🤖 AI Agent processing: {request.message}")

        # Use fallback approach (more reliable than function calling with Groq)
        messages = [
            {"role": "system", "content": AI_AGENT_FALLBACK_PROMPT}
        ]

        # Add conversation history
        for msg in request.conversation_history[-10:]:
            messages.append(msg)

        # Add current message
        messages.append({
            "role": "user",
            "content": request.message
        })

        # Get AI response
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=8000
        )

        ai_response = response.choices[0].message.content

        # Parse and create files
        tool_calls_made, files_modified = parse_and_create_files(ai_response, agent)

        # Add success message if files were created
        if files_modified:
            ai_response += f"\n\n✅ Successfully created {len(files_modified)} file(s):\n"
            for f in files_modified:
                ai_response += f"  - {f}\n"

        print(f"✅ AI Agent completed - Created {len(files_modified)} files")

        return CodeChatResponse(
            response=ai_response,
            tool_calls=tool_calls_made,
            files_modified=files_modified,
            context_summary=agent.get_context_summary()
        )

    except Exception as e:
        import traceback
        error_msg = f"❌ Error: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset-session")
async def reset_session(session_id: str = "default"):
    """Reset an agent session"""
    if session_id in agent_sessions:
        del agent_sessions[session_id]
    return {"message": f"Session {session_id} reset"}


@router.get("/available-tools")
async def get_available_tools():
    """Get list of available tools"""
    agent = AIAgentTools()
    return {"tools": agent.get_available_tools()}


@router.post("/execute-tool")
async def execute_tool_directly(
    project_path: str,
    tool_name: str,
    arguments: Dict[str, Any]
):
    """Execute a tool directly (for testing)"""
    agent = AIAgentTools(project_root=project_path)
    result = agent.execute_tool(tool_name, arguments)
    return result
