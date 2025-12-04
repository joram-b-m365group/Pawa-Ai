# 🚀 COMPLETE GITHUB SETUP - COPY & PASTE

Everything is ready! Just follow these steps:

---

## Step 1: Run the Setup Script (30 seconds)

Double-click: **`PUSH_TO_GITHUB.bat`**

This will:
- Configure git with your info
- Add all files
- Create initial commit

---

## Step 2: Create GitHub Repository (2 minutes)

1. Go to: **https://github.com/new**
2. Fill in:
   - **Repository name**: `pawa-ai`
   - **Description**: `AI coding assistant with 2M token context - 100% FREE`
   - **Public** or **Private** (your choice!)
   - **DON'T** check "Initialize with README"
3. Click **Create repository**

---

## Step 3: Push to GitHub (1 minute)

GitHub will show you commands. Copy them and run in terminal:

```bash
cd C:\Users\Jorams\genius-ai

# Replace YOUR_USERNAME with your actual GitHub username!
git remote add origin https://github.com/YOUR_USERNAME/pawa-ai.git
git branch -M main
git push -u origin main
```

**Done!** Your code is now on GitHub! 🎉

---

## Step 4: Deploy Backend to Render (5 minutes)

1. Go to: **https://render.com**
2. Click **Sign Up** → Sign in with GitHub
3. Authorize Render to access your repos
4. Click **New +** → **Web Service**
5. Select your `pawa-ai` repository
6. Render will show settings. Click **Advanced** and configure:

   - **Name**: `pawa-ai-backend`
   - **Region**: Oregon (or closest to you)
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn super_intelligent_endpoint:app --host 0.0.0.0 --port $PORT`

7. Click **Environment** and add:
   ```
   GOOGLE_API_KEY=AIzaSyBzT0i4WjPexzHG-QR5RIARNLX0ZOjK8uM
   GROQ_API_KEY=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
   PORT=8000
   ```

8. Click **Create Web Service**

Render will deploy! You'll get a URL like:
**`https://pawa-ai-backend.onrender.com`**

**COPY THIS URL!** You'll need it next.

---

## Step 5: Update Extension with Production URL (2 minutes)

```bash
cd C:\Users\Jorams\genius-ai\vscode-extension

# Replace YOUR_RENDER_URL with the URL from Step 4!
powershell -Command "(Get-Content package.json) -replace 'http://localhost:8000', 'YOUR_RENDER_URL' | Set-Content package.json"

# Example:
# powershell -Command "(Get-Content package.json) -replace 'http://localhost:8000', 'https://pawa-ai-backend.onrender.com' | Set-Content package.json"

# Commit the change
cd ..
git add vscode-extension/package.json
git commit -m "Update extension with production backend URL"
git push
```

---

## Step 6: Publish Extension to VS Code Marketplace (10 minutes)

### A. Get Azure DevOps Token (First Time - 5 min)

1. Go to: **https://dev.azure.com**
2. Sign in with Microsoft account
3. Click your profile picture (top right) → **Personal Access Tokens**
4. Click **+ New Token**
5. Configure:
   - **Name**: `VS Code Publishing`
   - **Organization**: `All accessible organizations`
   - **Expiration**: `90 days` (or longer)
   - **Scopes**: Click **Show all scopes**
     - Scroll to **Marketplace**
     - Check **Manage** ✅
6. Click **Create**
7. **COPY THE TOKEN** - You won't see it again!

### B. Publish (5 min)

```bash
cd C:\Users\Jorams\genius-ai\vscode-extension

# Compile
npm run compile

# Package
vsce package --allow-missing-repository

# Login (paste your PAT when prompted)
vsce login pawa-ai

# Publish!
vsce publish
```

**Done!** Your extension will be live at:
**`https://marketplace.visualstudio.com/items?itemName=pawa-ai.pawa-ai`**

Anyone can install with:
```bash
code --install-extension pawa-ai.pawa-ai
```

