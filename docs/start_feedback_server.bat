@echo off
echo.
echo Starting LLM Data Explorer Feedback System
echo ==============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3 from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet

if errorlevel 1 (
    echo Error installing dependencies
    pause
    exit /b 1
)

echo Dependencies installed
echo.

REM Start the server
echo Starting Flask API server...
echo    API: http://localhost:5000
echo    Dashboard: Open admin_dashboard.html in your browser
echo.
echo Press Ctrl+C to stop the server
echo ==============================================
echo.

python feedback_api.py
pause
