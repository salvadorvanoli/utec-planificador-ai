# Start UTEC Planificador AI Agent V2 (PowerShell)
Write-Host "================================================" -ForegroundColor Cyan
Write-Host " UTEC Planificador AI Agent V2" -ForegroundColor Green
Write-Host " Starting application..." -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Change to project root
Set-Location (Split-Path $PSScriptRoot)

# Check if .env exists
if (-not (Test-Path .env)) {
    Write-Host "[WARNING] .env file not found!" -ForegroundColor Yellow
    Write-Host "Please copy .env.example to .env and configure your OPENAI_KEY" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if virtual environment exists
if (-not (Test-Path .venv)) {
    Write-Host "[INFO] Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "[INFO] Virtual environment created." -ForegroundColor Green
    Write-Host ""
}

# Activate virtual environment
Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1

# Install/Update dependencies
Write-Host "[INFO] Installing dependencies..." -ForegroundColor Cyan
pip install . --quiet
Write-Host ""

# Start the application (DB initializes automatically)
Write-Host "[INFO] Starting server on http://localhost:8000" -ForegroundColor Green
Write-Host "[INFO] Database will initialize automatically on first run" -ForegroundColor Cyan
Write-Host "[INFO] Press CTRL+C to stop" -ForegroundColor Yellow
Write-Host ""
python -m uvicorn app.main_v2:app --reload --host 0.0.0.0 --port 8000

