# 🚀 FASTEST WAY: Use Ngrok (60 Seconds to Production!)

Since Railway requires payment, here's the **FASTEST** way to get your extension published TODAY:

---

## Why Ngrok?

- ✅ **FREE forever**
- ✅ **No account needed** (basic tier)
- ✅ **60 seconds setup**
- ✅ Works with your local backend
- ✅ Perfect for publishing extension immediately

**Note**: Free tier URL changes when you restart ngrok, but it's perfect for testing and initial publishing!

---

## Step 1: Install Ngrok (30 seconds)

### Option A: Download Executable (Recommended)
1. Go to: https://ngrok.com/download
2. Download Windows version
3. Extract `ngrok.exe` to: `C:\Users\Jorams\genius-ai\`

### Option B: Chocolatey
```powershell
choco install ngrok
```

### Option C: Winget
```powershell
winget install ngrok
```

---

## Step 2: Start Ngrok (10 seconds)

Your backend is already running on port 8000. Just tunnel it:

```bash
cd C:\Users\Jorams\genius-ai

# Start ngrok tunnel
ngrok http 8000
```

You'll see something like:
```
Forwarding   https://abc123xyz.ngrok-free.app -> http://localhost:8000
```

**Copy that `https://abc123xyz.ngrok-free.app` URL!**

---

## Step 3: Update & Publish Extension (20 seconds)

Open a **NEW terminal** and run:

```powershell
cd C:\Users\Jorams\genius-ai

# Replace YOUR_NGROK_URL with the URL from Step 2
powershell -ExecutionPolicy Bypass -File quick-deploy.ps1 -RailwayURL "YOUR_NGROK_URL"
```

Example:
```powershell
powershell -ExecutionPolicy Bypass -File quick-deploy.ps1 -RailwayURL "https://abc123xyz.ngrok-free.app"
```

This will:
1. Update extension with your ngrok URL
2. Recompile & package
3. Help you publish to VS Code Marketplace

---

## 🎉 DONE!

Your extension will be live on VS Code Marketplace in **60 seconds**!

---

## Upgrade to Permanent URL (Optional, Later)

Once your extension is published and working, you can upgrade to a permanent backend:

### Free Permanent Options:
1. **Render.com** (750 hrs/month free) - See [ALTERNATIVE_DEPLOY.md](ALTERNATIVE_DEPLOY.md)
2. **Fly.io** (3 free VMs) - See [ALTERNATIVE_DEPLOY.md](ALTERNATIVE_DEPLOY.md)
3. **Ngrok Static URL** ($8/month) - Run: `ngrok http 8000 --domain=your-static-domain.ngrok-free.app`

Then just update extension and publish new version:
```powershell
powershell -ExecutionPolicy Bypass -File quick-deploy.ps1 -RailwayURL "YOUR_NEW_PERMANENT_URL"
```

---

## Ngrok Pro Tips

### Make URL Stay Longer (Free Tier)
Sign up for free account at https://ngrok.com/signup and get:
- Auth token (prevents URL changes)
- Longer session time

```bash
# Get your auth token from: https://dashboard.ngrok.com/get-started/your-authtoken
ngrok config add-authtoken YOUR_AUTH_TOKEN

# Now your URL will stay the same as long as ngrok is running
ngrok http 8000
```

### Keep Ngrok Running
```bash
# Keep ngrok running in background
start ngrok http 8000
```

---

## Why This Works

Your local backend (running on port 8000) already has:
- ✅ Gemini 2M context working
- ✅ All APIs tested
- ✅ Environment variables set

Ngrok just makes it publicly accessible!

---

## 🚀 LET'S DO IT NOW!

Run these 3 commands in order:

### Terminal 1 (Keep ngrok running):
```bash
cd C:\Users\Jorams\genius-ai
ngrok http 8000
```
**Copy the `https://` URL you see!**

### Terminal 2 (Deploy extension):
```powershell
cd C:\Users\Jorams\genius-ai
powershell -ExecutionPolicy Bypass -File quick-deploy.ps1 -RailwayURL "PASTE_NGROK_URL_HERE"
```

**That's it! You'll have a published extension in 60 seconds! 🎉**

---

## Next Steps After Publishing

1. **Share your extension**:
   - Reddit: r/vscode
   - Twitter: Tag @code
   - Product Hunt

2. **Monitor usage**:
   - VS Code Marketplace: https://marketplace.visualstudio.com/manage

3. **Upgrade backend** (when ready):
   - Deploy to Render/Fly.io for permanent URL
   - Update extension with new URL
   - Publish new version

---

**Ready? Let's get you published TODAY! 🚀**
