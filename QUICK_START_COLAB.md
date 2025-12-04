# 🚀 Quick Start: Connect Your Colab Model to Genius AI

## The Problem You're Facing

You're getting **"Failed to fetch"** error from Colab. This means Genius AI can't reach your Colab model.

## Solution (5 Minutes Setup)

### Step 1: Get Your ngrok Token (1 minute)

1. Go to: https://dashboard.ngrok.com/signup
2. Sign up for free (or login)
3. Copy your authtoken from: https://dashboard.ngrok.com/get-started/your-authtoken
4. It looks like: `2abc...xyz123`

---

### Step 2: Set Up Colab (2 minutes)

1. **Open Google Colab**: https://colab.research.google.com
2. **Create a new notebook**
3. **Copy the entire code** from `COLAB_TEMPLATE.py`
4. **IMPORTANT: Replace this line:**
   ```python
   ngrok.set_auth_token("YOUR_NGROK_AUTH_TOKEN_HERE")
   ```
   With your actual token:
   ```python
   ngrok.set_auth_token("2abc...xyz123")  # Your token
   ```
5. **Run the cell** (Ctrl+Enter or click ▶️)

---

### Step 3: Wait for Setup (1 minute)

You'll see:
```
📦 Installing dependencies...
✅ Dependencies installed!
🤖 Loading your model...
✅ Model loaded!
🚀 Starting Flask server...
✅ Flask server running
🌐 Creating public ngrok tunnel...
✅ Tunnel created!

🎉 YOUR MODEL IS NOW ACCESSIBLE!
📡 Public URL: https://abc123.ngrok.io
```

**IMPORTANT:** Copy the URL! (e.g., `https://abc123.ngrok.io`)

---

### Step 4: Configure Genius AI (1 minute)

**On your local computer**, open terminal/command prompt and run:

```bash
python configure_colab_model.py https://abc123.ngrok.io
```

(Replace `https://abc123.ngrok.io` with YOUR URL from Step 3)

You should see:
```
✅ Configuration successful!
✅ Connection test successful!
READY TO USE!
```

---

### Step 5: Test It! (30 seconds)

Open http://localhost:3000 and ask a question!

The custom model is now available through the `/custom-chat` endpoint.

---

## Troubleshooting

### Error: "Failed to fetch"

**Cause 1: Colab cell stopped running**
- ✅ Make sure the Colab cell is still running
- ✅ You should see a green checkmark and "Keep this cell running"

**Cause 2: Wrong URL**
- ✅ Copy the EXACT URL from Colab output
- ✅ Include https:// at the beginning
- ✅ Don't add /chat at the end (the script does this automatically)

**Cause 3: ngrok token not set**
- ✅ Make sure you replaced `YOUR_NGROK_AUTH_TOKEN_HERE` with your actual token
- ✅ Get token from: https://dashboard.ngrok.com/get-started/your-authtoken

---

### Error: "ngrok authentication required"

You need to set your ngrok token:
1. Sign up at https://ngrok.com
2. Get your token
3. Replace `YOUR_NGROK_AUTH_TOKEN_HERE` in the Colab code

---

### Error: "Cannot connect to custom model"

**Check:**
1. Is the Colab cell running? (green checkmark)
2. Can you open the URL in your browser? Try: `https://your-url.ngrok.io/health`
3. Is your Genius AI backend running? Check: http://localhost:8000/health

---

## What the Code Does

1. **Installs dependencies** - Flask, ngrok, etc.
2. **Creates a Flask API** - With `/chat` endpoint
3. **Enables CORS** - So Genius AI can connect
4. **Starts ngrok tunnel** - Makes Colab accessible from internet
5. **Provides public URL** - For Genius AI to connect to

---

## Using Your Own Model

The template includes a simple echo model. To use your own model:

**Option A: Hugging Face Model**

Replace the model loading section with:
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "your-model-name-here"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_response(message):
    inputs = tokenizer(message, return_tensors='pt')
    outputs = model.generate(**inputs, max_new_tokens=512)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
```

Then in the `/chat` endpoint, replace:
```python
response_text = simple_model(message)
```
With:
```python
response_text = generate_response(message)
```

**Option B: Custom Model**

Replace the `simple_model` function with your own inference code.

---

## Three Ways to Use Your Model

Once configured, you have 3 endpoints:

### 1. Groq Only (Default)
```
POST /chat
```
- Fast (1-3 seconds)
- Free
- Llama 3.3 70B with super intelligence

### 2. Your Custom Model
```
POST /custom-chat
```
- Uses only your Colab model
- Good for specialized tasks

### 3. Hybrid (Recommended!)
```
POST /hybrid-chat
```
- Groq does reasoning
- Your model does generation
- Best of both worlds!

---

## Testing

**Test with curl:**
```bash
# Test health
curl http://localhost:8000/custom-model/config

# Test custom chat
curl -X POST http://localhost:8000/custom-chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello from Genius AI!"}'

# Test hybrid
curl -X POST http://localhost:8000/hybrid-chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain quantum computing"}'
```

**Test in browser:**
1. Open http://localhost:3000
2. Ask any question
3. The response will come from your configured model

---

## Important Notes

⚠️ **Keep Colab Running**
- If you stop the Colab cell, the tunnel closes
- You'll need to restart and get a new URL
- Re-run the configuration script with the new URL

⚠️ **Free Tier Limits**
- ngrok free tier: 1 tunnel at a time
- Colab free tier: Limited GPU hours
- Consider upgrading for production use

⚠️ **Security**
- ngrok URLs are public
- Add authentication if handling sensitive data
- Don't commit tokens to git

---

## Next Steps

After successful connection:
- [ ] Test with simple questions
- [ ] Replace echo model with your actual model
- [ ] Try hybrid mode for best results
- [ ] Add model switching UI (coming soon!)

---

## Need Help?

**Check backend logs:**
```bash
# The backend will show any errors
# Look for "Custom Model Error" messages
```

**Check Colab output:**
- Should show "✅ Endpoint test successful!"
- If not, check the error messages

**Still stuck?**
- Make sure backend is running: http://localhost:8000/health
- Make sure frontend is running: http://localhost:3000
- Make sure Colab cell is running (green checkmark)
- Try restarting everything in order: Colab → Backend → Configuration

---

**You're almost there! Follow the 5 steps above and you'll be connected in minutes!** 🚀
