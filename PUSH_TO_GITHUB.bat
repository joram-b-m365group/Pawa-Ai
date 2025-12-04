@echo off
echo ========================================
echo  Pawa AI - Push to GitHub
echo ========================================
echo.

cd /d "%~dp0"

REM Set git user info (you can change this!)
echo [1/4] Configuring Git...
git config user.name "Jorams"
git config user.email "jorams@pawa-ai.com"
echo     ✓ Git configured

echo.
echo [2/4] Adding all files...
git add .
echo     ✓ Files staged

echo.
echo [3/4] Creating commit...
git commit -m "Initial commit: Pawa AI with 2M token Gemini context"
echo     ✓ Commit created

echo.
echo ========================================
echo  Ready to Push to GitHub!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Create a new repository on GitHub:
echo    https://github.com/new
echo.
echo 2. Name it: pawa-ai
echo.
echo 3. DON'T initialize with README
echo.
echo 4. After creating, run these commands:
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/pawa-ai.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo (Replace YOUR_USERNAME with your GitHub username!)
echo.
pause
