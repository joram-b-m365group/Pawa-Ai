# Genius AI - Quick Start Guide

Get your advanced AI chat system running in minutes!

## Option 1: Docker (Recommended for Beginners)

### Prerequisites
- Docker and Docker Compose installed
- At least 16GB RAM
- 20GB free disk space

### Steps

1. **Navigate to project:**
```bash
cd genius-ai
```

2. **Configure environment:**
```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` and set:
```env
DEVICE=cpu  # or 'cuda' if you have NVIDIA GPU
```

3. **Start everything:**
```bash
docker-compose up --build
```

Wait for models to download (first time only, ~4-7GB).

4. **Open your browser:**
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

Done! Start chatting!

## Option 2: Manual Setup (For Developers)

### Backend

```bash
# 1. Create virtual environment
cd backend
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure
cp .env.example .env
# Edit .env as needed

# 5. Run
python -m genius_ai.api.server
```

Backend runs at: http://localhost:8000

### Frontend

```bash
# 1. Install dependencies
cd frontend
npm install

# 2. Configure
echo "VITE_API_URL=http://localhost:8000" > .env

# 3. Run
npm run dev
```

Frontend runs at: http://localhost:3000

## First Steps

### 1. Test Basic Chat

Open http://localhost:3000 and try:
- "Explain how you work"
- "Write a Python function to calculate fibonacci"
- "Plan a project for building a web app"

### 2. Add Knowledge

Add documents to the knowledge base:

```bash
curl -X POST "http://localhost:8000/documents" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Your company documentation or knowledge here...",
    "metadata": {"source": "docs", "category": "technical"}
  }'
```

Now ask questions about your documents!

### 3. Explore Multi-Agent Reasoning

Try complex tasks that trigger multiple agents:
- "Analyze the problem of climate change and create an action plan"
- "Debug this code and explain your reasoning step by step"

Watch the metadata in responses to see which agents were used.

## Configuration Tips

### For Faster Responses

In `backend/.env`:
```env
# Use smaller model
BASE_MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.2

# Reduce tokens
AGENT_MAX_TOKENS=1024

# Disable reflection for speed
ENABLE_REFLECTION=false
```

### For Better Quality

```env
# Use larger model
BASE_MODEL_NAME=mistralai/Mixtral-8x7B-Instruct-v0.1

# Increase tokens
AGENT_MAX_TOKENS=2048

# Enable all features
ENABLE_REFLECTION=true
USE_RAG=true
```

### For Low Memory Systems

```env
# Essential settings
DEVICE=cpu
MEMORY_WINDOW_SIZE=2048
MAX_CONVERSATION_HISTORY=20
```

## Common Issues

### "Out of memory"
- Set `DEVICE=cpu` in `.env`
- Use smaller model: `mistralai/Mistral-7B-Instruct-v0.2`
- Reduce `MEMORY_WINDOW_SIZE=2048`

### "Model download failed"
- Check internet connection
- Ensure 10GB+ free disk space
- Try different model

### "Port already in use"
Change ports in `docker-compose.yml` or `.env`:
```yaml
ports:
  - "8001:8000"  # Backend
  - "3001:3000"  # Frontend
```

### "Connection refused"
- Ensure backend is running first
- Check firewall settings
- Verify API_URL in frontend `.env`

## Next Steps

1. **Customize Agents**
   - Edit prompts in `backend/src/genius_ai/agents/`
   - Adjust agent behaviors
   - Add new specialized agents

2. **Add Custom Tools**
   - Create tools in `backend/src/genius_ai/tools/`
   - Enable code execution, web search, etc.

3. **Fine-tune Model**
   - Prepare your training data
   - Run fine-tuning pipeline
   - Deploy custom model

4. **Deploy to Production**
   - Use HTTPS
   - Set up authentication
   - Configure monitoring
   - Scale with Kubernetes

## Example Use Cases

### Personal Assistant
- Schedule management
- Email drafting
- Research assistance
- Note summarization

### Development Assistant
- Code generation
- Bug analysis
- Documentation writing
- Code review

### Business Intelligence
- Data analysis
- Report generation
- Market research
- Strategic planning

### Education
- Tutoring
- Homework help
- Concept explanation
- Study planning

## API Examples

### Chat
```python
import requests

response = requests.post('http://localhost:8000/chat', json={
    'message': 'Explain quantum entanglement',
    'use_rag': True,
    'temperature': 0.7
})

print(response.json()['response'])
```

### Streaming Chat
```python
import requests

def stream_chat(message):
    response = requests.post(
        'http://localhost:8000/chat/stream',
        json={'message': message, 'stream': True},
        stream=True
    )

    for line in response.iter_lines():
        if line.startswith(b'data: '):
            chunk = line[6:].decode('utf-8')
            if chunk == '[DONE]':
                break
            print(chunk, end='', flush=True)

stream_chat("Write a story about AI")
```

### Add Document
```python
import requests

response = requests.post('http://localhost:8000/documents', json={
    'content': 'Python is a high-level programming language...',
    'metadata': {'source': 'wiki', 'topic': 'programming'}
})

print(f"Added {response.json()['chunks_added']} chunks")
```

## Performance Tips

1. **Use GPU**: 5-10x faster
   ```env
   DEVICE=cuda
   ```

2. **Enable Caching**: Install Redis
   ```bash
   docker run -d -p 6379:6379 redis:alpine
   ```

3. **Batch Requests**: Send multiple requests in parallel

4. **Optimize Model**:
   - Use quantization (4-bit)
   - Enable LoRA adapters
   - Reduce context window

## Monitoring

Check system status:
```bash
# Health check
curl http://localhost:8000/health

# View logs
docker-compose logs -f backend

# Monitor resources
docker stats
```

## Getting Help

1. **Check logs**: `backend/logs/` or `docker-compose logs`
2. **API docs**: http://localhost:8000/docs
3. **Read architecture**: See `ARCHITECTURE.md`
4. **Review setup**: See `SETUP.md`

## What Makes Genius AI Special?

✅ **Multi-Agent Reasoning**: Multiple specialized AI agents collaborate
✅ **RAG System**: Retrieves and uses your knowledge base
✅ **Advanced Memory**: Remembers context across conversations
✅ **Self-Reflection**: Critiques and improves its own responses
✅ **Tool Use**: Can execute code, search, and use functions
✅ **Streaming**: Real-time response generation
✅ **Customizable**: Easy to extend and fine-tune
✅ **Production-Ready**: Built with FastAPI, Docker, proper architecture

## Ready to Build Something Amazing?

Start chatting and explore what's possible with advanced AI!

Questions? Issues? Check the documentation or examine the code - it's all designed to be readable and modifiable.

Happy coding! 🚀
