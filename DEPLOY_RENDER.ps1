# PAWA AI - Deploy to Render.com (100% FREE)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Pawa AI - Deploy to Render.com" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "✓ Render.com offers 750 hours/month FREE (no credit card!)" -ForegroundColor Green
Write-Host ""

# Check if render CLI is installed
Write-Host "[1/4] Checking Render CLI..." -ForegroundColor Yellow
if (!(Get-Command render -ErrorAction SilentlyContinue)) {
    Write-Host "      Installing Render CLI..." -ForegroundColor Yellow
    npm install -g @render/cli 2>&1 | Out-Null

    if ($LASTEXITCODE -ne 0) {
        Write-Host "      [INFO] Could not install Render CLI via npm" -ForegroundColor Yellow
        Write-Host "      Use web interface instead (easier!)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  TWO OPTIONS TO DEPLOY:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "OPTION A: Web Interface (RECOMMENDED - 5 minutes)" -ForegroundColor Green
Write-Host "----------------------------------------------------" -ForegroundColor Gray
Write-Host "1. Go to: https://render.com/new/web" -ForegroundColor White
Write-Host "2. Select 'Public Git repository'" -ForegroundColor White
Write-Host "3. Repository URL: https://github.com/YOUR_USERNAME/genius-ai" -ForegroundColor White
Write-Host "   (Or connect your GitHub account)" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Configure:" -ForegroundColor White
Write-Host "   Name: pawa-ai-backend" -ForegroundColor Gray
Write-Host "   Region: Oregon (or closest)" -ForegroundColor Gray
Write-Host "   Branch: main" -ForegroundColor Gray
Write-Host "   Root Directory: backend" -ForegroundColor Gray
Write-Host "   Runtime: Python 3" -ForegroundColor Gray
Write-Host "   Build: pip install -r requirements.txt" -ForegroundColor Gray
Write-Host "   Start: uvicorn super_intelligent_endpoint:app --host 0.0.0.0 --port `$PORT" -ForegroundColor Gray
Write-Host ""
Write-Host "5. Add Environment Variables:" -ForegroundColor White
Write-Host "   GOOGLE_API_KEY=AIzaSyBzT0i4WjPexzHG-QR5RIARNLX0ZOjK8uM" -ForegroundColor Gray
Write-Host "   GROQ_API_KEY=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" -ForegroundColor Gray
Write-Host ""
Write-Host "6. Click 'Create Web Service'" -ForegroundColor White
Write-Host ""
Write-Host "Your URL will be: https://pawa-ai-backend.onrender.com" -ForegroundColor Cyan
Write-Host ""
Write-Host ""

Write-Host "OPTION B: Use Blueprint (FASTEST - 2 minutes)" -ForegroundColor Green
Write-Host "----------------------------------------------------" -ForegroundColor Gray
Write-Host "1. Go to: https://render.com" -ForegroundColor White
Write-Host "2. Click 'New +' → 'Blueprint'" -ForegroundColor White
Write-Host "3. Select your repo or paste: https://github.com/YOUR_USERNAME/genius-ai" -ForegroundColor White
Write-Host "4. Render will auto-detect render.yaml (already created!)" -ForegroundColor White
Write-Host "5. Click 'Apply'" -ForegroundColor White
Write-Host ""
Write-Host "✓ render.yaml is already configured at: $scriptPath\backend\render.yaml" -ForegroundColor Green
Write-Host ""
Write-Host ""

Write-Host "========================================" -ForegroundColor Yellow
Write-Host "  NO GIT REPO? NO PROBLEM!" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "OPTION C: Deploy Without Git (EASIEST)" -ForegroundColor Green
Write-Host "----------------------------------------------------" -ForegroundColor Gray
Write-Host ""
Write-Host "I'll create a quick GitHub repo setup for you..." -ForegroundColor Yellow
Write-Host ""

$setupGit = Read-Host "Want me to help setup Git + GitHub? (y/n)"

if ($setupGit -eq 'y' -or $setupGit -eq 'Y') {
    Write-Host ""
    Write-Host "Setting up Git repository..." -ForegroundColor Green

    cd $scriptPath

    # Initialize git if not already
    if (!(Test-Path ".git")) {
        git init
        Write-Host "✓ Git initialized" -ForegroundColor Green
    }

    # Create .gitignore if not exists
    if (!(Test-Path ".gitignore")) {
        @"
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/
venv/
.env
node_modules/
.vscode/
*.vsix
.DS_Store
"@ | Out-File -FilePath ".gitignore" -Encoding utf8
        Write-Host "✓ .gitignore created" -ForegroundColor Green
    }

    # Add and commit
    git add .
    git commit -m "Initial commit for deployment" 2>&1 | Out-Null
    Write-Host "✓ Files committed" -ForegroundColor Green

    Write-Host ""
    Write-Host "Now create GitHub repository:" -ForegroundColor Yellow
    Write-Host "1. Go to: https://github.com/new" -ForegroundColor White
    Write-Host "2. Name: genius-ai" -ForegroundColor White
    Write-Host "3. Public or Private (your choice)" -ForegroundColor White
    Write-Host "4. DON'T initialize with README" -ForegroundColor White
    Write-Host "5. Create repository" -ForegroundColor White
    Write-Host ""
    Write-Host "Then run these commands:" -ForegroundColor Yellow
    Write-Host "git remote add origin https://github.com/YOUR_USERNAME/genius-ai.git" -ForegroundColor Gray
    Write-Host "git branch -M main" -ForegroundColor Gray
    Write-Host "git push -u origin main" -ForegroundColor Gray
    Write-Host ""
    Write-Host "After pushing, use Render Option A or B above!" -ForegroundColor Green
    Write-Host ""
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AFTER DEPLOYMENT:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Once your backend is live on Render, run:" -ForegroundColor Yellow
Write-Host ""
Write-Host "cd $scriptPath" -ForegroundColor White
Write-Host "powershell -ExecutionPolicy Bypass -File quick-deploy.ps1 -RailwayURL `"https://pawa-ai-backend.onrender.com`"" -ForegroundColor White
Write-Host ""
Write-Host "(Replace the URL with your actual Render URL if different)" -ForegroundColor Gray
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  📚 HELPFUL LINKS:" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Render Dashboard: https://dashboard.render.com" -ForegroundColor Cyan
Write-Host "Render Docs: https://render.com/docs/web-services" -ForegroundColor Cyan
Write-Host "GitHub: https://github.com" -ForegroundColor Cyan
Write-Host ""
Write-Host "Need help? Check ALTERNATIVE_DEPLOY.md for more options!" -ForegroundColor Yellow
Write-Host ""
