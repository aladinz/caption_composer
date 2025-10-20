@echo off
REM Caption Composer - Windows Run Script
REM Run this script to start the trading intelligence tool

echo.
echo ========================================
echo   Caption Composer - TradeGPT-Aladdin
echo ========================================
echo.

REM Check if virtual environment exists
if exist ".venv\Scripts\activate.bat" (
    echo [*] Activating virtual environment...
    call .venv\Scripts\activate.bat
    echo [✓] Virtual environment activated
    echo.
) else (
    echo [!] No virtual environment found at .venv
    echo [*] Using system Python...
    echo.
)

REM Check if dependencies are installed
python -c "import yfinance, pandas" 2>nul
if errorlevel 1 (
    echo [!] Missing dependencies detected
    echo [*] Installing yfinance and pandas...
    pip install yfinance pandas
    echo.
)

REM Run the caption composer
echo [*] Starting Caption Composer...
echo.
python caption_composer.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo [!] An error occurred. Press any key to exit...
    pause >nul
)
