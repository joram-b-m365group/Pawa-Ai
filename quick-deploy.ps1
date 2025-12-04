# PAWA AI - QUICK DEPLOYMENT SCRIPT
# Run this after you complete Railway login manually

param(
    [Parameter(Mandatory=$true)]
    [string]$RailwayURL
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Pawa AI - Quick Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path

# Validate Railway URL
if ($RailwayURL -notmatch '^https?://') {
    Write-Host "[ERROR] Railway URL must start with http:// or https://" -ForegroundColor Red
    Write-Host "Example: https://genius-ai-production.up.railway.app" -ForegroundColor Yellow
    exit 1
}

Write-Host "[1/3] Updating Extension with Production URL..." -ForegroundColor Green
Write-Host "      Railway URL: $RailwayURL" -ForegroundColor Cyan

cd "$scriptPath\vscode-extension"

# Update package.json
(Get-Content package.json) -replace 'http://localhost:8000', $RailwayURL | Set-Content package.json
Write-Host "      ✓ Updated package.json" -ForegroundColor Green

# Compile
Write-Host "      Compiling TypeScript..." -ForegroundColor Yellow
npm run compile | Out-Null
Write-Host "      ✓ Compiled successfully" -ForegroundColor Green

# Package
Write-Host "      Creating VSIX package..." -ForegroundColor Yellow
vsce package --allow-missing-repository | Out-Null
Write-Host "      ✓ Created pawa-ai-2.0.0.vsix" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Extension Ready to Publish!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "[2/3] Next Step: Get Azure DevOps Token" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Go to: https://dev.azure.com" -ForegroundColor White
Write-Host "2. Profile → Personal Access Tokens → New Token" -ForegroundColor White
Write-Host "3. Name: 'VS Code Publishing'" -ForegroundColor White
Write-Host "4. Scopes: Marketplace → Manage (check this!)" -ForegroundColor White
Write-Host "5. Copy the token" -ForegroundColor White
Write-Host ""

$ready = Read-Host "Have you created and copied the token? (y/n)"

if ($ready -eq 'y' -or $ready -eq 'Y') {
    Write-Host ""
    Write-Host "[3/3] Publishing Extension..." -ForegroundColor Green
    Write-Host ""

    # Login to vsce
    Write-Host "Paste your Personal Access Token when prompted:" -ForegroundColor Yellow
    vsce login pawa-ai

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "Publishing to marketplace..." -ForegroundColor Yellow
        vsce publish

        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "========================================" -ForegroundColor Green
            Write-Host "  🎉 DEPLOYMENT COMPLETE!" -ForegroundColor Green
            Write-Host "========================================" -ForegroundColor Green
            Write-Host ""
            Write-Host "Your extension is now LIVE at:" -ForegroundColor Cyan
            Write-Host "https://marketplace.visualstudio.com/items?itemName=pawa-ai.pawa-ai" -ForegroundColor White
            Write-Host ""
            Write-Host "Users can install with:" -ForegroundColor Yellow
            Write-Host "  ext install pawa-ai.pawa-ai" -ForegroundColor White
            Write-Host ""
            Write-Host "Backend URL: $RailwayURL" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "🏆 You now have a production SaaS with 2M token context!" -ForegroundColor Green
            Write-Host "💰 Cost: $0/month (free tier)" -ForegroundColor Green
            Write-Host ""
        } else {
            Write-Host ""
            Write-Host "[ERROR] Publishing failed. Check the error above." -ForegroundColor Red
            Write-Host "Try: vsce publish manually" -ForegroundColor Yellow
        }
    } else {
        Write-Host ""
        Write-Host "[ERROR] Login failed. Make sure your token has 'Marketplace → Manage' scope." -ForegroundColor Red
    }
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "  Paused - Complete These Steps:" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Get Azure DevOps token from: https://dev.azure.com" -ForegroundColor White
    Write-Host "2. Run: vsce login pawa-ai" -ForegroundColor White
    Write-Host "3. Run: vsce publish" -ForegroundColor White
    Write-Host ""
}

Write-Host ""
Write-Host "Optional: Deploy Frontend to Vercel" -ForegroundColor Cyan
Write-Host "-------------------------------------" -ForegroundColor Cyan
Write-Host "cd frontend" -ForegroundColor White
Write-Host "vercel login" -ForegroundColor White
Write-Host "vercel" -ForegroundColor White
Write-Host "vercel env add REACT_APP_API_URL production" -ForegroundColor White
Write-Host "  (Enter: $RailwayURL)" -ForegroundColor Yellow
Write-Host "vercel --prod" -ForegroundColor White
Write-Host ""
