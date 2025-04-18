@echo off
setlocal enabledelayedexpansion

:: Colors for output
set "GREEN=[32m"
set "YELLOW=[33m"
set "RED=[31m"
set "NC=[0m"

echo %GREEN%Starting Stock Platform Setup...%NC%

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo %RED%Python is not installed. Please install Python 3.11+ first.%NC%
    exit /b 1
)

:: Check if Node.js is installed
node --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo %RED%Node.js is not installed. Please install Node.js 18+ first.%NC%
    exit /b 1
)

:: Create necessary directories
echo %YELLOW%Creating project directories...%NC%
mkdir backend\data\raw 2>nul
mkdir backend\data\processed 2>nul
mkdir backend\data\cache 2>nul
mkdir frontend\public 2>nul
mkdir logs 2>nul

:: Create .env files if they don't exist
echo %YELLOW%Setting up environment files...%NC%
if not exist backend\.env (
    (
        echo DATABASE_URL=mysql://username:password@localhost:3306/stock_platform
        echo SECRET_KEY=your-secret-key-here
        echo ALGORITHM=HS256
        echo ACCESS_TOKEN_EXPIRE_MINUTES=30
    ) > backend\.env
)

if not exist frontend\.env (
    (
        echo NEXT_PUBLIC_API_URL=http://localhost:8000
    ) > frontend\.env
)

:: Create and activate Python virtual environment
echo %YELLOW%Setting up Python environment...%NC%
cd backend
python -m venv venv
call venv\Scripts\activate.bat

:: Install Python dependencies
echo %YELLOW%Installing Python dependencies...%NC%
pip install -r requirements.txt

:: Run database migrations
echo %YELLOW%Running database migrations...%NC%
alembic upgrade head

:: Start backend server
echo %YELLOW%Starting backend server...%NC%
start /B uvicorn main:app --reload --host 0.0.0.0 --port 8000

:: Setup frontend
echo %YELLOW%Setting up frontend...%NC%
cd ..\frontend
call npm install

:: Start frontend development server
echo %YELLOW%Starting frontend development server...%NC%
start /B npm run dev

echo %GREEN%Setup completed!%NC%
echo %GREEN%Backend is running at: http://localhost:8000%NC%
echo %GREEN%Frontend is running at: http://localhost:3000%NC%
echo %GREEN%API documentation is available at: http://localhost:8000/docs%NC%
echo %GREEN%Database can be managed at: http://localhost/phpmyadmin%NC%

:: Keep the script running
pause 