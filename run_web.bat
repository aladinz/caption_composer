@echo off
REM Caption Composer - Web Interface Launcher
REM Run this script to start the web server

echo.
echo ==========================================
echo   Caption Composer - Web Interface
echo   TradeGPT-Aladdin Trading Intelligence
echo ==========================================
echo.

REM Check if virtual environment exists
if exist ".venv\Scripts\activate.bat" (
    echo [*] Activating virtual environment...
    call .venv\Scripts\activate.bat
    echo [√] Virtual environment activated
    echo.
) else (
    echo [!] No virtual environment found at .venv
    echo [*] Using system Python...
    echo.
)

REM Check if Flask is installed
python -c "import flask, flask_cors" 2>nul
if errorlevel 1 (
    echo [!] Flask dependencies not found
    echo [*] Installing Flask and flask-cors...
    pip install flask flask-cors
    echo.
)

REM Start the web server
echo [*] Starting web server...
echo.
echo ==========================================
echo   Web Interface: http://localhost:5000
echo   Press Ctrl+C to stop the server
echo ==========================================
echo.

python app.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo [!] An error occurred. Press any key to exit...
    pause >nul
)
