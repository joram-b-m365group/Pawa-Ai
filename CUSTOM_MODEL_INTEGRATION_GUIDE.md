# 🔌 Custom Model Integration Guide - Genius AI

Connect your own AI models (from Colab, local servers, or cloud endpoints) to Genius AI!

---

## 🎯 What This Enables

### 3 Model Modes:
1. **Groq Mode** (Default) - Fast, free Llama 3.3 70B with super intelligence
2. **Custom Mode** - Your own model (Colab, local, or cloud)
3. **Hybrid Mode** - Best of both! Groq for reasoning + Your model for generation

---

## 📡 Backend Endpoints

### 1. Configure Custom Model
**POST** `/custom-model/config`

Set your custom model URL (e.g., from Colab ngrok tunnel):

```json
{
  "model_url": "https://your-ngrok-url.ngrok.io/chat",
  "model_name": "My Custom Model",
  "timeout": 60
}
```

**Response:**
```json
{
  "success": true,
  "message": "Custom model configured successfully",
  "model_url": "https://your-ngrok-url.ngrok.io/chat",
  "model_name": "My Custom Model"
}
```

---

### 2. Check Configuration
**GET** `/custom-model/config`

Check if custom model is configured:

```json
{
  "model_url": "https://your-ngrok-url.ngrok.io/chat",
  "is_configured": true
}
```

---

### 3. Chat with Custom Model
**POST** `/custom-chat`

Use your custom model directly:

```json
{
  "message": "Explain quantum computing",
  "temperature": 0.9,
  "max_tokens": 16000,
  "system_prompt": "You are a helpful assistant"
}
```

**Response:**
```json
{
  "response": "Quantum computing is...",
  "model": "Custom Model (Colab)",
  "tokens_used": 150,
  "processing_time": 3.5
}
```

---

### 4. Hybrid Mode (Groq + Custom)
**POST** `/hybrid-chat`

Get the best of both worlds:
- **Groq**: Fast reasoning and analysis
- **Custom Model**: Specialized generation

Same request format as `/chat`:
```json
{
  "message": "Solve this calculus problem",
  "temperature": 0.9
}
```

**How it works:**
1. Groq analyzes the query and creates structured reasoning
2. Custom model receives Groq's analysis + original question
3. Response combines both intelligences
4. Falls back to Groq if custom model fails

---

## 🚀 Setup Guide: Colab Model

### Step 1: Prepare Your Colab Notebook

Your Colab endpoint must accept POST requests with this format:

```python
# In your Colab notebook:
from flask import Flask, request, jsonify
from pyngrok import ngrok

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message')
    temperature = data.get('temperature', 0.9)
    max_tokens = data.get('max_tokens', 16000)

    # Your model inference here
    response_text = your_model.generate(message, temperature, max_tokens)

    return jsonify({
        'response': response_text,
        'model': 'My Custom Model',
        'tokens_used': len(response_text.split())
    })

# Start ngrok tunnel
public_url = ngrok.connect(5000)
print(f"Public URL: {public_url}")

# Run Flask
app.run(port=5000)
```

---

### Step 2: Get Your ngrok URL

When you run the Colab cell, you'll see:
```
Public URL: https://abc123.ngrok.io
```

Copy this URL!

---

### Step 3: Configure Genius AI

**Option A: Using curl**
```bash
curl -X POST http://localhost:8000/custom-model/config \
  -H "Content-Type: application/json" \
  -d '{
    "model_url": "https://abc123.ngrok.io/chat",
    "model_name": "My Colab Model"
  }'
```

**Option B: Using Python**
```python
import requests

requests.post('http://localhost:8000/custom-model/config', json={
    'model_url': 'https://abc123.ngrok.io/chat',
    'model_name': 'My Colab Model'
})
```

**Option C: Using the UI** (coming soon in next update!)

---

### Step 4: Test Your Connection

```bash
curl -X POST http://localhost:8000/custom-chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello from Genius AI!"
  }'
```

---

## 🔧 Troubleshooting

### Error: "Failed to fetch"

**Possible causes:**
1. **Colab isn't running** - Make sure your Colab cell is running
2. **ngrok tunnel expired** - Restart the Colab cell to get a new URL
3. **CORS issue** - Add CORS headers to your Colab endpoint:

```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # Enable CORS
```

4. **Wrong URL** - Double-check the ngrok URL and `/chat` path

---

### Error: "Custom model request timed out"

**Solutions:**
- Increase timeout in config: `"timeout": 120`
- Optimize your model for faster inference
- Use a smaller model or reduce max_tokens

---

### Error: "Cannot connect to custom model"

