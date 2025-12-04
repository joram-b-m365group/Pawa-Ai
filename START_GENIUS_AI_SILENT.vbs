' Genius AI - Silent Launcher (No Terminal Windows)
' Double-click this file to start Genius AI without any terminal windows

Set WshShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
scriptDir = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Kill any existing processes
WshShell.Run "powershell -WindowStyle Hidden -Command ""Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object {$_.Path -like '*working_vision_endpoint*'} | Stop-Process -Force""", 0, True
WshShell.Run "powershell -WindowStyle Hidden -Command ""Get-Process -Name node -ErrorAction SilentlyContinue | Where-Object {$_.CommandLine -like '*vite*'} | Stop-Process -Force""", 0, True

' Wait a moment
WScript.Sleep 2000

' Start Super Intelligent Backend (hidden)
backendCmd = "cmd /c cd /d """ & scriptDir & "\backend"" && C:\Users\Jorams\anaconda3\python.exe super_intelligent_endpoint.py"
WshShell.Run backendCmd, 0, False

' Wait for backend to start
WScript.Sleep 5000

' Start Frontend (hidden)
frontendCmd = "cmd /c cd /d """ & scriptDir & "\frontend"" && npm run dev"
WshShell.Run frontendCmd, 0, False

' Wait for frontend to start
WScript.Sleep 8000

' Open browser
WshShell.Run "http://localhost:3000", 1, False

' Show success message
MsgBox "Genius AI is now running!" & vbCrLf & vbCrLf & _
       "Frontend: http://localhost:3000" & vbCrLf & _
       "Backend:  http://localhost:8000" & vbCrLf & vbCrLf & _
       "To stop, run STOP_GENIUS_AI.bat", _
       vbInformation, "Genius AI Started"
