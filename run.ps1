# SwasthAI Chat MVP - Run Script

Write-Host "🏥 Starting SwasthAI Chat MVP..." -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "⚠️  Virtual environment not found!" -ForegroundColor Red
    Write-Host "   Please run setup.ps1 first" -ForegroundColor Yellow
    exit 1
}

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found!" -ForegroundColor Red
    Write-Host "   Please copy .env.example to .env and add your API key" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

# Run the application
Write-Host "🚀 Launching SwasthAI Chat..." -ForegroundColor Green
Write-Host ""
Write-Host "📱 Open your browser and navigate to:" -ForegroundColor Yellow
Write-Host "   http://localhost:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

python main.py