**Check:**
- Is Colab running?
- Is ngrok active? (Check the Colab logs)
- Can you access the URL in your browser?
- Is the endpoint path correct? (should be `/chat`)

---

## 💡 Example Colab Template

Complete Colab notebook template with Genius AI integration:

```python
# Install dependencies
!pip install flask pyngrok transformers torch -q

from flask import Flask, request, jsonify
from flask_cors import CORS
from pyngrok import ngrok
import threading

app = Flask(__name__)
CORS(app)  # Enable CORS for Genius AI

# Load your model (example with Hugging Face)
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "your-model-name"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model': model_name})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        temperature = data.get('temperature', 0.9)
        max_tokens = data.get('max_tokens', 512)

        # Generate response
        inputs = tokenizer(message, return_tensors='pt')
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature,
            do_sample=True
        )

        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return jsonify({
            'response': response_text,
            'model': model_name,
            'tokens_used': len(outputs[0])
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run Flask in background thread
def run_flask():
    app.run(port=5000, debug=False)

flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Start ngrok tunnel
public_url = ngrok.connect(5000)
print("=" * 60)
print("🚀 MODEL API READY!")
print("=" * 60)
print(f"Public URL: {public_url}")
print(f"Health Check: {public_url}/health")
print(f"Chat Endpoint: {public_url}/chat")
print("=" * 60)
print("\n📝 Configure Genius AI with:")
print(f"curl -X POST http://localhost:8000/custom-model/config \\")
print(f'  -H "Content-Type: application/json" \\')
print(f"  -d '{{\"model_url\": \"{public_url}/chat\"}}'")
print("=" * 60)

# Keep alive
import time
while True:
    time.sleep(60)
```

---

## 🎨 Frontend Integration (Coming Next!)

The next update will add a UI with:
- Model selector dropdown (Groq / Custom / Hybrid)
- Custom model URL configuration form
- Connection status indicator
- Automatic fallback to Groq if custom model fails

---

## 🔐 Security Notes

### Best Practices:
✅ Use HTTPS (ngrok provides this automatically)
✅ Add authentication to your Colab endpoint if needed
✅ Set reasonable timeouts
✅ Validate input data
✅ Rate limit your custom endpoint

### Never:
❌ Expose API keys in public URLs
❌ Store sensitive data in Colab without encryption
❌ Use custom models for sensitive/private data without proper security

---

## 🌟 Advanced Use Cases

### 1. Domain-Specific Model
Train a model on medical/legal/technical docs, use Hybrid mode:
- Groq provides general reasoning
- Your model provides domain expertise

### 2. Multi-Language Model
Use a model fine-tuned for your language:
- Switch to Custom mode for native language support

### 3. Local Model (Privacy)
Run models locally without internet:
```python
# In your local setup:
model_url = "http://localhost:11434/api/generate"  # Ollama example
```

### 4. Cloud Deployment
Deploy your model on AWS/GCP/Azure:
```python
model_url = "https://your-api.cloud.com/v1/chat"
```

---

## 📊 Performance Comparison

| Mode | Speed | Quality | Cost | Best For |
|------|-------|---------|------|----------|
| **Groq** | ⚡⚡⚡ Very Fast (1-3s) | 🎯 Excellent | 💰 FREE | General use, reasoning |
| **Custom** | 🐢 Depends on model | 🎯 Varies | 💰 Your compute | Specialized tasks |
| **Hybrid** | ⚡⚡ Fast (3-6s) | 🎯 Best | 💰 FREE + Your compute | Complex, domain-specific |

---

## 🎯 Quick Start Checklist

- [ ] Run your model in Colab with Flask + ngrok
- [ ] Copy the ngrok URL
- [ ] Configure Genius AI with POST /custom-model/config
- [ ] Test with /custom-chat endpoint
- [ ] Try Hybrid mode with /hybrid-chat
- [ ] Integrate with frontend (coming soon!)

---

## 📞 Support

### Check Status:
```bash
# Backend health
curl http://localhost:8000/health

# Custom model config
curl http://localhost:8000/custom-model/config

# Colab health (replace URL)
curl https://your-ngrok-url.ngrok.io/health
```

### Debug Mode:
Check backend logs for detailed error messages:
```
Custom Model Error: [error details]
```

---

## 🎉 What's Next?

**Coming in v8.0:**
- ✨ Model switching UI with dropdown
- ✨ Visual connection status indicator
- ✨ Built-in Colab template generator
- ✨ Performance metrics dashboard
- ✨ Multiple custom models support
- ✨ Model A/B testing

---

**Made with ❤️ for Genius AI**
*Connecting the world's AI models, one API at a time!* 🌐🤖
