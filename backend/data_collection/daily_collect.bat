@echo off
echo ============================================================
echo Genius AI - Daily Data Collection
echo ============================================================
echo Starting data collection: %date% %time%
echo.

cd /d C:\Users\Jorams\genius-ai

echo [1/3] Collecting StackOverflow examples...
/c/Users/Jorams/anaconda3/python.exe backend/data_collection/stackoverflow_scraper.py
if %errorlevel% neq 0 (
    echo [ERROR] StackOverflow scraper failed
    echo ERROR: %date% %time% - StackOverflow scraper failed >> logs/collection.log
    goto :error
)
echo [OK] StackOverflow collection complete
echo.

echo [2/3] Downloading Wikipedia articles...
/c/Users/Jorams/anaconda3/python.exe backend/data_collection/wikipedia_downloader.py
if %errorlevel% neq 0 (
    echo [ERROR] Wikipedia downloader failed
    echo ERROR: %date% %time% - Wikipedia downloader failed >> logs/collection.log
    goto :error
)
echo [OK] Wikipedia download complete
echo.

echo [3/3] Logging results...
echo SUCCESS: %date% %time% - Data collection completed >> logs/collection.log
echo.
echo ============================================================
echo Data collection completed successfully!
echo Check logs/collection.log for details
echo ============================================================
pause
exit /b 0

:error
echo ============================================================
echo Data collection encountered errors - check logs
echo ============================================================
pause
exit /b 1
