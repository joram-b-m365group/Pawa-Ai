# One-Command Deployment Script

## Quick Deploy Commands

### 1. Deploy Backend to Railway

```bash
# Install Railway CLI (one-time)
npm install -g @railway/cli

# Deploy backend
cd backend
railway login
railway init
railway up

# Set environment variables
railway variables set GOOGLE_API_KEY=AIzaSyBzT0i4WjPexzHG-QR5RIARNLX0ZOjK8uM
railway variables set GROQ_API_KEY=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
railway variables set PORT=8000

# Get your public URL
railway domain

# COPY THE URL - You'll need it next!
```

**Result**: Backend live at `https://your-app.up.railway.app`

---

### 2. Update Extension with Production URL

```bash
# Open package.json and change the API URL
cd ../vscode-extension

# Replace "http://localhost:8000" with your Railway URL in package.json line 149
# Or run this command (replace YOUR_RAILWAY_URL):
powershell -Command "(Get-Content package.json) -replace 'http://localhost:8000', 'https://your-app.up.railway.app' | Set-Content package.json"

# Recompile
npm run compile
```

---

### 3. Package Extension

```bash
# Still in vscode-extension directory
npm install -g @vscode/vsce

# Package
vsce package

# This creates: pawa-ai-2.0.0.vsix
```

**Result**: VSIX package ready at `vscode-extension/pawa-ai-2.0.0.vsix`

---

### 4. Publish to VS Code Marketplace

#### A. Create Publisher Account (First Time Only)

1. Go to: https://dev.azure.com
2. Sign in with Microsoft account
3. User Settings → Personal Access Tokens → New Token
4. Name: "VS Code Publishing"
5. Scopes: Select "Marketplace" → "Manage"
6. Create token and COPY IT

#### B. Publish

```bash
# Login (use PAT from above when prompted)
vsce login pawa-ai

# Publish
vsce publish

# Or if publisher doesn't exist yet:
vsce create-publisher pawa-ai
vsce publish
```

**Result**: Extension live at `https://marketplace.visualstudio.com/items?itemName=pawa-ai.pawa-ai`

---

### 5. Deploy Frontend to Vercel (Optional)

```bash
# Install Vercel CLI (one-time)
npm install -g vercel

# Deploy frontend
cd ../frontend
vercel login
vercel

# Add API URL environment variable
vercel env add REACT_APP_API_URL
# Enter your Railway URL: https://your-app.up.railway.app

# Deploy to production
vercel --prod
```

**Result**: Frontend live at `https://your-app.vercel.app`

---

## All-in-One PowerShell Script (Windows)

Save this as `deploy-all.ps1`:

```powershell
# Pawa AI - One-Command Deployment
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Pawa AI - Automated Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check if Railway CLI is installed
if (!(Get-Command railway -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Railway CLI..." -ForegroundColor Yellow
    npm install -g @railway/cli
}

# Deploy Backend
Write-Host "`n[1/5] Deploying Backend to Railway..." -ForegroundColor Green
cd backend
railway login
railway init
railway up

Write-Host "`nSetting environment variables..." -ForegroundColor Yellow
railway variables set GOOGLE_API_KEY=AIzaSyBzT0i4WjPexzHG-QR5RIARNLX0ZOjK8uM
railway variables set GROQ_API_KEY=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
railway variables set PORT=8000

$RAILWAY_URL = railway domain
Write-Host "`nBackend deployed at: $RAILWAY_URL" -ForegroundColor Cyan

# Update Extension
Write-Host "`n[2/5] Updating Extension with Production URL..." -ForegroundColor Green
cd ../vscode-extension
(Get-Content package.json) -replace 'http://localhost:8000', $RAILWAY_URL | Set-Content package.json
npm run compile

# Package Extension
Write-Host "`n[3/5] Packaging Extension..." -ForegroundColor Green
if (!(Get-Command vsce -ErrorAction SilentlyContinue)) {
    npm install -g @vscode/vsce
}
vsce package

Write-Host "`n[4/5] Extension packaged: pawa-ai-2.0.0.vsix" -ForegroundColor Cyan
Write-Host "`nTo publish to marketplace, run:" -ForegroundColor Yellow
Write-Host "  cd vscode-extension" -ForegroundColor White
Write-Host "  vsce login pawa-ai" -ForegroundColor White
Write-Host "  vsce publish" -ForegroundColor White

