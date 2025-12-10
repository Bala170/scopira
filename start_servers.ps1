Write-Host "========================================" -ForegroundColor Green
Write-Host "Scopira Development Server Startup" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "Starting Backend Server (Flask API)..." -ForegroundColor Yellow
Write-Host "Please wait while the backend initializes..." -ForegroundColor Yellow
Write-Host ""

$backendPath = Join-Path $PSScriptRoot "backend"
$frontendPath = Join-Path $PSScriptRoot "frontend"

# Kill any existing Python processes on our ports
try {
    Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object {
        $_.MainWindowTitle -like "*Scopira*" -or $_.Id -in @(
            (Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue).OwningProcess,
            (Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue).OwningProcess
        )
    } | Stop-Process -Force -ErrorAction SilentlyContinue
} catch {}

# Start backend server
Start-Process -WindowStyle Normal -WorkingDirectory $backendPath -FilePath "python" -ArgumentList "app_simple.py"

Write-Host "Waiting 3 seconds for backend to start..." -ForegroundColor Cyan
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "Starting Frontend Server (HTTP Server)..." -ForegroundColor Yellow

# Start frontend server
Start-Process -WindowStyle Normal -WorkingDirectory $frontendPath -FilePath "python" -ArgumentList "-m", "http.server", "8000"

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Both servers are starting up!" -ForegroundColor Green
Write-Host ""
Write-Host "Backend API: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Frontend:    http://localhost:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Profile Page: http://localhost:8000/profile.html" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Test connections
Write-Host "Testing connections..." -ForegroundColor Yellow

try {
    $backendTest = Invoke-RestMethod -Uri "http://localhost:5000/" -Method GET -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✓ Backend API is responding" -ForegroundColor Green
} catch {
    Write-Host "✗ Backend API connection failed" -ForegroundColor Red
    Write-Host "  Make sure Python Flask is working" -ForegroundColor Red
}

try {
    $frontendTest = Invoke-WebRequest -Uri "http://localhost:8000/" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✓ Frontend server is responding" -ForegroundColor Green
} catch {
    Write-Host "✗ Frontend server connection failed" -ForegroundColor Red
    Write-Host "  Make sure Python HTTP server is working" -ForegroundColor Red
}

Write-Host ""
Write-Host "Opening profile page in browser..." -ForegroundColor Cyan
Start-Process "http://localhost:8000/profile.html"

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")