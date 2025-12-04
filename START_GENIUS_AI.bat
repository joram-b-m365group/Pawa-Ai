@echo off
REM Genius AI - Easy Launcher Script
REM Double-click this file to start both backend and frontend

echo ======================================================================
echo                    GENIUS AI - LAUNCHER
echo ======================================================================
echo.
echo Starting Genius AI...
echo.

REM Kill any existing processes on ports 8000 and 3000
echo Cleaning up old processes...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do taskkill /F /PID %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| find ":3000" ^| find "LISTENING"') do taskkill /F /PID %%a >nul 2>&1

REM Wait a moment for ports to free up
timeout /t 2 /nobreak >nul

echo.
echo [1/2] Starting Super Intelligent Backend API (Port 8000)...
cd /d "%~dp0backend"
start "Genius AI - Super Intelligent Backend" /MIN cmd /c "C:\Users\Jorams\anaconda3\python.exe super_intelligent_endpoint.py"

REM Wait for backend to start
timeout /t 5 /nobreak >nul

echo [2/2] Starting Frontend (Port 3000)...
cd /d "%~dp0frontend"
start "Genius AI - Frontend" /MIN cmd /c "npm run dev"

REM Wait for frontend to start
timeout /t 8 /nobreak >nul

echo.
echo ======================================================================
echo                   GENIUS AI IS NOW RUNNING!
echo ======================================================================
echo.
echo  Backend:  http://localhost:8000
echo  Frontend: http://localhost:3000
echo.
echo  Opening browser in 3 seconds...
echo ======================================================================
echo.

timeout /t 3 /nobreak >nul

REM Open browser
start http://localhost:3000

echo.
echo Browser opened! Genius AI is ready to use.
echo.
echo To stop Genius AI:
echo   - Close the Backend window
echo   - Close the Frontend window
echo   OR double-click STOP_GENIUS_AI.bat
echo.
pause
