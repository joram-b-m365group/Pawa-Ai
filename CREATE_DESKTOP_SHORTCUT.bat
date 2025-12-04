@echo off
REM Creates a desktop shortcut for Genius AI

echo Creating Desktop Shortcut for Genius AI...
echo.

set SCRIPT="%TEMP%\CreateShortcut.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") >> %SCRIPT%
echo sLinkFile = "%USERPROFILE%\Desktop\Genius AI.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "%~dp0START_GENIUS_AI_SILENT.vbs" >> %SCRIPT%
echo oLink.WorkingDirectory = "%~dp0" >> %SCRIPT%
echo oLink.Description = "Start Genius AI" >> %SCRIPT%
echo oLink.IconLocation = "%SystemRoot%\System32\shell32.dll,13" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%

cscript //nologo %SCRIPT%
del %SCRIPT%

echo.
echo ======================================================================
echo   Desktop shortcut created successfully!
echo ======================================================================
echo.
echo   Look for "Genius AI" icon on your desktop.
echo   Double-click it to start Genius AI anytime!
echo.
pause
