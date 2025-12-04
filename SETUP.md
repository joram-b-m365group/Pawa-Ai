# Genius AI - Setup Guide

This guide will help you set up and run your advanced AI chat system.

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose (optional)
- NVIDIA GPU with CUDA support (optional, but recommended)
- At least 16GB RAM (32GB+ recommended for larger models)

## Quick Start with Docker

The easiest way to get started:

```bash
# Clone or navigate to the project
cd genius-ai

# Copy environment file
cp backend/.env.example backend/.env

# Edit backend/.env and configure your settings
# Important: Set DEVICE=cuda if you have a GPU, or DEVICE=cpu otherwise

# Start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Manual Setup

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Start the backend:**
```bash
python -m genius_ai.api.server
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Create environment file:**
```bash
# Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env
```

4. **Start development server:**
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Configuration

### Model Selection

Edit `backend/.env`:

```env
# For Mistral (recommended, smaller, faster)
BASE_MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.2

# For LLaMA 2 (requires approval from Meta)
BASE_MODEL_NAME=meta-llama/Llama-2-7b-chat-hf

# For larger, more capable models (requires more VRAM)
BASE_MODEL_NAME=mistralai/Mixtral-8x7B-Instruct-v0.1
```

### Device Configuration

```env
# Use CUDA (requires NVIDIA GPU)
DEVICE=cuda

# Use Metal (for Apple Silicon Macs)
DEVICE=mps

# Use CPU (slower, but works everywhere)
DEVICE=cpu
```

### Memory Configuration

```env
# Adjust based on your RAM
MAX_CONVERSATION_HISTORY=50
MEMORY_WINDOW_SIZE=4096

# For limited memory
MAX_CONVERSATION_HISTORY=20
MEMORY_WINDOW_SIZE=2048
```

## Advanced Features

### 1. Knowledge Base (RAG)

Add documents to the knowledge base:

```python
# Via API
import requests

response = requests.post(
    'http://localhost:8000/documents',
    json={
        'content': 'Your document content here...',
        'metadata': {
            'source': 'documentation',
            'category': 'technical'
        }
    }
)
```

### 2. Fine-tuning

Fine-tune the model on your data:

```bash
cd backend
python -m genius_ai.training.fine_tune \
    --dataset path/to/dataset.json \
    --output models/fine-tuned
```

### 3. Multi-Agent System

The orchestrator automatically uses:
- **Reasoning Agent**: Analyzes and breaks down problems
- **Planning Agent**: Creates action plans
- **Reflection Agent**: Improves responses

Configure in `backend/.env`:
```env
ENABLE_REFLECTION=true
MAX_AGENT_ITERATIONS=10
```

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Performance Optimization

### For GPU Users

1. **Enable quantization** (reduces VRAM usage):
```env
USE_LORA=true
LORA_R=8
```

2. **Batch processing**:
```env
API_WORKERS=4
```

### For CPU Users

1. **Use smaller models**:
```env
BASE_MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.2
```

2. **Reduce context window**:
```env
MEMORY_WINDOW_SIZE=2048
AGENT_MAX_TOKENS=1024
```

## Troubleshooting

### Out of Memory

- Reduce `MEMORY_WINDOW_SIZE`
- Enable quantization
- Use a smaller model
- Reduce `MAX_CONVERSATION_HISTORY`

### Slow Responses

- Use GPU if available
- Reduce `AGENT_MAX_TOKENS`
- Disable reflection: `ENABLE_REFLECTION=false`
- Increase `API_WORKERS`

### Model Download Issues

Models are downloaded from Hugging Face. If downloads fail:

1. Check internet connection
2. Set Hugging Face token (for gated models):
```bash
export HUGGING_FACE_TOKEN=your_token_here
```

3. Manually download to `models/cache/`

## Production Deployment

### Security Checklist

- [ ] Change `SECRET_KEY` in `.env`
- [ ] Set up proper CORS origins
- [ ] Use HTTPS
- [ ] Set up authentication
- [ ] Configure rate limiting
- [ ] Set up monitoring

### Deployment Options

1. **Docker + Cloud VM** (AWS, GCP, Azure)
2. **Kubernetes** (for scaling)
3. **Serverless** (with model served separately)

### Scaling

- Use load balancer for multiple backend instances
- Separate vector database (hosted ChromaDB)
- Use managed PostgreSQL
- Implement caching with Redis

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

### Example API Calls

**Send a chat message:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain quantum computing",
    "use_rag": true,
    "temperature": 0.7
  }'
```

**Add a document:**
```bash
curl -X POST "http://localhost:8000/documents" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Quantum computing uses quantum bits...",
    "metadata": {"source": "wiki"}
  }'
```

## Next Steps

1. **Customize agents** - Edit agent prompts in `backend/src/genius_ai/agents/`
2. **Add tools** - Create custom tools in `backend/src/genius_ai/tools/`
3. **Train on your data** - Fine-tune with domain-specific data
4. **Extend capabilities** - Add image processing, web search, etc.

## Support

For issues and questions:
- Check the logs in `backend/logs/`
- Review API docs at `/docs`
- Check model compatibility on Hugging Face

## License

MIT License - See LICENSE file for details
