@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Pawa AI Extension - Direct Installation
echo ========================================
echo.

REM Get VS Code extensions directory
set "VSCODE_EXT=%USERPROFILE%\.vscode\extensions"

if not exist "%VSCODE_EXT%" (
    echo [ERROR] VS Code extensions directory not found
    echo Location tried: %VSCODE_EXT%
    echo.
    echo Please make sure VS Code is installed.
    pause
    exit /b 1
)

echo [OK] VS Code extensions directory found
echo.

REM Extension directory name
set "EXT_DIR=%VSCODE_EXT%\pawa.pawa-ai-1.0.1"

echo Step 1: Removing old Pawa AI versions...
for /d %%d in ("%VSCODE_EXT%\pawa*pawa-ai*") do (
    echo   Removing: %%d
    rd /s /q "%%d" 2>nul
)
echo [OK] Old versions removed
echo.

echo Step 2: Creating new extension directory...
mkdir "%EXT_DIR%" 2>nul
echo [OK] Directory created: %EXT_DIR%
echo.

echo Step 3: Copying VSIX as ZIP...
copy /Y "pawa-ai-1.0.1.vsix" "pawa-ai-1.0.1.zip" >nul
echo [OK] VSIX copied as ZIP
echo.

echo Step 4: Extracting extension files...
powershell -Command "Expand-Archive -Path 'pawa-ai-1.0.1.zip' -DestinationPath 'temp_install' -Force"

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to extract files
    pause
    exit /b 1
)

echo [OK] Files extracted
echo.

echo Step 5: Moving files to VS Code extensions...
xcopy /E /I /Y "temp_install\extension\*" "%EXT_DIR%\" >nul

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to copy files
    pause
    exit /b 1
)

echo [OK] Files copied
echo.

echo Step 6: Cleaning up...
rd /s /q "temp_install" 2>nul
del "pawa-ai-1.0.1.zip" 2>nul
echo [OK] Cleanup complete
echo.

echo ========================================
echo SUCCESS! Extension Installed!
echo ========================================
echo.
echo Installation directory:
echo %EXT_DIR%
echo.
echo IMPORTANT - Next Steps:
echo   1. CLOSE ALL VS Code windows completely
echo   2. Reopen VS Code
echo   3. Press Ctrl+Shift+A to open Pawa AI chat
echo   4. Or click the Pawa AI icon in the left sidebar
echo.
echo Make sure backend is running:
echo   http://localhost:8000
echo.
echo Verification:
echo   - In VS Code, press Ctrl+Shift+X (Extensions)
echo   - Search for "Pawa AI"
echo   - Should show as installed
echo.
pause
