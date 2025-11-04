# SwasthAI Chat MVP - Quick Setup Script for Windows PowerShell

Write-Host "🏥 SwasthAI Chat MVP - Setup Script" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "✓ Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found! Please install Python 3.8 or higher" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "✓ Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  Virtual environment already exists" -ForegroundColor Green
} else {
    python -m venv venv
    Write-Host "  Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "✓ Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "  Virtual environment activated" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "✓ Installing dependencies..." -ForegroundColor Yellow
Write-Host "  This may take a few minutes..." -ForegroundColor Gray
pip install -r requirements.txt --quiet
Write-Host "  Dependencies installed" -ForegroundColor Green

# Setup .env file
Write-Host ""
Write-Host "✓ Setting up environment variables..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  .env file already exists" -ForegroundColor Green
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "  .env file created from template" -ForegroundColor Green
    Write-Host ""
    Write-Host "  ⚠️  IMPORTANT: Edit .env file and add your API key!" -ForegroundColor Red
    Write-Host "     - For OpenAI: Get key from https://platform.openai.com/api-keys" -ForegroundColor Gray
    Write-Host "     - For Gemini (Free): Get key from https://makersuite.google.com/app/apikey" -ForegroundColor Gray
}

# Summary
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file and add your API key" -ForegroundColor White
Write-Host "2. Run: python main.py" -ForegroundColor White
Write-Host "3. Open: http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "Happy Coding! 🚀" -ForegroundColor Cyan
