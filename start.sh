#!/usr/bin/env bash
set -e

echo "========================================================"
echo "       TAXCLAIM AI - 1-COMMAND LAUNCHER (UNIX)         "
echo "========================================================"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[1/3] Setting up Backend..."
cd "$ROOT_DIR/backend"
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

echo "Starting FastAPI Backend server on port 8000..."
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!

echo "[2/3] Setting up Frontend..."
cd "$ROOT_DIR/frontend"
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

echo "Starting Vite Frontend Command Center on port 5173..."
npm run dev -- --host 127.0.0.1 --port 5173 &
FRONTEND_PID=$!

echo ""
echo "[3/3] Ready! Access URLs:"
echo " - Frontend UI:  http://localhost:5173"
echo " - Swagger Docs: http://localhost:8000/docs"
echo "========================================================"
echo "Press CTRL+C to stop both servers."

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true; exit" SIGINT SIGTERM
wait
