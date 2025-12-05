# Pawa AI - One-Command Deployment
# Run this script to deploy everything automatically

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Pawa AI - Automated Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get the script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if Railway CLI is installed
Write-Host "[Checking] Railway CLI..." -ForegroundColor Yellow
if (!(Get-Command railway -ErrorAction SilentlyContinue)) {
    Write-Host "[Installing] Railway CLI..." -ForegroundColor Green
    npm install -g @railway/cli
} else {
    Write-Host "[OK] Railway CLI is installed" -ForegroundColor Green
}

# Check if vsce is installed
Write-Host "[Checking] VS Code Extension Manager..." -ForegroundColor Yellow
if (!(Get-Command vsce -ErrorAction SilentlyContinue)) {
    Write-Host "[Installing] vsce..." -ForegroundColor Green
    npm install -g @vscode/vsce
} else {
    Write-Host "[OK] vsce is installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Step 1: Deploy Backend to Railway" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

cd "$scriptPath\backend"

Write-Host "[Action Required] Please login to Railway..." -ForegroundColor Yellow
railway login

Write-Host "[Creating] Railway project..." -ForegroundColor Green
railway init

Write-Host "[Deploying] Backend..." -ForegroundColor Green
railway up

Write-Host "[Setting] Environment variables..." -ForegroundColor Green
railway variables set GOOGLE_API_KEY=AIzaSyBzT0i4WjPexzHG-QR5RIARNLX0ZOjK8uM
railway variables set GROQ_API_KEY=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
railway variables set PORT=8000

Write-Host "[Getting] Public URL..." -ForegroundColor Green
$RAILWAY_URL = railway domain

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host " Backend Deployed Successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "URL: $RAILWAY_URL" -ForegroundColor Cyan
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Step 2: Update Extension" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

cd "$scriptPath\vscode-extension"

Write-Host "[Updating] Extension package.json with production URL..." -ForegroundColor Green
(Get-Content package.json) -replace 'http://localhost:8000', $RAILWAY_URL | Set-Content package.json

Write-Host "[Compiling] Extension..." -ForegroundColor Green
npm run compile

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host " Extension Updated!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Step 3: Package Extension" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "[Packaging] Extension as VSIX..." -ForegroundColor Green
vsce package

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host " Extension Packaged!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "File: pawa-ai-2.0.0.vsix" -ForegroundColor Cyan
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Step 4: Publish to Marketplace (Manual)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To publish to VS Code Marketplace:" -ForegroundColor Yellow
Write-Host "1. Go to: https://dev.azure.com" -ForegroundColor White
Write-Host "2. Create Personal Access Token (Marketplace → Manage)" -ForegroundColor White
Write-Host "3. Run: vsce login pawa-ai" -ForegroundColor White
Write-Host "4. Enter your PAT when prompted" -ForegroundColor White
Write-Host "5. Run: vsce publish" -ForegroundColor White
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Step 5: Deploy Frontend (Optional)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
$deploy_frontend = Read-Host "Deploy frontend to Vercel? (y/n)"

if ($deploy_frontend -eq 'y' -or $deploy_frontend -eq 'Y') {
    cd "$scriptPath\frontend"

    if (!(Get-Command vercel -ErrorAction SilentlyContinue)) {
        Write-Host "[Installing] Vercel CLI..." -ForegroundColor Green
        npm install -g vercel
    }

    Write-Host "[Action Required] Please login to Vercel..." -ForegroundColor Yellow
    vercel login

    Write-Host "[Deploying] Frontend..." -ForegroundColor Green
    vercel --yes

    Write-Host "[Setting] Environment variable..." -ForegroundColor Green
    Write-Host "When prompted, enter API URL: $RAILWAY_URL" -ForegroundColor Yellow
    vercel env add REACT_APP_API_URL

    Write-Host "[Deploying] To production..." -ForegroundColor Green
    $VERCEL_URL = vercel --prod

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host " Frontend Deployed!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "URL: $VERCEL_URL" -ForegroundColor Cyan
    Write-Host ""
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host " Deployment Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "--------" -ForegroundColor Cyan
Write-Host "Backend URL:  $RAILWAY_URL" -ForegroundColor White
if ($VERCEL_URL) {
    Write-Host "Frontend URL: $VERCEL_URL" -ForegroundColor White
}
Write-Host "Extension:    $scriptPath\vscode-extension\pawa-ai-2.0.0.vsix" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Create Azure DevOps account: https://dev.azure.com" -ForegroundColor White
Write-Host "2. Get Personal Access Token" -ForegroundColor White
Write-Host "3. Publish extension: vsce login pawa-ai && vsce publish" -ForegroundColor White
Write-Host ""
Write-Host "Congratulations! Your Pawa AI is ready for production! 🎉" -ForegroundColor Green
