# 🚀 Gemini Quick Start - 2M Token Context FREE!

## Get 200K+ Context in 5 Minutes (No Payment!)

---

## ✅ Step 1: Get FREE Google API Key

**Visit**: https://aistudio.google.com/

1. Click "Get API key" (top right)
2. Sign in with your Google account
3. Click "Create API key"
4. Copy your key (starts with `AIza...`)

**Takes**: 2 minutes
**Cost**: $0 (FREE forever!)
**No credit card required!**

---

## ✅ Step 2: Add to Pawa AI

**Open**: `backend/.env`

**Add this line**:
```bash
GOOGLE_API_KEY=AIza...your-key-here
```

**Example**:
```bash
# Gemini API (FREE 2M token context!)
GOOGLE_API_KEY=AIzaSyC1234567890abcdefghijklmnopqrstuv
```

---

## ✅ Step 3: Install Google SDK

```bash
cd backend
pip install google-generativeai
```

---

## ✅ Step 4: Restart Backend

Backend will automatically detect and enable Gemini!

You should see:
```
✅ Gemini API routes registered! (2M token context - FREE!)
```

---

## 🎯 That's It!

Your Pawa AI now has:
- ✅ **2 MILLION token context** (vs Claude's 200K)
- ✅ **100% FREE** (no credit card)
- ✅ **Automatic switching** (Llama for small, Gemini for large)

---

## 🚀 How It Works

### Automatic Smart Routing:

**Small Context** (< 8K tokens):
- Uses Llama 3.3 70B (fast, FREE)

**Large Context** (> 8K tokens):
- Automatically switches to Gemini 1.5 Pro
- 2M token context
- Still FREE!

### You Don't Need to Do Anything:
The smart router automatically selects the best model!

---

## 📊 What You Can Do Now

### 1. **Analyze Entire Codebases**
```
POST /gemini/analyze-large-codebase
{
  "files": {
    "app.py": "...",
    "models.py": "...",
    "views.py": "..."
  },
  "question": "How does authentication work?"
}
```

### 2. **Process Long Documents**
```
POST /gemini/analyze-long-document
{
  "document": "...entire book...",
  "question": "Summarize main points"
}
```

### 3. **Code Review Entire Project**
```
POST /gemini/code-review-full-project
{
  "project_files": {
    "file1.py": "...",
    "file2.py": "..."
  }
}
```

### 4. **Regular Chat with Massive Context**
```
POST /gemini/chat
{
  "message": "Explain this codebase",
  "conversation_history": []
}
```

---

## 💡 Usage Tips

**FREE Tier Limits**:
- 15 requests per minute
- 1500 requests per day
- 4M tokens per minute

**For Personal Use**: More than enough!

**To Check Status**:
```bash
curl http://localhost:8000/gemini/health
```

**To See Models**:
```bash
curl http://localhost:8000/gemini/models
```

---

## 🎉 Summary

**Before**: 8K token context with Llama
**After**: 2 MILLION token context with Gemini
**Cost**: $0 (FREE!)
**Setup Time**: 5 minutes
**Better than**: Claude (200K for $$)

**You now have the largest context window available, for FREE!** 🚀

---

## 📞 Need Help?

**Test it works**:
```bash
curl http://localhost:8000/gemini/health
```

Should return:
```json
{
  "status": "healthy",
  "message": "Gemini API is working! 2M token context available!"
}
```

**Everything is integrated and ready to go!** 🎊
