# 🚀 GITHUB DEPLOYMENT GUIDE

Deploy everything using GitHub! Free, automated, and professional.

---

## 🎯 What You'll Get

✅ **Backend**: Auto-deployed to Render via GitHub Actions
✅ **Frontend**: Hosted on GitHub Pages (FREE, unlimited bandwidth!)
✅ **Extension**: Auto-published to VS Code Marketplace on release
✅ **CI/CD**: Automatic deployments on every push
✅ **Version Control**: Full git history

**Cost**: $0/month!

---

## Step 1: Create GitHub Repository (2 minutes)

### A. Initialize Git (if not done)

```bash
cd C:\Users\Jorams\genius-ai

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Pawa AI with 2M token Gemini"
```

### B. Create GitHub Repo

1. Go to: https://github.com/new
2. **Repository name**: `pawa-ai` (or any name)
3. **Public** or **Private** (your choice)
4. **DON'T** initialize with README, .gitignore, or license
5. Click **Create repository**

### C. Push to GitHub

Copy the commands from GitHub and run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/pawa-ai.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy Backend to Render (5 minutes)

### A. Create Render Account

1. Go to: https://render.com
2. Sign up with GitHub (easiest!)
3. Authorize Render to access your repos

### B. Deploy from GitHub

1. Click **New +** → **Web Service**
2. Select your `pawa-ai` repository
3. Configure:
   - **Name**: `pawa-ai-backend`
   - **Region**: Oregon (or closest)
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn super_intelligent_endpoint:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables**:
   ```
   GOOGLE_API_KEY=AIzaSyBzT0i4WjPexzHG-QR5RIARNLX0ZOjK8uM
   GROQ_API_KEY=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
   PORT=8000
   ```

5. Click **Create Web Service**

Render will:
- Auto-detect your `render.yaml` config (already created!)
- Deploy your backend
- Give you a URL like: `https://pawa-ai-backend.onrender.com`

**Copy this URL - you'll need it!**

### C. Enable Auto-Deploy (Optional)

In Render dashboard:
1. Go to your service settings
2. Enable **Auto-Deploy** → Every push to `main` auto-deploys!

---

## Step 3: Update Extension with Production URL (2 minutes)

```bash
cd C:\Users\Jorams\genius-ai\vscode-extension

# Update package.json with your Render URL
powershell -Command "(Get-Content package.json) -replace 'http://localhost:8000', 'https://pawa-ai-backend.onrender.com' | Set-Content package.json"

# Commit the change
git add package.json
git commit -m "Update extension with production backend URL"
git push
```

---

## Step 4: Set Up GitHub Secrets (3 minutes)

For auto-publishing extension:

1. Go to: `https://github.com/YOUR_USERNAME/pawa-ai/settings/secrets/actions`
2. Click **New repository secret**
3. Add these secrets:

### Secret 1: VSCE_PAT
- **Name**: `VSCE_PAT`
- **Value**: Your Azure DevOps Personal Access Token
  - Get from: https://dev.azure.com
  - Create PAT with **Marketplace → Manage** scope

### Secret 2: BACKEND_URL
- **Name**: `BACKEND_URL`
- **Value**: `https://pawa-ai-backend.onrender.com` (your Render URL)

### Secret 3: RENDER_API_KEY (Optional - for backend auto-deploy)
- **Name**: `RENDER_API_KEY`
- **Value**: Get from https://dashboard.render.com/account/api-keys

### Secret 4: RENDER_SERVICE_ID (Optional)
- **Name**: `RENDER_SERVICE_ID`
- **Value**: Found in your Render service URL

---

## Step 5: Deploy Frontend to GitHub Pages (2 minutes)

### A. Enable GitHub Pages

1. Go to: `https://github.com/YOUR_USERNAME/pawa-ai/settings/pages`
2. **Source**: Deploy from a branch → **GitHub Actions**
3. Save

### B. Trigger Deployment

```bash
cd C:\Users\Jorams\genius-ai

# Make any change to frontend (or just trigger workflow)
git commit --allow-empty -m "Deploy frontend to GitHub Pages"
git push
```

GitHub Actions will:
- Build your React frontend
- Deploy to GitHub Pages
- Your frontend will be live at: `https://YOUR_USERNAME.github.io/pawa-ai/`

---

## Step 6: Publish Extension (2 minutes)

### Option A: Manual Publish (First Time)

