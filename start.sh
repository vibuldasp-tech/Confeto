#!/bin/bash

# EQUIS SAR Generator - Startup Script
# This script starts both the backend and frontend servers

echo "========================================="
echo "  EQUIS SAR Generator - Starting...     "
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.8 or higher from https://www.python.org/"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed."
    echo "Please install Node.js 16 or higher from https://nodejs.org/"
    exit 1
fi

echo "✓ Python and Node.js found"
echo ""

# Start backend
echo "Starting backend server..."
cd backend

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "⚠ Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ Virtual environment created and activated"
    echo "Installing backend dependencies..."
    pip install -r requirements.txt
fi

# Start backend in background
echo "Launching backend on http://localhost:8000"
python main.py &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

cd ..

# Wait a bit for backend to start
sleep 3

# Start frontend
echo ""
echo "Starting frontend server..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "⚠ node_modules not found. Installing dependencies..."
    npm install
fi

echo "Launching frontend on http://localhost:5173"
npm run dev &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

cd ..

echo ""
echo "========================================="
echo "  ✓ EQUIS SAR Generator is running!     "
echo "========================================="
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Open http://localhost:5173 in your browser to use the app."
echo ""
echo "To stop the servers, press Ctrl+C"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "Servers stopped."
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Wait for processes
wait
