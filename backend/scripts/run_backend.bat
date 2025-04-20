@echo off
setlocal enabledelayedexpansion

echo [32mStarting Backend Server...[0m

:: Kiểm tra Python đã được cài đặt chưa
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [31mError: Python is not installed or not in PATH[0m
    pause
    exit /b 1
)

:: Kiểm tra thư mục backend có tồn tại không
if not exist backend (
    echo [31mError: backend directory not found[0m
    pause
    exit /b 1
)

cd backend

:: Kiểm tra virtual environment
if not exist venv (
    echo [33mCreating virtual environment...[0m
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate.bat
if %ERRORLEVEL% neq 0 (
    echo [31mError: Failed to activate virtual environment[0m
    pause
    exit /b 1
)

:: Kiểm tra các package cần thiết
echo [33mChecking required packages...[0m
pip install fastapi uvicorn loguru vnstock pydantic-settings python-dotenv

:: Kill any existing process on port 8000
echo [33mChecking for existing processes on port 8000...[0m
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do (
    echo [33mKilling process with PID: %%a[0m
    taskkill /F /PID %%a 2>nul
)

:: Kiểm tra main.py có tồn tại không
if not exist main.py (
    echo [31mError: main.py not found in backend directory[0m
    pause
    exit /b 1
)

:: Start backend server
echo [32mStarting FastAPI server on http://localhost:8000[0m
echo [33mPress Ctrl+C to stop the server[0m
python main.py

pause 