```bash
cd vscode-extension

# Compile
npm run compile

# Package
vsce package --allow-missing-repository

# Publish
vsce login pawa-ai
vsce publish
```

### Option B: Auto-Publish via GitHub (After first time)

1. Create a new release on GitHub:
   ```bash
   git tag v2.0.0
   git push origin v2.0.0
   ```

2. Go to: `https://github.com/YOUR_USERNAME/pawa-ai/releases/new`
3. Select tag `v2.0.0`
4. Title: `v2.0.0 - 2M Token Context Release`
5. Click **Publish release**

GitHub Actions will automatically:
- Compile extension
- Package VSIX
- Publish to VS Code Marketplace!

---

## 🎉 DONE! Here's What You Have:

### Backend
- **URL**: `https://pawa-ai-backend.onrender.com`
- **Auto-deploys** on every push to `backend/`
- **2M token Gemini** context
- **Free tier**: 750 hours/month

### Frontend
- **URL**: `https://YOUR_USERNAME.github.io/pawa-ai/`
- **Auto-deploys** on every push to `frontend/`
- **GitHub Pages**: Unlimited bandwidth!

### Extension
- **Marketplace**: `https://marketplace.visualstudio.com/items?itemName=pawa-ai.pawa-ai`
- **Auto-publishes** on GitHub release
- **Users install**: `code --install-extension pawa-ai.pawa-ai`

---

## 📊 Automated Workflows Created

I've created 3 GitHub Actions workflows for you:

1. **[.github/workflows/deploy-backend.yml](.github/workflows/deploy-backend.yml)**
   - Triggers: Push to `backend/`
   - Deploys backend to Render

2. **[.github/workflows/publish-extension.yml](.github/workflows/publish-extension.yml)**
   - Triggers: GitHub release created
   - Publishes extension to VS Code Marketplace

3. **[.github/workflows/deploy-frontend.yml](.github/workflows/deploy-frontend.yml)**
   - Triggers: Push to `frontend/`
   - Deploys frontend to GitHub Pages

---

## 🔄 Daily Workflow

After initial setup, your workflow is super simple:

### Update Backend
```bash
# Make changes to backend
git add backend/
git commit -m "Add new feature"
git push
# ✅ Auto-deployed to Render!
```

### Update Extension
```bash
# Make changes to extension
git add vscode-extension/
git commit -m "Fix bug"
git tag v2.0.1
git push origin v2.0.1
# Create release on GitHub
# ✅ Auto-published to marketplace!
```

### Update Frontend
```bash
# Make changes to frontend
git add frontend/
git commit -m "UI improvements"
git push
# ✅ Auto-deployed to GitHub Pages!
```

---

## 💰 Total Cost

- GitHub: **FREE** (public or private repos)
- Render: **FREE** (750 hours/month)
- GitHub Pages: **FREE** (unlimited)
- VS Code Marketplace: **FREE**
- GitHub Actions: **FREE** (2000 minutes/month)

**Total: $0/month!** 🎉

---

## 🚀 Quick Start Commands

If you already have git initialized:

```bash
# 1. Create GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/pawa-ai.git
git push -u origin main

# 2. Deploy backend on Render (use web UI)

# 3. Update extension URL
cd vscode-extension
powershell -Command "(Get-Content package.json) -replace 'http://localhost:8000', 'https://pawa-ai-backend.onrender.com' | Set-Content package.json"
git add package.json
git commit -m "Update production URL"
git push

# 4. Publish extension
npm run compile
vsce package --allow-missing-repository
vsce publish

# 5. Enable GitHub Pages in repo settings
```

---

## 🔧 Troubleshooting

### GitHub Actions failing?
- Check secrets are set correctly
- Verify VSCE_PAT has Marketplace → Manage scope
- Check workflow logs in Actions tab

### Backend deploy failing?
- Verify `render.yaml` exists in backend/
- Check environment variables in Render dashboard
- View logs in Render dashboard

### Extension publish failing?
- Make sure you ran `vsce login pawa-ai` first time manually
- Verify VSCE_PAT secret is correct
- Check you have publisher account at https://marketplace.visualstudio.com/manage

---

## 📚 Learn More

- **GitHub Actions**: https://docs.github.com/en/actions
- **Render**: https://render.com/docs
- **GitHub Pages**: https://pages.github.com
- **VS Code Publishing**: https://code.visualstudio.com/api/working-with-extensions/publishing-extension

---

**Ready to deploy? Start with Step 1! 🚀**
