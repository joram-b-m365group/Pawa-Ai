@echo off
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                                                               ║
echo ║           🧠 ULTIMATE GENIUS AI SYSTEM 🧠                     ║
echo ║                                                               ║
echo ║  Multi-Agent Intelligence ^| Long-Term Memory ^| Learning       ║
echo ║                                                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo Starting the Ultimate AI System...
echo.

REM Check if Ollama is running
ollama list >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Ollama is not running!
    echo.
    echo Please:
    echo 1. Install Ollama from https://ollama.com/download
    echo 2. Open Ollama application
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)

echo ✓ Ollama is running
echo.

REM Check if LLaMA model is downloaded
ollama list | findstr "llama3.2" >nul
if %errorlevel% neq 0 (
    echo ⚠️  LLaMA 3.2 model not found!
    echo.
    echo Downloading model (this will take 2-3 minutes)...
    ollama pull llama3.2
)

echo ✓ LLaMA 3.2 model ready
echo.

REM Start Docker containers
echo Starting Ultimate AI system...
docker-compose -f docker-compose-ultimate.yml up --build -d

if %errorlevel% equ 0 (
    echo.
    echo ╔═══════════════════════════════════════════════════════════════╗
    echo ║                                                               ║
    echo ║                  ✅ SYSTEM READY! ✅                           ║
    echo ║                                                               ║
    echo ╚═══════════════════════════════════════════════════════════════╝
    echo.
    echo 🚀 Your Ultimate AI is now running!
    echo.
    echo 📱 Open your web interface:
    echo    web-app\index.html
    echo.
    echo 📚 API Documentation:
    echo    http://localhost:8000/docs
    echo.
    echo 💡 Features:
    echo    ✓ 5 Specialized Agents (Reasoning, Math, Vision, Code, Creative^)
    echo    ✓ Long-term memory
    echo    ✓ Continuous learning
    echo    ✓ Model fine-tuning
    echo    ✓ Human-like conversation
    echo    ✓ $0 cost - completely FREE!
    echo.
    echo 📖 Full guide: ULTIMATE_AI_README.md
    echo.
    echo Opening web interface...
    start "" "%CD%\web-app\index.html"
    echo.
) else (
    echo.
    echo ❌ Failed to start system
    echo.
    echo Please check:
    echo 1. Docker Desktop is running
    echo 2. No other service is using port 8000
    echo.
)

pause
