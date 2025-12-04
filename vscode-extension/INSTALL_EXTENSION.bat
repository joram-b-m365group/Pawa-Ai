@echo off
echo ====================================
echo Pawa AI VS Code Extension Installer
echo ====================================
echo.

echo Step 1: Checking if extension file exists...
if not exist "pawa-ai-1.0.0.vsix" (
    echo [ERROR] Extension file not found!
    echo Please run this from the vscode-extension directory.
    pause
    exit /b 1
)
echo [OK] Extension file found

echo.
echo Step 2: Installing extension...
echo.
echo IMPORTANT: This will open VS Code.
echo In VS Code:
echo   1. Press Ctrl+Shift+X (Extensions panel)
echo   2. If you see old "Pawa AI" extension, click gear icon and Uninstall
echo   3. After uninstalling, press Ctrl+Shift+P
echo   4. Type: Extensions: Install from VSIX
echo   5. Select this file: %cd%\pawa-ai-1.0.0.vsix
echo   6. Click Install
echo   7. Reload VS Code when prompted
echo.
echo Press any key to open VS Code...
pause > nul

echo.
echo Opening VS Code with extension file...
start "" "pawa-ai-1.0.0.vsix"

echo.
echo ====================================
echo Installation Steps:
echo ====================================
echo.
echo 1. VS Code should have opened
echo 2. It may ask to install the extension
echo 3. Click "Install"
echo 4. If not, follow the instructions above
echo.
echo After installation:
echo   - Press Ctrl+Shift+P to open chat
echo   - Or click Pawa AI icon in sidebar
echo.
echo Backend must be running at: http://localhost:8000
echo.
pause
