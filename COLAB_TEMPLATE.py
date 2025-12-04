# ============================================================================
# GENIUS AI - COLAB MODEL INTEGRATION TEMPLATE
# ============================================================================
# Copy this entire code into a Google Colab cell and run it
# This will expose your model through ngrok and connect it to Genius AI
# ============================================================================

# STEP 1: Install dependencies
print("📦 Installing dependencies...")
!pip install flask flask-cors pyngrok transformers torch -q
print("✅ Dependencies installed!\n")

# STEP 2: Import libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
from pyngrok import ngrok
import threading
import time

# STEP 3: Set up ngrok authentication (IMPORTANT!)
# Your ngrok token has been pre-configured!
print("🔐 Setting up ngrok...")
ngrok.set_auth_token("34yPxIq19Prrf1LfBstzMd7qeeq_3SfLbXcfrQPDSuyWKgD8B")
print("✅ ngrok authenticated!\n")

# STEP 4: Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for Genius AI

# STEP 5: Load your model (CUSTOMIZE THIS SECTION!)
print("🤖 Loading your model...")

# Option A: Use Hugging Face model (example)
# from transformers import AutoModelForCausalLM, AutoTokenizer
# model_name = "microsoft/DialoGPT-medium"  # Change to your model
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name)

# Option B: Use a simple echo bot (for testing)
def simple_model(message):
    """Simple echo model for testing - REPLACE with your actual model"""
    return f"Echo from Colab: {message}\n\nThis is a test response. Replace this with your actual model inference code."

print("✅ Model loaded!\n")

# STEP 6: Create API endpoints
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model': 'Colab Custom Model',
        'message': 'Model is ready!'
    })

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    """Main chat endpoint for Genius AI"""

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
        temperature = data.get('temperature', 0.9)
        max_tokens = data.get('max_tokens', 512)

        print(f"\n📨 Received: {message[:50]}...")

        # CUSTOMIZE THIS: Replace with your model inference
        # Example for simple echo:
        response_text = simple_model(message)

        # Example for Hugging Face model:
        # inputs = tokenizer.encode(message, return_tensors='pt')
        # outputs = model.generate(
        #     inputs,
        #     max_new_tokens=max_tokens,
        #     temperature=temperature,
        #     do_sample=True
        # )
        # response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        print(f"✅ Generated response")

        # Return response in Genius AI format
        return jsonify({
            'response': response_text,
            'model': 'Colab Custom Model',
            'tokens_used': len(response_text.split())
        })

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'error': str(e)}), 500

# STEP 7: Start Flask in background
def run_flask():
    app.run(port=5000, debug=False, use_reloader=False)

print("🚀 Starting Flask server...")
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()

# Wait for Flask to start
time.sleep(2)
print("✅ Flask server running on port 5000\n")

# STEP 8: Create ngrok tunnel
print("🌐 Creating public ngrok tunnel...")
public_url = ngrok.connect(5000)
print("✅ Tunnel created!\n")

# STEP 9: Display configuration info
print("=" * 70)
print("🎉 YOUR MODEL IS NOW ACCESSIBLE!")
print("=" * 70)
print(f"\n📡 Public URL: {public_url}")
print(f"🏥 Health Check: {public_url}/health")
print(f"💬 Chat Endpoint: {public_url}/chat")
print("\n" + "=" * 70)
print("📋 COPY THIS COMMAND AND RUN IT IN YOUR LOCAL TERMINAL:")
print("=" * 70)
print(f"\npython configure_colab_model.py {public_url}")
print("\nOR manually configure with curl:")
print(f"""
curl -X POST http://localhost:8000/custom-model/config \\
  -H "Content-Type: application/json" \\
  -d '{{"model_url": "{public_url}/chat"}}'
""")
print("=" * 70)
print("\n✨ After configuration, use these endpoints in Genius AI:")
print("   /chat          - Groq only (fast)")
print("   /custom-chat   - Your Colab model")
print("   /hybrid-chat   - Groq + Your model (recommended!)")
print("\n🌐 Open Genius AI: http://localhost:3000")
print("=" * 70)

# STEP 10: Keep the server running
print("\n⚠️  KEEP THIS CELL RUNNING!")
print("If you stop this cell, the ngrok tunnel will close.\n")

# Test the endpoint
print("🧪 Testing endpoint...")
import requests
try:
    test = requests.post(f"{public_url}/chat", json={"message": "test"})
    if test.status_code == 200:
        print("✅ Endpoint test successful!")
    else:
        print(f"⚠️  Endpoint returned status {test.status_code}")
except Exception as e:
    print(f"⚠️  Endpoint test failed: {e}")

print("\n" + "=" * 70)
print("✅ SETUP COMPLETE - Ready to use with Genius AI!")
print("=" * 70)

# Keep alive loop
try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    print("\n\n🛑 Shutting down...")
    ngrok.disconnect(public_url)
    print("✅ Tunnel closed")
