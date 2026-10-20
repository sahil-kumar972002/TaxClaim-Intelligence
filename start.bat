@echo off
title TaxClaim AI Launcher
echo ========================================================
echo        TAXCLAIM AI - 1-CLICK LAUNCHER
echo ========================================================
echo.

cd /d "%~dp0"

echo [1/3] Checking Backend environment...
cd backend
if not exist .venv (
    echo Creating Python virtual environment...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    echo Installing backend dependencies...
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

echo Starting FastAPI Backend server on port 8000...
start "TaxClaim Backend" cmd /k "call .venv\Scripts\activate.bat && python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload"

cd ..\frontend

echo [2/3] Checking Frontend environment...
if not exist node_modules (
    echo Installing node dependencies...
    call npm install
)

echo Starting Vite Frontend Command Center on port 5173...
start "TaxClaim Frontend" cmd /k "npm run dev -- --host 127.0.0.1 --port 5173"

echo.
echo [3/3] Opening Browser...
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo ========================================================
echo  TaxClaim AI is now running!
echo  - Frontend UI:  http://localhost:5173
echo  - Swagger Docs: http://localhost:8000/docs
echo ========================================================
echo Keep this window or the spawned windows open to keep servers active.
pause
