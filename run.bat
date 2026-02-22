@echo off

echo Checking if Ollama is running...
curl -s http://localhost:11434 >nul 2>&1
if errorlevel 1 (
    echo [error] Ollama is not running. Please start Ollama first.
    echo Download from: https://ollama.com/download
    pause
    exit /b 1
)

pip install -r requirements.txt --quiet

echo.
set /p project_path="Enter the path to the project you want to analyze: "
set /p question="Enter your question (or press Enter for default analysis): "

if "%question%"=="" (
    python main.py %project_path%
) else (
    python main.py %project_path% --ask "%question%"
)
