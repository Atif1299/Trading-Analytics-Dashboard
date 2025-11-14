@echo off
echo ========================================
echo Starting Trading Analytics System
echo ========================================
echo.

echo Starting Backend Server...
start cmd /k "cd backend && python main.py"

timeout /t 3 /nobreak > nul

echo Starting Frontend Server...
start cmd /k "cd frontend && npm run dev"

echo.
echo ✅ Both servers are starting!
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Close this window to keep servers running
pause
