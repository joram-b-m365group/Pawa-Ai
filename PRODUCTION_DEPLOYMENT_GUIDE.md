# Pawa AI - Production Deployment Guide

Complete guide to deploy Pawa AI to production and publish to VS Code Marketplace.

---

## Table of Contents

1. [Extension Preparation](#1-extension-preparation)
2. [Backend Deployment](#2-backend-deployment)
3. [VS Code Marketplace Publishing](#3-vs-code-marketplace-publishing)
4. [Frontend Deployment](#4-frontend-deployment)
5. [Post-Deployment](#5-post-deployment)

---

## 1. Extension Preparation

### 1.1 Update Extension Files

**Status**: ✅ DONE
- Added Gemini 2M context support to [vscode-extension/src/ai/PawaAI.ts](vscode-extension/src/ai/PawaAI.ts:118)
- Added Gemini settings to [vscode-extension/package.json](vscode-extension/package.json:178-192)
- Updated version to 2.0.0
- Enhanced description for marketplace

### 1.2 Create Professional Icon

**TODO**: Create a 128x128px PNG icon

```bash
cd vscode-extension/media
# Place your icon.png here (128x128, professional design)
```

**Recommended**:
- Use Figma/Canva to design
- Colors: Blue/Purple gradient
- Include "PA" or lightning bolt symbol
- Export as `icon.png` (128x128)

### 1.3 Update README for Marketplace

The README should include:
- Screenshots of the extension in action
- Feature highlights with images
- Installation instructions
- Configuration guide
- Usage examples

### 1.4 Build Extension

```bash
cd vscode-extension

# Install dependencies (if not done)
npm install

# Compile TypeScript
npm run compile

# Install vsce (VS Code publishing tool)
npm install -g @vscode/vsce

# Package extension
vsce package
```

This creates `pawa-ai-2.0.0.vsix`

---

## 2. Backend Deployment

### Option A: Railway (Recommended)

**Why Railway?**
- Free tier: 500 hours/month
- Easy Python deployment
- Auto HTTPS
- Environment variables
- Zero config

**Steps**:

1. **Create Railway Account**
   - Visit [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create New Project**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli

   # Login
   railway login

   # Initialize
   cd backend
   railway init
   ```

3. **Add Configuration Files**

   Create `railway.json`:
   ```json
   {
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "python super_intelligent_endpoint.py",
       "restartPolicyType": "ON_FAILURE",
       "restartPolicyMaxRetries": 10
     }
   }
   ```

   Create `requirements.txt` (already exists):
   ```
   fastapi>=0.104.0
   uvicorn>=0.24.0
   pydantic>=2.5.0
   groq>=0.4.1
   google-generativeai>=0.8.3
   python-dotenv>=1.0.0
   ```

4. **Set Environment Variables**
   ```bash
   railway variables set GOOGLE_API_KEY=AIzaSyBzT0i4WjPexzHG-QR5RIARNLX0ZOjK8uM
   railway variables set GROQ_API_KEY=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
   railway variables set PORT=8000
   railway variables set API_HOST=0.0.0.0
   ```

5. **Deploy**
   ```bash
   railway up
   ```

6. **Get Public URL**
   ```bash
   railway domain
   ```

   Your backend will be at: `https://your-app.up.railway.app`

### Option B: Render

**Steps**:

1. Visit [render.com](https://render.com)
2. Create New Web Service
3. Connect GitHub repo
4. Configure:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python super_intelligent_endpoint.py`
5. Add environment variables (same as Railway)
6. Deploy

### Option C: Heroku

**Steps**:

1. Install Heroku CLI
   ```bash
   npm install -g heroku
   ```

2. Login and create app
   ```bash
   heroku login
   cd backend
   heroku create pawa-ai-backend
   ```

3. Create `Procfile`:
   ```
   web: python super_intelligent_endpoint.py
   ```

4. Set config vars
   ```bash
   heroku config:set GOOGLE_API_KEY=AIzaSyBzT0i4WjPexzHG-QR5RIARNLX0ZOjK8uM
   heroku config:set GROQ_API_KEY=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
   ```

5. Deploy
   ```bash
   git push heroku main
   ```

### Update Extension with Production URL

After deploying, update the default API URL in [vscode-extension/package.json](vscode-extension/package.json:146):

```json
"pawa-ai.apiUrl": {
  "type": "string",
  "default": "https://your-app.up.railway.app",
  "description": "Pawa AI backend API URL"
}
```

Then rebuild: `npm run compile && vsce package`

---

## 3. VS Code Marketplace Publishing

### 3.1 Create Publisher Account

1. **Get Azure DevOps Account**
   - Visit [dev.azure.com](https://dev.azure.com)
   - Sign in with Microsoft account
   - Create organization (if needed)

2. **Create Personal Access Token (PAT)**
   - Go to User Settings → Personal Access Tokens
   - Click "New Token"
   - Name: "VS Code Publishing"
   - Organization: All accessible organizations
   - Scopes: **Marketplace** → **Manage**
   - Expiration: 1 year
   - Copy token (you won't see it again!)

3. **Create Publisher**
   ```bash
   vsce create-publisher pawa-ai
   ```

   Or visit [marketplace.visualstudio.com/manage](https://marketplace.visualstudio.com/manage)

### 3.2 Login to vsce

```bash
vsce login pawa-ai
# Paste your PAT when prompted
```

### 3.3 Publish Extension

```bash
cd vscode-extension

# Final build
npm run compile

# Publish
vsce publish
```

This will:
- Build the extension
- Upload to marketplace
- Make it available globally

### 3.4 Update Extension Listing

Visit [marketplace.visualstudio.com/manage](https://marketplace.visualstudio.com/manage) and:

1. Add screenshots (4-6 images showing features)
2. Add detailed description
3. Add tags: `ai`, `code-generation`, `productivity`, `assistant`
4. Set pricing: FREE
5. Add Q&A section

---

## 4. Frontend Deployment

### Option A: Vercel (Recommended for React)

```bash
cd frontend

# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Add environment variable
vercel env add REACT_APP_API_URL
# Enter: https://your-backend.up.railway.app

# Deploy to production
vercel --prod
```

### Option B: Netlify

```bash
cd frontend

# Install Netlify CLI
npm install -g netlify-cli

# Build
npm run build

# Deploy
netlify deploy

# Deploy to production
netlify deploy --prod
```

### Update Frontend API URL

Edit [frontend/.env](frontend/.env):
```
REACT_APP_API_URL=https://your-backend.up.railway.app
```

---

## 5. Post-Deployment

### 5.1 Test Everything

**Test Backend**:
```bash
curl https://your-backend.up.railway.app/health
curl https://your-backend.up.railway.app/gemini/health
```

**Test Extension**:
1. Install from marketplace: `ext install pawa-ai.pawa-ai`
2. Configure backend URL in settings
3. Test chat, code generation, refactoring
4. Enable Gemini and test 2M context

**Test Frontend**:
1. Visit your Vercel/Netlify URL
2. Test chat interface
3. Test code editor with run/preview
4. Test terminal execution

### 5.2 Monitor Usage

**Railway**:
- Dashboard shows usage, logs, metrics
- Set up alerts for errors

**VS Code Marketplace**:
- View install stats at [marketplace.visualstudio.com/manage](https://marketplace.visualstudio.com/manage)
- Monitor ratings and reviews

### 5.3 Update Documentation

Create these docs:
1. **User Guide**: How to install and use
2. **API Docs**: Backend API reference
3. **Contributing Guide**: How to contribute
4. **Changelog**: Version history

### 5.4 Set Up CI/CD (Optional)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish Extension

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'

      - name: Install dependencies
        run: |
          cd vscode-extension
          npm install

      - name: Publish
        run: |
          cd vscode-extension
          npx vsce publish -p ${{ secrets.VSCE_PAT }}
```

---

## Quick Checklist

- [ ] Extension code updated with Gemini support
- [ ] Icon created (128x128 PNG)
- [ ] README updated with screenshots
- [ ] Extension built and tested locally
- [ ] Backend deployed to Railway/Render/Heroku
- [ ] Backend URL updated in extension
- [ ] Extension rebuilt with production URL
- [ ] Azure DevOps account created
- [ ] Personal Access Token generated
- [ ] Publisher account created
- [ ] Extension published to marketplace
- [ ] Marketplace listing enhanced
- [ ] Frontend deployed to Vercel/Netlify
- [ ] All services tested end-to-end
- [ ] Documentation updated
- [ ] CI/CD set up (optional)

---

## Costs Summary

| Service | Free Tier | Cost After Free |
|---------|-----------|-----------------|
| **Railway** | 500 hours/month | $5/month |
| **Vercel** | 100GB bandwidth | $20/month |
| **VS Code Marketplace** | FREE forever | FREE |
| **Gemini API** | 1500 req/day | $7/1M tokens |
| **Groq API** | FREE forever | FREE |

**Total**: $0/month for moderate usage!

---

## Support & Resources

- **Railway Docs**: https://docs.railway.app
- **VS Code Publishing**: https://code.visualstudio.com/api/working-with-extensions/publishing-extension
- **Vercel Docs**: https://vercel.com/docs
- **Gemini API**: https://ai.google.dev

---

**You're ready to deploy Pawa AI to production!** 🚀

Follow this guide step-by-step and you'll have:
- Extension live on VS Code Marketplace
- Backend running 24/7 on Railway
- Frontend deployed on Vercel
- Users around the world using your AI assistant!
