# 🔑 Claude API Setup Guide

## Getting Your Claude API Key

### Option 1: Official Anthropic API (Paid)

**Step 1: Create Anthropic Account**
1. Visit: https://console.anthropic.com/
2. Click "Sign Up"
3. Create account with email

**Step 2: Add Payment Method**
- Anthropic requires a payment method
- Credit card or debit card
- **Pricing**: Pay-as-you-go
  - Claude 3.5 Sonnet: $3 per million input tokens, $15 per million output tokens
  - Claude 3 Opus: $15 per million input tokens, $75 per million output tokens
  - Claude 3 Haiku: $0.25 per million input tokens, $1.25 per million output tokens

**Step 3: Get API Key**
1. Go to: https://console.anthropic.com/settings/keys
2. Click "Create Key"
3. Copy your key (starts with `sk-ant-`)

**Step 4: Add to Pawa AI**
Create/edit `backend/.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

---

### Option 2: FREE Alternative - Use Llama Models (Already Working!)

**Good News**: Pawa AI already has FREE models that work great!

**Available FREE Models**:
- **Llama 3.3 70B** - Excellent for coding
- **Llama 3.2 90B Vision** - Great for image analysis
- **Llama 3.1 8B** - Super fast for quick questions

**Setup**: Already done! Using Groq API (FREE, no credit card needed)

**Performance Comparison**:
| Feature | Claude 3.5 Sonnet | Llama 3.3 70B |
|---------|-------------------|---------------|
| Coding | ★★★★★ (Best) | ★★★★☆ (Excellent) |
| Speed | ★★★☆☆ | ★★★★★ (Very Fast) |
| Cost | $$ Paid | 💰 FREE |
| Context | 200K tokens | 8K tokens |

**For most tasks, the FREE Llama models are excellent!**

---

### Option 3: Alternative Paid APIs (Cheaper than Claude Direct)

#### **3A. OpenRouter** (Recommended - Pay-as-you-go, many models)
**Website**: https://openrouter.ai/
**Pricing**: $5 minimum, access to Claude + many other models
**Setup**:
1. Sign up at https://openrouter.ai/
2. Add $5 credit
3. Get API key
4. Can access Claude through OpenRouter API

**Advantages**:
- Lower minimum deposit ($5 vs Anthropic's higher requirements)
- Access to multiple models (Claude, GPT-4, Llama, etc.)
- Pay only for what you use

---

#### **3B. Poe API** (Subscription-based)
**Website**: https://poe.com/
**Pricing**: $20/month for unlimited Claude access
**Setup**:
1. Subscribe to Poe
2. Use their API
3. Access Claude through Poe

---

#### **3C. Perplexity API** (Also has Claude)
**Website**: https://www.perplexity.ai/
**Pricing**: Variable
**Setup**: Similar to OpenRouter

---

### Option 4: Free Trial Alternatives

Unfortunately, **Anthropic does NOT offer free trials** for Claude API at this time.

**But you can try Claude for free**:
- Visit https://claude.ai (web interface)
- Free tier available
- No API access on free tier

---

## 🎯 Recommendation: Use What You Have!

### Why Llama Models are Great (and FREE):

**1. Llama 3.3 70B** (Already working in Pawa AI)
- Excellent for coding
- Very fast responses
- Completely FREE via Groq
- No credit card needed

**2. Smart Model Router** (Already built!)
Pawa AI automatically selects the best FREE model for each task:
- Coding → Llama 3.3 70B
- Images → Llama 3.2 90B Vision
- Quick questions → Llama 3.1 8B

**3. When to Upgrade to Claude**:
Only if you need:
- 200K context window (very long documents)
- Absolute best quality for complex reasoning
- Production-grade reliability

For 95% of coding tasks, **Llama 3.3 70B is excellent!**

---

## 📦 Quick Setup Options

### A. Use FREE Models (Recommended to Start)
**Status**: ✅ Already working!
**Cost**: $0
**Action**: Nothing to do, already set up!

### B. Add Claude API (Optional)
**Cost**: ~$3-5 for testing (pay-as-you-go)
**Action**:
1. Get key from https://console.anthropic.com/
2. Add to `backend/.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key
   ```
3. Restart backend

### C. Use OpenRouter (Budget Option)
**Cost**: $5 minimum
**Benefits**: Access to Claude + GPT-4 + many models
**Action**:
1. Sign up at https://openrouter.ai/
2. Get API key
3. Modify Pawa AI to use OpenRouter endpoint

---

## 🔧 How to Add Any API Key to Pawa AI

### Step 1: Create/Edit `.env` File
```bash
cd backend
nano .env  # or use any text editor
```

### Step 2: Add Your Key
```bash
# Claude (Anthropic)
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Or OpenRouter
OPENROUTER_API_KEY=your-openrouter-key

