# 🚀 ACTIVATE GEMINI - 2 Minutes!

## ✅ API Key Added!

Your Google API key has been added to `backend/.env`:
```
GOOGLE_API_KEY=AIzaSyBzT0i4WjPexzHG-QR5RIARNLX0ZOjK8uM
```

---

## 📦 Next: Install & Restart

### Option 1: Automatic (Recommended)

**Windows**:
1. Open Command Prompt or PowerShell
2. Navigate to backend folder:
   ```cmd
   cd C:\Users\Jorams\genius-ai\backend
   ```
3. Run the activation script:
   ```cmd
   activate_gemini.bat
   ```

This will:
- Install google-generativeai package
- Restart backend with Gemini enabled
- Show success message

---

### Option 2: Manual Steps

If the automatic script doesn't work:

**Step 1**: Install Package
```cmd
cd C:\Users\Jorams\genius-ai\backend
pip install google-generativeai
```

**Step 2**: Stop Current Backend
- Find the terminal where backend is running
- Press `Ctrl+C` to stop it

**Step 3**: Restart Backend
```cmd
python super_intelligent_endpoint.py
```

**Step 4**: Look for Success Messages
You should see:
```
✅ Gemini API routes registered! (2M token context - FREE!)
✅ Simple Terminal Executor registered!
```

---

## 🧪 Test It Works

After backend restarts, test in a new terminal:

**Test 1: Gemini Health Check**
```cmd
curl http://localhost:8000/gemini/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "Gemini API is working! 2M token context available!",
  "test_response": "Hello! How can I help you today?"
}
```

**Test 2: Terminal Executor**
```cmd
curl http://localhost:8000/terminal/health
```

Expected response:
```json
{
  "status": "healthy",
  "test_output": "hello"
}
```

**Test 3: List Available Models**
```cmd
curl http://localhost:8000/gemini/models
```

You should see Gemini 1.5 Pro with 2,000,000 token context!

---

## 🎉 What You'll Have

Once activated:

### Automatic Smart Routing:
- **Small tasks** (< 8K tokens) → Llama 3.3 70B (fast, FREE)
- **Large tasks** (> 8K tokens) → **Gemini 1.5 Pro** (2M tokens, FREE!)
- **Image tasks** → Llama 3.2 90B Vision (FREE)

### New Capabilities:
- ✅ Analyze entire codebases (50+ files at once)
- ✅ Process 1500-page documents
- ✅ Complete project reviews
- ✅ Run code with one click
- ✅ Live preview in editor
- ✅ Integrated terminal

---

## 📊 Before vs After

### Before Gemini:
- 8K token context
- Can analyze ~10 files
- Limited document size

### After Gemini (2 Minutes):
- **2 MILLION token context** (250x more!)
- Can analyze **entire codebases**
- Process **book-length documents**
- Still **100% FREE**

---

## 🔍 Troubleshooting

### Issue: "pip install" fails
**Fix**: Make sure you're in the correct Python environment
```cmd
where python
pip --version
```

### Issue: "Module not found" after install
**Fix**: Restart the backend server (stop with Ctrl+C, then run again)

### Issue: Backend won't start
**Fix**: Check the terminal output for errors. Common issues:
- Port 8000 already in use → Kill other process using port 8000
- Missing dependencies → Run: `pip install -r requirements.txt`

### Issue: Gemini endpoint returns "Not Found"
**Fix**: Backend needs restart to load new routes

---

## 📞 Quick Reference

**Backend Location**: `C:\Users\Jorams\genius-ai\backend`

**Start Backend**:
```cmd
cd C:\Users\Jorams\genius-ai\backend
python super_intelligent_endpoint.py
```

**Install Package**:
```cmd
pip install google-generativeai
```

**Test Gemini**:
```cmd
curl http://localhost:8000/gemini/health
```

---

## 🎯 Summary

**Status**: API key added ✅
**Next**: Install package + restart (2 minutes)
**Result**: 2M token context, 100% FREE!

**Run**: `cd backend && activate_gemini.bat`

---

**You're 2 minutes away from 2 MILLION token context!** 🚀
