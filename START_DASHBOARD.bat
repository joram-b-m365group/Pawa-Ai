@echo off
echo ======================================================================
echo GENIUS AI - Dashboard
echo ======================================================================
echo.
echo Starting dashboard server...
echo.
echo Dashboard will open automatically in your browser!
echo URL: http://localhost:8000/frontend/dashboard.html
echo.
echo Press Ctrl+C to stop the server
echo ======================================================================
echo.

cd /d C:\Users\Jorams\genius-ai
/c/Users/Jorams/anaconda3/python.exe start_dashboard.py

pause
