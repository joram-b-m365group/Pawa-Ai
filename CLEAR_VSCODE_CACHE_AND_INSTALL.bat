@echo off
echo ========================================
echo Clear VS Code Cache and Reinstall Pawa AI
echo ========================================
echo.

echo IMPORTANT: Close ALL VS Code windows before continuing!
echo.
pause

echo.
echo Step 1: Clearing VS Code cache...
rd /s /q "%APPDATA%\Code\Cache" 2>nul
rd /s /q "%APPDATA%\Code\CachedData" 2>nul
rd /s /q "%APPDATA%\Code\CachedExtensions" 2>nul
rd /s /q "%APPDATA%\Code\CachedExtensionVSIXs" 2>nul
rd /s /q "%LOCALAPPDATA%\Programs\Microsoft VS Code\resources\app\extensions" 2>nul
echo [OK] Cache cleared

echo.
echo Step 2: Removing old Pawa AI installations...
rd /s /q "%USERPROFILE%\.vscode\extensions\pawa-ai.pawa-ai-1.0.0" 2>nul
rd /s /q "%USERPROFILE%\.vscode\extensions\pawa-ai.pawa-ai-1.0.1" 2>nul
rd /s /q "%USERPROFILE%\.vscode\extensions\pawa-ai.pawa-ai-1.0.2" 2>nul
rd /s /q "%USERPROFILE%\.vscode\extensions\pawa.pawa-ai-1.0.1" 2>nul
echo [OK] Old versions removed

echo.
echo Step 3: Installing Pawa AI extension...
cd /d "%~dp0vscode-extension"
powershell -ExecutionPolicy Bypass -File install_final.ps1

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo CRITICAL NEXT STEPS:
echo   1. Open VS Code
echo   2. Press Ctrl+Shift+X (Extensions)
echo   3. Look for "Pawa AI" in the list
echo   4. If you see it, click the gear icon and Enable
echo   5. Press Ctrl+Shift+A to open chat
echo.
echo If extension still doesn't show:
echo   - Try: Ctrl+Shift+P → "Developer: Reload Window"
echo   - Or restart your computer
echo.
pause
