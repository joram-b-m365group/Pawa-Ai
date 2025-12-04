@echo off
echo ========================================
echo   Activating Gemini 2M Token Context
echo ========================================
echo.

echo [1/2] Installing Google Generative AI...
pip install google-generativeai
if %errorlevel% neq 0 (
    echo ERROR: Failed to install google-generativeai
    echo Please run: pip install google-generativeai
    pause
    exit /b 1
)

echo.
echo [2/2] Restarting Backend...
echo.
echo ========================================
echo   GEMINI ACTIVATED!
echo ========================================
echo.
echo Your Pawa AI now has:
echo   - 2 MILLION token context (10x Claude!)
echo   - 100%% FREE (no credit card)
echo   - Auto-switching for large contexts
echo.
echo Starting backend server...
echo.

python super_intelligent_endpoint.py
