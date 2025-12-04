# How to Start Genius AI (No Terminal Needed!)

## 🚀 Quick Start - 3 Easy Ways

### Option 1: Silent Mode (Recommended - No Terminal Windows!)

**Just double-click:**
```
START_GENIUS_AI_SILENT.vbs
```

✅ Runs completely in the background
✅ No terminal windows
✅ Auto-opens browser
✅ Clean and simple

**What happens:**
1. Cleans up old processes
2. Starts backend (hidden)
3. Starts frontend (hidden)
4. Opens http://localhost:3000
5. Shows success message

---

### Option 2: Regular Mode (With Minimized Terminal Windows)

**Just double-click:**
```
START_GENIUS_AI.bat
```

✅ Shows minimized terminal windows
✅ Can see logs if needed
✅ Auto-opens browser
✅ Shows startup progress

**What happens:**
1. Cleans up old processes
2. Starts backend in minimized window
3. Starts frontend in minimized window
4. Opens http://localhost:3000
5. Ready to use!

---

### Option 3: Manual Start (If you want full control)

**Open 2 terminals:**

**Terminal 1 - Backend:**
```bash
cd backend
python working_vision_endpoint.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Then open:** http://localhost:3000

---

## 🛑 How to Stop

### Easy Way:
**Just double-click:**
```
STOP_GENIUS_AI.bat
```

This will cleanly stop both backend and frontend.

### Manual Way:
- Close the terminal windows
- OR press `Ctrl+C` in each terminal

---

## 📁 Files Explained

| File | Purpose |
|------|---------|
| **START_GENIUS_AI_SILENT.vbs** | 🌟 Best option - runs hidden, no terminals |
| **START_GENIUS_AI.bat** | Runs with minimized terminals |
| **STOP_GENIUS_AI.bat** | Stops all Genius AI processes |
| **HOW_TO_START.md** | This file - instructions |

---

## 🎯 What Runs When You Start

### Backend (Port 8000)
- Python FastAPI server
- Groq AI integration
- Image analysis
- File upload handling
- Rate limiting

### Frontend (Port 3000)
- React + TypeScript
- Vite dev server
- Hot module reload
- Beautiful UI

---

## 💡 Pro Tips

### Create Desktop Shortcut:

1. **Right-click** `START_GENIUS_AI_SILENT.vbs`
2. Select **"Create shortcut"**
3. Drag shortcut to Desktop
4. Rename to "Genius AI"
5. **Done!** Now double-click desktop icon to start

### Pin to Taskbar:

1. Create a batch file that runs the VBS:
   ```batch
   @echo off
   wscript "C:\Users\Jorams\genius-ai\START_GENIUS_AI_SILENT.vbs"
   ```
2. Save as `genius_ai_launcher.bat`
3. Right-click → Pin to Taskbar

### Auto-Start on Windows Startup:

1. Press `Win + R`
2. Type: `shell:startup`
3. Copy `START_GENIUS_AI_SILENT.vbs` into that folder
4. Genius AI will start automatically when you log in!

---

## ❓ Troubleshooting

### "Port already in use" error:
**Solution:** Run `STOP_GENIUS_AI.bat` first, then start again

### Backend won't start:
**Solution:**
```bash
cd backend
C:\Users\Jorams\anaconda3\python.exe working_vision_endpoint.py
```
Check for error messages

### Frontend won't start:
**Solution:**
```bash
cd frontend
npm install
npm run dev
```

### Browser doesn't open:
**Solution:** Manually open http://localhost:3000

### Nothing works:
**Solution:**
1. Run `STOP_GENIUS_AI.bat`
2. Wait 10 seconds
3. Run `START_GENIUS_AI_SILENT.vbs` again

---

## 🌐 URLs

- **Frontend (Main App):** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **API Health Check:** http://localhost:8000/health

---

## ✨ Features Available

Once started, you can:

✅ Chat with 70B AI
✅ Upload and analyze images
✅ Record voice messages
✅ Get code with syntax highlighting
✅ Export/share conversations
✅ Switch between AI models
✅ Process documents
✅ Use stunning landing page

---

## 🎉 Recommended Workflow

### Daily Use:
1. **Double-click** `START_GENIUS_AI_SILENT.vbs`
2. Wait for browser to open
3. Start using Genius AI!
4. When done, close browser
5. **Double-click** `STOP_GENIUS_AI.bat`

### For Development:
1. Use `START_GENIUS_AI.bat` (so you can see logs)
2. Keep terminal windows open
3. Watch for errors or debugging info
4. Press `Ctrl+C` in terminals when done

---

## 📊 System Check

Before starting, make sure you have:

✅ Python 3.10+ installed
✅ Node.js 16+ installed
✅ npm packages installed (`npm install` in frontend folder)
✅ Python packages installed (`pip install -r requirements.txt` in backend folder)

---

## 🚀 Summary

**Easiest Way to Start:**
```
Double-click: START_GENIUS_AI_SILENT.vbs
```

**Easiest Way to Stop:**
```
Double-click: STOP_GENIUS_AI.bat
```

**That's it!** No terminal needed! 🎉

---

## 💻 What's Running

When Genius AI is active:

```
┌─────────────────────────────────────┐
│  Genius AI System                   │
├─────────────────────────────────────┤
│                                     │
│  Backend (Port 8000)                │
│  ├── FastAPI Server                 │
│  ├── Groq AI Integration            │
│  ├── Llama 3.3 70B                  │
│  └── Image Analysis                 │
│                                     │
│  Frontend (Port 3000)               │
│  ├── React App                      │
│  ├── Landing Page                   │
│  ├── Chat Interface                 │
│  └── File Upload UI                 │
│                                     │
│  Browser: http://localhost:3000     │
│                                     │
└─────────────────────────────────────┘
```

**Enjoy your AI assistant!** 🧠✨
