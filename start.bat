@echo off
REM EQUIS SAR Generator - Startup Script for Windows
REM This script starts both the backend and frontend servers

echo =========================================
echo   EQUIS SAR Generator - Starting...     
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed.
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed.
    echo Please install Node.js 16 or higher from https://nodejs.org/
    pause
    exit /b 1
)

echo √ Python and Node.js found
echo.

REM Start backend
echo Starting backend server...
cd backend

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo √ Virtual environment activated
) else (
    echo Warning: Virtual environment not found. Creating one...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo √ Virtual environment created and activated
    echo Installing backend dependencies...
    pip install -r requirements.txt
)

REM Start backend
echo Launching backend on http://localhost:8000
start "EQUIS Backend" python main.py

cd ..

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend
echo.
echo Starting frontend server...
cd frontend

REM Check if node_modules exists
if not exist node_modules (
    echo Warning: node_modules not found. Installing dependencies...
    call npm install
)

echo Launching frontend on http://localhost:5173
start "EQUIS Frontend" npm run dev

cd ..

echo.
echo =========================================
echo   √ EQUIS SAR Generator is running!     
echo =========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Open http://localhost:5173 in your browser to use the app.
echo.
echo To stop the servers, close both terminal windows.
echo.
pause
