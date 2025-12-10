#!/bin/bash
# Start UTEC Planificador AI Agent V2

echo "================================================"
echo " UTEC Planificador AI Agent V2"
echo " Starting application..."
echo "================================================"
echo ""

# Change to project root
cd "$(dirname "$0")/.."

# Check if .env exists
if [ ! -f .env ]; then
    echo "[WARNING] .env file not found!"
    echo "Please copy .env.example to .env and configure your OPENAI_KEY"
    echo ""
    exit 1
fi

# Check if virtual environment exists
if [ ! -d .venv ]; then
    echo "[INFO] Virtual environment not found. Creating..."
    python3 -m venv .venv
    echo "[INFO] Virtual environment created."
    echo ""
fi

# Activate virtual environment
source .venv/bin/activate

# Install/Update dependencies
echo "[INFO] Installing dependencies..."
pip install -r requirements.txt --quiet
echo ""

# Start the application (DB initializes automatically)
echo "[INFO] Starting server on http://localhost:8000"
echo "[INFO] Database will initialize automatically on first run"
echo "[INFO] Press CTRL+C to stop"
echo ""
python -m uvicorn app.main_v2:app --reload --host 0.0.0.0 --port 8000
echo ""
uvicorn app.main_v2:app --reload --host 0.0.0.0 --port 8000
@echo off
REM Start UTEC Planificador AI Agent V2

echo ================================================
echo  UTEC Planificador AI Agent V2
echo  Starting application...
echo ================================================
echo.

REM Check if .env exists
if not exist .env (
    echo [WARNING] .env file not found!
    echo Please copy .env.example to .env and configure your OPENAI_KEY
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist venv (
    echo [INFO] Virtual environment not found. Creating...
    python -m venv venv
    echo [INFO] Virtual environment created.
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install/Update dependencies
echo [INFO] Installing dependencies...
pip install -e . --quiet
echo.

REM Initialize database
echo [INFO] Initializing database...
python scripts\migrate_to_v2.py
echo.

REM Start the application
echo [INFO] Starting server on http://localhost:8000
echo [INFO] Press CTRL+C to stop
echo.
uvicorn app.main_v2:app --reload --host 0.0.0.0 --port 8000

