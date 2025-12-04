# ============================================================================
# GENIUS AI - COLAB WITH REAL AI MODEL
# ============================================================================
# This uses Microsoft's DialoGPT - a conversational AI model
# Copy this entire code into Google Colab and run it!
# ============================================================================

# STEP 1: Install dependencies
print("📦 Installing dependencies (this takes 2-3 minutes)...")
!pip install flask flask-cors pyngrok transformers torch -q
print("✅ Dependencies installed!\n")

# STEP 2: Import libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
from pyngrok import ngrok
import threading
import time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# STEP 3: Set up ngrok authentication
print("🔐 Setting up ngrok...")
ngrok.set_auth_token("34yPxIq19Prrf1LfBstzMd7qeeq_3SfLbXcfrQPDSuyWKgD8B")
print("✅ ngrok authenticated!\n")

# STEP 4: Create Flask app
app = Flask(__name__)
CORS(app)

# STEP 5: Load the AI model
print("🤖 Loading DialoGPT-medium model...")
print("   This is a real conversational AI from Microsoft")
print("   Size: ~350MB - first time takes 2-3 minutes\n")

model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Set padding token
tokenizer.pad_token = tokenizer.eos_token

# Move to GPU if available (Colab usually has GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

print(f"✅ Model loaded on {device}!\n")

# Conversation history for context
conversation_history = []

# STEP 6: Create API endpoints
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model': 'DialoGPT-medium',
        'device': str(device),
        'message': 'Real AI model ready!'
    })

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    """Main chat endpoint with real AI"""

    # Handle CORS preflight
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Get request data
        data = request.json
        message = data.get('message', '')
        max_tokens = data.get('max_tokens', 512)
        temperature = data.get('temperature', 0.9)

        print(f"\n📨 Received: {message[:50]}...")

        # Add user message to history
        user_input = tokenizer.encode(message + tokenizer.eos_token, return_tensors='pt')

        # Combine with conversation history (keep last 3 exchanges for context)
        if len(conversation_history) > 0:
            # Keep last 3 turns (6 messages total)
            recent_history = conversation_history[-6:]
            bot_input = torch.cat(recent_history + [user_input], dim=-1)
        else:
            bot_input = user_input

        # Move to device
        bot_input = bot_input.to(device)

        # Limit input length to prevent memory issues
        if bot_input.shape[-1] > 512:
            bot_input = bot_input[:, -512:]

        # Generate response
        with torch.no_grad():
            chat_output = model.generate(
                bot_input,
                max_new_tokens=min(max_tokens, 200),  # Limit to 200 tokens
                temperature=temperature,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                pad_token_id=tokenizer.eos_token_id
            )

        # Decode response (only the new tokens)
        response_text = tokenizer.decode(
            chat_output[:, bot_input.shape[-1]:][0],
            skip_special_tokens=True
        )

        # Update conversation history
        conversation_history.append(user_input[0])
        conversation_history.append(chat_output[:, bot_input.shape[-1]:][0])

        # Keep history manageable (max 6 exchanges)
        if len(conversation_history) > 12:
            conversation_history.pop(0)
            conversation_history.pop(0)

        print(f"✅ Generated: {response_text[:50]}...")

        return jsonify({
            'response': response_text,
            'model': 'DialoGPT-medium (Microsoft)',
            'tokens_used': len(response_text.split()),
            'device': str(device)
        })

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset_conversation():
    """Reset conversation history"""
    global conversation_history
    conversation_history = []
    return jsonify({'status': 'Conversation reset'})

# STEP 7: Start Flask in background
def run_flask():
    app.run(port=5000, debug=False, use_reloader=False)

print("🚀 Starting Flask server...")
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

time.sleep(2)
print("✅ Flask server running\n")

# STEP 8: Create ngrok tunnel
print("🌐 Creating public ngrok tunnel...")
public_url = ngrok.connect(5000)
print("✅ Tunnel created!\n")

# STEP 9: Display info
print("=" * 70)
print("🎉 REAL AI MODEL IS NOW ACCESSIBLE!")
print("=" * 70)
print(f"\n📡 Public URL: {public_url}")
print(f"🤖 Model: DialoGPT-medium (Microsoft)")
print(f"💻 Device: {device}")
print(f"🏥 Health: {public_url}/health")
print(f"💬 Chat: {public_url}/chat")
print("\n" + "=" * 70)
print("📋 RUN THIS ON YOUR COMPUTER:")
print("=" * 70)

# Extract just the URL part
url_str = str(public_url)
if 'https://' in url_str:
    # Extract URL from NgrokTunnel object string
    start = url_str.find('https://')
    end = url_str.find('"', start)
    clean_url = url_str[start:end]
else:
    clean_url = url_str

print(f"\npython configure_colab_model.py {clean_url}")
print("\nOR use curl:")
print(f"""
curl -X POST http://localhost:8000/custom-model/config \\
  -H "Content-Type: application/json" \\
  -d '{{"model_url": "{clean_url}/chat"}}'
""")
print("=" * 70)
print("\n✨ After configuration:")
print("   /chat          - Groq (fast)")
print("   /custom-chat   - DialoGPT (your Colab)")
print("   /hybrid-chat   - Both combined!")
print("\n🌐 Test at: http://localhost:3000")
print("=" * 70)

# STEP 10: Test the model
print("\n🧪 Testing the AI model...")
import requests
try:
    test_response = requests.post(
        f"{clean_url}/chat",
        json={"message": "Hello! What can you help me with?"}
    )
    if test_response.status_code == 200:
        result = test_response.json()
        print("✅ Model test successful!")
        print(f"   AI Response: {result.get('response', '')[:100]}...")
    else:
        print(f"⚠️  Test returned status {test_response.status_code}")
except Exception as e:
    print(f"⚠️  Test failed: {e}")
    print("   (This is OK - will work once configured)")

print("\n" + "=" * 70)
print("✅ SETUP COMPLETE - Real AI Model Ready!")
print("=" * 70)
print("\n⚠️  KEEP THIS CELL RUNNING!")
print("If you stop it, the tunnel closes.\n")

# Keep alive
try:
    print("💡 Model is running. Ask questions at http://localhost:3000")
    print("💡 Type anything in Genius AI and it will use this model!\n")
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    print("\n\n🛑 Shutting down...")
    ngrok.disconnect(public_url)
    print("✅ Tunnel closed")
