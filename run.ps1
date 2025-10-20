# Caption Composer - PowerShell Run Script
# Run this script to start the trading intelligence tool

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Caption Composer - TradeGPT-Aladdin" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "[*] Activating virtual environment..." -ForegroundColor Yellow
    & ".venv\Scripts\Activate.ps1"
    Write-Host "[✓] Virtual environment activated" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "[!] No virtual environment found at .venv" -ForegroundColor Red
    Write-Host "[*] Using system Python..." -ForegroundColor Yellow
    Write-Host ""
}

# Check if dependencies are installed
try {
    python -c "import yfinance, pandas" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Dependencies missing"
    }
} catch {
    Write-Host "[!] Missing dependencies detected" -ForegroundColor Red
    Write-Host "[*] Installing yfinance and pandas..." -ForegroundColor Yellow
    pip install yfinance pandas
    Write-Host ""
}

# Run the caption composer
Write-Host "[*] Starting Caption Composer..." -ForegroundColor Yellow
Write-Host ""
python caption_composer.py

# Check exit code
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[!] An error occurred." -ForegroundColor Red
    Read-Host "Press Enter to exit"
}
