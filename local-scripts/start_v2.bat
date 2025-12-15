@echo off
REM Start UTEC Planificador AI Agent V2 (Windows CMD)
echo ================================================
echo  UTEC Planificador AI Agent V2
echo  Starting application...
echo ================================================
echo.

REM Change to project root
cd /d "%~dp0.."

REM Check if .env exists
if not exist .env (
    echo [WARNING] .env file not found!
    echo Please copy .env.example to .env and configure your OPENAI_KEY
    echo.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist .venv (
    echo [INFO] Virtual environment not found. Creating...
    python -m venv .venv
    echo [INFO] Virtual environment created.
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install/update dependencies
echo [INFO] Installing dependencies...
pip install .

REM Start the server
echo.
echo [INFO] Starting server on http://localhost:8000
echo [INFO] Press CTRL+C to stop
echo.
python -m uvicorn app.main_v2:app --reload --host 0.0.0.0 --port 8000