# Or OpenAI (if you want GPT-4)
OPENAI_API_KEY=sk-your-openai-key
```

### Step 3: Restart Backend
```bash
python super_intelligent_endpoint.py
```

### Step 4: Verify
```bash
curl http://localhost:8000/claude/health
```

Should return:
```json
{
  "status": "healthy",
  "message": "Claude API is configured and working"
}
```

---

## 💡 Smart Spending Tips

If you decide to pay for Claude API:

**1. Start Small**
- Add $5-10 credit first
- Test with small tasks
- Monitor usage

**2. Use Smart Routing**
Pawa AI's smart router can:
- Use FREE models for simple tasks
- Use Claude only for complex tasks
- Save money automatically

**3. Set Usage Limits**
In Anthropic console:
- Set monthly spending limit
- Get alerts at thresholds
- Prevent overspending

**4. Optimize Prompts**
- Shorter prompts = less cost
- Be specific = better results = fewer retries

---

## 📊 Cost Estimation

### Typical Usage Costs:

**Light Usage** (10 requests/day):
- With FREE Llama: $0/month
- With Claude 3.5 Sonnet: ~$2-5/month
- With Claude 3 Opus: ~$10-15/month

**Medium Usage** (50 requests/day):
- With FREE Llama: $0/month
- With Claude 3.5 Sonnet: ~$10-20/month
- With Claude 3 Opus: ~$50-75/month

**Heavy Usage** (200+ requests/day):
- With FREE Llama: $0/month
- With Claude 3.5 Sonnet: ~$50-100/month
- With Claude 3 Opus: ~$200-300/month

**Recommendation**: Start with FREE Llama, upgrade only if needed!

---

## 🚀 What Works Right Now (No API Key Needed)

Your Pawa AI already has:

✅ **Llama 3.3 70B** - Excellent coding model (FREE)
✅ **Llama 3.2 90B Vision** - Image analysis (FREE)
✅ **Llama 3.1 8B** - Fast responses (FREE)
✅ **Smart Model Router** - Auto-selects best FREE model
✅ **Artifacts** - Live code preview
✅ **Thinking Display** - AI reasoning
✅ **Full IDE** - Code editor + preview + terminal
✅ **Project Management** - Organize everything

**You can use Pawa AI fully functional right now without paying anything!**

---

## ❓ FAQ

**Q: Is Claude API worth it?**
A: For most users, NO. The FREE Llama models are excellent for coding. Only upgrade if you need the absolute best for complex reasoning or very long documents.

**Q: Can I try Claude without paying?**
A: Not via API. But you can use claude.ai web interface for free.

**Q: What if I don't have a credit card?**
A: Use the FREE Llama models! They're already working in Pawa AI and are great for coding.

**Q: Can I switch between FREE and paid models?**
A: YES! Pawa AI's smart router lets you choose per request.

**Q: How do I know which model is being used?**
A: Check the backend logs or add a display in the UI.

---

## 🎉 Summary

**Best Option**: Stick with FREE Llama models (already working!)

**If You Want Claude**:
1. Sign up at https://console.anthropic.com/
2. Add payment method
3. Get API key
4. Add to `backend/.env`
5. Restart backend

**Budget Alternative**: OpenRouter ($5 minimum, many models)

**Bottom Line**: You already have excellent AI models working for FREE! 🎊

---

## 📞 Need Help?

If you decide to add Claude API and need help:
1. Get your API key from Anthropic
2. Add it to `backend/.env`
3. Restart backend
4. Test with: `curl http://localhost:8000/claude/health`

**The FREE models in Pawa AI are already production-ready!** 🚀
