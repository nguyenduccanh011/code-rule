@echo off
echo Activating virtual environment...
call .\backend\venv\Scripts\activate.bat

echo Starting backend server...
cd backend
uvicorn app.main:app --reload

pause 