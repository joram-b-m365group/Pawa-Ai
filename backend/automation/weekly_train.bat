@echo off
echo ============================================================
echo Genius AI - Weekly Model Training
echo ============================================================
echo Starting weekly training: %date% %time%
echo.

cd /d C:\Users\Jorams\genius-ai

echo [1/3] Preparing training data...
echo   - Checking collected data from past week
for /f %%i in ('dir /b /a-d data\stackoverflow\*.json 2^>nul ^| find /c /v ""') do set SO_FILES=%%i
for /f %%i in ('dir /b /a-d data\wikipedia\*.json 2^>nul ^| find /c /v ""') do set WIKI_FILES=%%i
echo   - StackOverflow files: %SO_FILES%
echo   - Wikipedia files: %WIKI_FILES%
echo.

echo [2/3] Training enhanced model with all collected data...
/c/Users/Jorams/anaconda3/python.exe backend/train_enhanced.py
if %errorlevel% neq 0 (
    echo [ERROR] Training failed
    echo ERROR: %date% %time% - Training failed >> logs/training.log
    goto :error
)
echo [OK] Training complete
echo.

echo [3/3] Logging results...
echo SUCCESS: %date% %time% - Weekly training completed >> logs/training.log
echo.
echo ============================================================
echo Weekly training completed successfully!
echo New model saved to: genius_model_enhanced/
echo Check logs/training.log for details
echo ============================================================
pause
exit /b 0

:error
echo ============================================================
echo Training encountered errors - check logs
echo ============================================================
pause
exit /b 1
