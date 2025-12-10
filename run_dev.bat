@echo off
echo ============================================
echo Starting Scopira Development Servers
echo ============================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo Starting Flask Backend Server on port 5000...
start "Scopira Backend" cmd /k "cd /d %~dp0backend && python app.py"

:: Wait for backend to start
timeout /t 3 /nobreak >nul

echo Starting Frontend Server on port 8000...
start "Scopira Frontend" cmd /k "cd /d %~dp0frontend && python server.py"

echo.
echo ============================================
echo Development servers started!
echo ============================================
echo.
echo Frontend: http://localhost:8000
echo Backend API: http://localhost:5000
echo.
echo Close the terminal windows to stop the servers.
echo.
pause