# Deploy Frontend (Optional)
Write-Host "`n[5/5] Deploy Frontend? (y/n)" -ForegroundColor Green
$deploy_frontend = Read-Host

if ($deploy_frontend -eq 'y') {
    cd ../frontend
    if (!(Get-Command vercel -ErrorAction SilentlyContinue)) {
        npm install -g vercel
    }
    vercel login
    vercel --yes
    vercel env add REACT_APP_API_URL $RAILWAY_URL
    vercel --prod
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Deployment Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "1. Create publisher at: https://dev.azure.com" -ForegroundColor White
Write-Host "2. Get Personal Access Token (Marketplace → Manage)" -ForegroundColor White
Write-Host "3. Run: vsce login pawa-ai" -ForegroundColor White
Write-Host "4. Run: vsce publish" -ForegroundColor White
Write-Host "`nYour backend: $RAILWAY_URL" -ForegroundColor Cyan
```

Run it:
```powershell
powershell -ExecutionPolicy Bypass -File deploy-all.ps1
```

---

## All-in-One Bash Script (Mac/Linux)

Save this as `deploy-all.sh`:

```bash
#!/bin/bash

# Pawa AI - One-Command Deployment
echo "========================================"
echo "  Pawa AI - Automated Deployment"
echo "========================================"

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Deploy Backend
echo -e "\n[1/5] Deploying Backend to Railway..."
cd backend
railway login
railway init
railway up

echo "Setting environment variables..."
railway variables set GOOGLE_API_KEY=AIzaSyBzT0i4WjPexzHG-QR5RIARNLX0ZOjK8uM
railway variables set GROQ_API_KEY=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
railway variables set PORT=8000

RAILWAY_URL=$(railway domain)
echo -e "\nBackend deployed at: $RAILWAY_URL"

# Update Extension
echo -e "\n[2/5] Updating Extension with Production URL..."
cd ../vscode-extension
sed -i "s|http://localhost:8000|$RAILWAY_URL|g" package.json
npm run compile

# Package Extension
echo -e "\n[3/5] Packaging Extension..."
if ! command -v vsce &> /dev/null; then
    npm install -g @vscode/vsce
fi
vsce package

echo -e "\n[4/5] Extension packaged: pawa-ai-2.0.0.vsix"
echo -e "\nTo publish to marketplace, run:"
echo "  cd vscode-extension"
echo "  vsce login pawa-ai"
echo "  vsce publish"

# Deploy Frontend (Optional)
echo -e "\n[5/5] Deploy Frontend? (y/n)"
read deploy_frontend

if [ "$deploy_frontend" = "y" ]; then
    cd ../frontend
    if ! command -v vercel &> /dev/null; then
        npm install -g vercel
    fi
    vercel login
    vercel --yes
    vercel env add REACT_APP_API_URL $RAILWAY_URL
    vercel --prod
fi

echo -e "\n========================================"
echo "  Deployment Complete!"
echo "========================================"
echo -e "\nNext Steps:"
echo "1. Create publisher at: https://dev.azure.com"
echo "2. Get Personal Access Token (Marketplace → Manage)"
echo "3. Run: vsce login pawa-ai"
echo "4. Run: vsce publish"
echo -e "\nYour backend: $RAILWAY_URL"
```

Run it:
```bash
chmod +x deploy-all.sh
./deploy-all.sh
```

---

## Manual Deployment Checklist

- [ ] Install Railway CLI: `npm install -g @railway/cli`
- [ ] Deploy backend: `cd backend && railway up`
- [ ] Set environment variables in Railway
- [ ] Copy Railway URL
- [ ] Update extension package.json with Railway URL
- [ ] Recompile extension: `npm run compile`
- [ ] Package extension: `vsce package`
- [ ] Create Azure DevOps account
- [ ] Get Personal Access Token
- [ ] Publish: `vsce publish`
- [ ] (Optional) Deploy frontend to Vercel

---

## What You Get

After running these commands:

✅ **Backend**: Live on Railway (24/7)
✅ **Extension**: Packaged and ready to publish
✅ **Frontend**: (Optional) Live on Vercel

**Total Time**: 15-20 minutes
**Total Cost**: $0/month (free tier)

---

## Support

Issues? Check:
- [PRODUCTION_DEPLOYMENT_GUIDE.md](PRODUCTION_DEPLOYMENT_GUIDE.md)
- [DEPLOYMENT_STATUS.md](DEPLOYMENT_STATUS.md)
- Railway logs: `railway logs`
- Vercel logs: `vercel logs`
