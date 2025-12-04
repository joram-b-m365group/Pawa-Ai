@echo off
echo ========================================
echo  Starting Ngrok Tunnel for Pawa AI
echo ========================================
echo.
echo Your backend is running on port 8000
echo Creating public tunnel...
echo.

cd /d "%~dp0"

if exist ngrok.exe (
    echo Starting ngrok...
    ngrok.exe http 8000
) else (
    echo ERROR: ngrok.exe not found!
    echo Please run: START_NGROK_SETUP.bat first
    pause
)
