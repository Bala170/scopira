@echo off
echo ========================================
echo Scopira Development Server Startup
echo ========================================
echo.

echo Starting Backend Server (Flask API)...
echo Please wait while the backend initializes...
echo.

cd /d "%~dp0backend"
start "Scopira Backend" cmd /c "python app_simple.py & pause"

echo Waiting 3 seconds for backend to start...
timeout /t 3 /nobreak >nul

echo.
echo Starting Frontend Server (HTTP Server)...
cd /d "%~dp0frontend"
start "Scopira Frontend" cmd /c "python -m http.server 8000 & pause"

echo.
echo ========================================
echo Both servers are starting up!
echo.
echo Backend API: http://localhost:5000
echo Frontend:    http://localhost:8000
echo.
echo Profile Page: http://localhost:8000/profile.html
echo ========================================
echo.
echo Press any key to continue...
pause >nul