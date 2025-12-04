# 🚀 60-SECOND DEPLOYMENT WITH NGROK

Your backend is already running! Just follow these 3 steps:

---

## Step 1: Extract & Start Ngrok (20 seconds)

```bash
cd C:\Users\Jorams\genius-ai

# Extract ngrok (wait for download to finish first!)
START_NGROK_SETUP.bat

# Start ngrok tunnel
START_NGROK.bat
```

You'll see something like:
```
Forwarding   https://abc123xyz.ngrok-free.app -> http://localhost:8000
```

**COPY that `https://...ngrok-free.app` URL!**

---

## Step 2: Package Extension (20 seconds)

Open a **NEW CMD window** and run:

```bash
PUBLISH_EXTENSION.bat "https://YOUR-NGROK-URL.ngrok-free.app"
```

Replace `YOUR-NGROK-URL` with the URL from Step 1.

Example:
```bash
PUBLISH_EXTENSION.bat "https://abc123xyz.ngrok-free.app"
```

This will:
- Update extension with your ngrok URL
- Compile TypeScript
- Package extension as VSIX

---

## Step 3: Publish to Marketplace (20 seconds)

### A. Get Azure Token (one-time, 2 minutes)

1. Go to: https://dev.azure.com
2. Profile → **Personal Access Tokens** → **+ New Token**
3. Name: `VS Code Publishing`
4. Scopes: **Marketplace** → **Manage** ✓
5. Click **Create** and **COPY THE TOKEN**

### B. Publish

```bash
cd C:\Users\Jorams\genius-ai\vscode-extension

# Login (paste token when prompted)
vsce login pawa-ai

# Publish!
vsce publish
```

---

## 🎉 DONE!

Your extension will be live at:
**`https://marketplace.visualstudio.com/items?itemName=pawa-ai.pawa-ai`**

Anyone can install with:
```bash
code --install-extension pawa-ai.pawa-ai
```

---

## 💡 After Publishing

### Keep Ngrok Running
Leave the ngrok window open! Your extension needs it to work.

### Upgrade to Permanent URL (Later)

When ready for permanent deployment, see [ALTERNATIVE_DEPLOY.md](ALTERNATIVE_DEPLOY.md):
- **Render.com** (750 hrs/month FREE)
- **Fly.io** (3 VMs FREE)
- **Ngrok Static URL** ($8/month)

Then just update extension and publish new version!

---

## 📊 What You Get

✅ **2 MILLION token context** (10x Claude!)
✅ **Published on VS Code Marketplace**
✅ **Global distribution**
✅ **FREE** (ngrok free tier)

**Time to deploy**: 60 seconds
**Cost**: $0!

---

## Troubleshooting

### Ngrok download not finished?
Wait for `ngrok.zip` to appear in `C:\Users\Jorams\genius-ai\`

### Extension compile errors?
```bash
cd vscode-extension
npm install
npm run compile
```

### Can't publish?
Make sure your Azure token has **Marketplace → Manage** scope!

---

**Ready? Run Step 1 now! 🚀**
