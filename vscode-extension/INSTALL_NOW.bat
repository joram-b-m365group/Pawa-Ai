@echo off
echo ========================================
echo Pawa AI Extension - Force Install
echo ========================================
echo.

echo Checking for VS Code...
where code >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] 'code' command not found in PATH
    echo Will try alternative method...
    goto ALTERNATIVE
)

echo [OK] VS Code found

echo.
echo Step 1: Uninstalling old version (if exists)...
code --uninstall-extension pawa-ai.pawa-ai >nul 2>nul
code --uninstall-extension pawa.pawa-ai >nul 2>nul
echo [OK] Old versions removed

echo.
echo Step 2: Installing new extension...
code --install-extension pawa-ai-1.0.1.vsix --force

if %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Extension installed!
    echo.
    echo ========================================
    echo Installation Complete!
    echo ========================================
    echo.
    echo Next steps:
    echo   1. Open or reload VS Code
    echo   2. Press Ctrl+Shift+A to open chat
    echo   3. Or click Pawa AI icon in sidebar
    echo.
    echo Backend must be running at: http://localhost:8000
    echo.
    pause
    exit /b 0
) else (
    echo [ERROR] Installation failed
    goto ALTERNATIVE
)

:ALTERNATIVE
echo.
echo ========================================
echo Alternative Installation Method
echo ========================================
echo.
echo I'll open the VSIX file for you.
echo In VS Code, it should prompt to install.
echo.
echo If not:
echo   1. Press Ctrl+Shift+P
echo   2. Type: Extensions: Install from VSIX
echo   3. Select: pawa-ai-1.0.1.vsix
echo   4. Click Install
echo.
pause

start "" "pawa-ai-1.0.1.vsix"
echo.
echo VSIX file opened. Please install through VS Code UI.
echo.
pause
