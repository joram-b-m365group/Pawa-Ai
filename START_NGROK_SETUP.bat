@echo off
echo ========================================
echo  Ngrok Setup for Pawa AI
echo ========================================
echo.

cd /d "%~dp0"

REM Check if ngrok.zip exists
if exist ngrok.zip (
    echo Extracting ngrok...
    powershell -Command "Expand-Archive -Path ngrok.zip -DestinationPath . -Force"
    echo.
    echo ✓ Ngrok extracted successfully!
    echo.
    echo Now run: START_NGROK.bat
    pause
) else (
    echo ERROR: ngrok.zip not found!
    echo Download is still in progress...
    echo Please wait and try again in a moment.
    pause
)
