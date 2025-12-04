@echo off
REM Genius AI - Stop Script
REM Double-click this file to stop both backend and frontend

echo ======================================================================
echo                    STOPPING GENIUS AI
echo ======================================================================
echo.

echo Stopping Backend (Port 8000)...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do (
    echo   Killing process %%a
    taskkill /F /PID %%a >nul 2>&1
)

echo Stopping Frontend (Port 3000)...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":3000" ^| find "LISTENING"') do (
    echo   Killing process %%a
    taskkill /F /PID %%a >nul 2>&1
)

echo.
echo ======================================================================
echo                   GENIUS AI STOPPED
echo ======================================================================
echo.
echo All services have been stopped.
echo To start again, double-click START_GENIUS_AI.bat
echo.
pause
