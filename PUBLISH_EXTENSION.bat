@echo off
echo ========================================
echo  Pawa AI - Publish Extension
echo ========================================
echo.

REM Check if ngrok URL is provided
if "%~1"=="" (
    echo ERROR: Please provide your ngrok URL!
    echo.
    echo Usage: PUBLISH_EXTENSION.bat "https://your-url.ngrok-free.app"
    echo.
    echo 1. Make sure ngrok is running ^(run START_NGROK.bat^)
    echo 2. Copy the https URL from ngrok
    echo 3. Run this script with that URL
    echo.
    pause
    exit /b 1
)

set NGROK_URL=%~1

echo Ngrok URL: %NGROK_URL%
echo.
echo [1/3] Updating extension configuration...

cd /d "%~dp0\vscode-extension"

REM Update package.json with ngrok URL
powershell -Command "(Get-Content package.json) -replace 'http://localhost:8000', '%NGROK_URL%' | Set-Content package.json"
echo ✓ Updated package.json

echo.
echo [2/3] Compiling and packaging extension...

call npm run compile
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Compilation failed!
    pause
    exit /b 1
)

call vsce package --allow-missing-repository
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Packaging failed!
    pause
    exit /b 1
)

echo ✓ Extension packaged: pawa-ai-2.0.0.vsix
echo.

echo ========================================
echo  [3/3] Ready to Publish!
echo ========================================
echo.
echo To publish to VS Code Marketplace:
echo.
echo 1. Go to: https://dev.azure.com
echo 2. Create Personal Access Token:
echo    - Name: VS Code Publishing
echo    - Scopes: Marketplace ^> Manage
echo 3. Run: vsce login pawa-ai
echo 4. Run: vsce publish
echo.
echo Your extension will be live at:
echo https://marketplace.visualstudio.com/items?itemName=pawa-ai.pawa-ai
echo.
pause
