@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Pawa AI - Manual Installation Method
echo ========================================
echo.

REM Get VS Code extensions directory
set "VSCODE_EXT=%USERPROFILE%\.vscode\extensions"

if not exist "%VSCODE_EXT%" (
    echo [ERROR] VS Code extensions directory not found: %VSCODE_EXT%
    echo.
    echo Please make sure VS Code is installed.
    pause
    exit /b 1
)

echo [OK] VS Code extensions directory found
echo Location: %VSCODE_EXT%
echo.

REM Create extension directory
set "EXT_DIR=%VSCODE_EXT%\pawa.pawa-ai-1.0.1"

echo Removing old versions...
rd /s /q "%VSCODE_EXT%\pawa-ai.pawa-ai-*" 2>nul
rd /s /q "%VSCODE_EXT%\pawa.pawa-ai-*" 2>nul
echo [OK] Old versions removed

echo.
echo Creating extension directory...
mkdir "%EXT_DIR%" 2>nul

echo Extracting extension files...
powershell -Command "Expand-Archive -Path 'pawa-ai-1.0.1.vsix' -DestinationPath '%EXT_DIR%' -Force"

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to extract VSIX
    pause
    exit /b 1
)

echo [OK] Files extracted

echo.
echo Moving files to correct location...
move "%EXT_DIR%\extension\*" "%EXT_DIR%\" >nul 2>nul
rd /s /q "%EXT_DIR%\extension" 2>nul
del "%EXT_DIR%\[Content_Types].xml" 2>nul
del "%EXT_DIR%\extension.vsixmanifest" 2>nul

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Extension installed to:
echo %EXT_DIR%
echo.
echo Next steps:
echo   1. Close ALL VS Code windows
echo   2. Reopen VS Code
echo   3. Press Ctrl+Shift+A to open chat
echo   4. Or click Pawa AI icon in sidebar
echo.
echo Make sure backend is running at: http://localhost:8000
echo.
pause
