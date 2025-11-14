@echo off
echo ========================================
echo Trading Analytics System - Quick Setup
echo ========================================
echo.

echo [1/3] Setting up Backend...
cd backend

if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo ✅ Created .env - Please edit it with your API keys
) else (
    echo ✅ .env already exists
)

echo.
echo [2/3] Installing Python dependencies...
pip install -r requirements.txt

cd ..

echo.
echo [3/3] Setting up Frontend...
cd frontend

if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo ✅ Created .env
) else (
    echo ✅ .env already exists
)

echo.
echo Installing Node dependencies...
call npm install

cd ..

echo.
echo ========================================
echo ✅ Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Add your credentials.json to the backend folder
echo 2. Edit backend/.env with your API keys
echo 3. Run start.bat to start the application
echo.
pause
