#!/usr/bin/env bash
# Caption Composer - Unix/Linux/Mac Run Script
# Run this script to start the trading intelligence tool

echo ""
echo "========================================"
echo "  Caption Composer - TradeGPT-Aladdin"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ -d ".venv" ]; then
    echo "[*] Activating virtual environment..."
    source .venv/bin/activate
    echo "[✓] Virtual environment activated"
    echo ""
else
    echo "[!] No virtual environment found at .venv"
    echo "[*] Using system Python..."
    echo ""
fi

# Check if dependencies are installed
python3 -c "import yfinance, pandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[!] Missing dependencies detected"
    echo "[*] Installing yfinance and pandas..."
    pip3 install yfinance pandas
    echo ""
fi

# Run the caption composer
echo "[*] Starting Caption Composer..."
echo ""
python3 caption_composer.py

# Check exit code
if [ $? -ne 0 ]; then
    echo ""
    echo "[!] An error occurred."
    read -p "Press Enter to exit..."
fi