---

## Step 7: Enable GitHub Actions (Optional - 2 minutes)

### For Auto-Deployment on Every Push!

1. Go to your GitHub repo: `https://github.com/YOUR_USERNAME/pawa-ai`
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these secrets:

**Secret 1: VSCE_PAT**
- Name: `VSCE_PAT`
- Value: Your Azure DevOps PAT (from Step 6A)

**Secret 2: BACKEND_URL**
- Name: `BACKEND_URL`
- Value: Your Render URL (from Step 4)

**Secret 3: RENDER_API_KEY** (Optional - for backend auto-deploy)
- Name: `RENDER_API_KEY`
- Value: Get from https://dashboard.render.com/u/YOUR_USERNAME/account/api-keys

**Secret 4: RENDER_SERVICE_ID** (Optional)
- Name: `RENDER_SERVICE_ID`
- Value: Found in your Render service URL

Now, every time you push to GitHub:
- Backend auto-deploys to Render ✅
- Extension auto-publishes on release ✅
- Frontend auto-deploys to GitHub Pages ✅

---

## Step 8: Deploy Frontend to GitHub Pages (Optional - 3 minutes)

1. Go to your repo: `https://github.com/YOUR_USERNAME/pawa-ai/settings/pages`
2. Under **Source**, select **GitHub Actions**
3. Save

Now push any change to trigger deployment:
```bash
git commit --allow-empty -m "Deploy frontend to GitHub Pages"
git push
```

Your frontend will be live at:
**`https://YOUR_USERNAME.github.io/pawa-ai/`**

---

## 🎉 YOU'RE DONE!

### What You Now Have:

✅ **Code on GitHub** - Version controlled, backed up
✅ **Backend on Render** - https://pawa-ai-backend.onrender.com
✅ **Extension on Marketplace** - https://marketplace.visualstudio.com/items?itemName=pawa-ai.pawa-ai
✅ **Auto-Deployment** - Push to GitHub = auto-deploy!
✅ **2M Token Context** - FREE Gemini API
✅ **Professional SaaS** - $0/month cost!

---

## 📊 Your Stats

Check your deployment status:
- **GitHub**: https://github.com/YOUR_USERNAME/pawa-ai
- **Render Dashboard**: https://dashboard.render.com
- **VS Code Marketplace**: https://marketplace.visualstudio.com/manage/publishers/pawa-ai
- **GitHub Pages**: https://YOUR_USERNAME.github.io/pawa-ai/

---

## 🚀 Daily Workflow

After setup, your workflow is super simple:

### Make Changes
```bash
# Edit code
git add .
git commit -m "Add new feature"
git push
```

**That's it!** GitHub Actions will:
- Deploy backend to Render
- Publish new extension version (on release)
- Deploy frontend to GitHub Pages

---

## 💡 Tips

### Create a Release (Auto-publish extension)
```bash
git tag v2.0.1
git push origin v2.0.1
```
Then create release on GitHub - extension auto-publishes!

### Update Backend
Just push changes to `backend/` folder - auto-deploys!

### Update Frontend
Push changes to `frontend/` folder - auto-deploys to GitHub Pages!

---

## 🎯 Next Steps

1. **Share your extension!**
   - Reddit: r/vscode, r/programming
   - Twitter/X: Tag @code
   - Product Hunt: https://producthunt.com

2. **Monitor usage**
   - Extension installs on Marketplace
   - Backend performance on Render
   - User feedback via GitHub Issues

3. **Keep improving**
   - Add features
   - Fix bugs
   - Update models
   - Improve UI

---

**Congratulations! You've deployed a production SaaS with 2M token context! 🎊**

**Total time**: ~25 minutes
**Total cost**: $0/month
**Potential users**: Millions of VS Code developers worldwide!

---

For more details, see [GITHUB_DEPLOYMENT.md](GITHUB_DEPLOYMENT.md)
