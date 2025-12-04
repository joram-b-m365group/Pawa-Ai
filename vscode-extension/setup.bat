@echo off
REM Pawa AI VS Code Extension - Setup Script for Windows
REM This script sets up the development environment and builds the extension

echo.
echo ================================
echo Pawa AI VS Code Extension Setup
echo ================================
echo.

REM Check Node.js
echo Checking Node.js...
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not installed. Please install Node.js 16+ first.
    pause
    exit /b 1
)

echo [OK] Node.js found
node -v

REM Check npm
echo.
echo Checking npm...
where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] npm is not installed.
    pause
    exit /b 1
)

echo [OK] npm found
npm -v

REM Install dependencies
echo.
echo Installing dependencies...
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed

REM Compile TypeScript
echo.
echo Compiling TypeScript...
call npm run compile
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] TypeScript compilation failed
    pause
    exit /b 1
)
echo [OK] TypeScript compiled successfully

REM Check vsce
echo.
echo Checking vsce...
where vsce >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [WARN] vsce not found. Installing globally...
    call npm install -g @vscode/vsce
    echo [OK] vsce installed
) else (
    echo [OK] vsce found
)

REM Verify build
echo.
echo Verifying build output...
if not exist "out" (
    echo [ERROR] Build output directory 'out' not found
    pause
    exit /b 1
)

if not exist "out\extension.js" (
    echo [ERROR] Main extension file 'out\extension.js' not found
    pause
    exit /b 1
)

echo [OK] Build output verified

REM Success message
echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo Next steps:
echo.
echo 1. Test the extension:
echo    - Open this folder in VS Code
echo    - Press F5 to launch Extension Development Host
echo.
echo 2. Package the extension:
echo    npm run package
echo.
echo 3. Install the extension:
echo    code --install-extension pawa-ai-1.0.0.vsix
echo.
echo 4. Make sure Pawa AI backend is running:
echo    http://localhost:8000
echo.
echo Documentation:
echo    - QUICK_START.md
echo    - README.md
echo    - INSTALLATION.md
echo.
echo Happy coding with Pawa AI!
echo.
pause
