@echo off
echo ========================================
echo Pawa AI Extension - Diagnostic Check
echo ========================================
echo.

set "EXT_DIR=%USERPROFILE%\.vscode\extensions\pawa-ai.pawa-ai-1.0.2"

echo Checking extension directory...
if exist "%EXT_DIR%" (
    echo [OK] Extension directory exists
    echo Location: %EXT_DIR%
) else (
    echo [ERROR] Extension directory NOT found
    echo Expected: %EXT_DIR%
    echo.
    echo Please run install_final.ps1 first
    pause
    exit /b 1
)

echo.
echo Checking critical files...

if exist "%EXT_DIR%\package.json" (
    echo [OK] package.json
) else (
    echo [ERROR] package.json missing
)

if exist "%EXT_DIR%\out\extension.js" (
    echo [OK] out\extension.js
) else (
    echo [ERROR] out\extension.js missing
)

if exist "%EXT_DIR%\out\chat\ChatProvider.js" (
    echo [OK] out\chat\ChatProvider.js
) else (
    echo [ERROR] out\chat\ChatProvider.js missing
)

if exist "%EXT_DIR%\out\ai\PawaAI.js" (
    echo [OK] out\ai\PawaAI.js
) else (
    echo [ERROR] out\ai\PawaAI.js missing
)

if exist "%EXT_DIR%\out\commands\index.js" (
    echo [OK] out\commands\index.js
) else (
    echo [ERROR] out\commands\index.js missing
)

echo.
echo Checking package.json content...
findstr /C:"\"name\": \"pawa-ai\"" "%EXT_DIR%\package.json" >nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Extension name correct
) else (
    echo [ERROR] Extension name issue
)

findstr /C:"\"publisher\": \"pawa-ai\"" "%EXT_DIR%\package.json" >nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Publisher correct
) else (
    echo [ERROR] Publisher issue
)

findstr /C:"\"version\": \"1.0.2\"" "%EXT_DIR%\package.json" >nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Version 1.0.2
) else (
    echo [ERROR] Version mismatch
)

echo.
echo ========================================
echo What to do if extension still not working:
echo ========================================
echo.
echo 1. CLOSE ALL VS Code windows completely
echo 2. Make sure no code.exe processes running (Task Manager)
echo 3. Reopen VS Code
echo 4. Check Extensions panel (Ctrl+Shift+X)
echo 5. Search for "Pawa AI"
echo 6. If not showing, try Developer: Reload Window
echo 7. Check Developer Tools console (Help menu)
echo.
echo To open chat after VS Code loads:
echo   - Press Ctrl+Shift+A
echo   - Or click Pawa AI icon in activity bar
echo   - Or Ctrl+Shift+P and type "Pawa AI: Open Chat"
echo.
pause
