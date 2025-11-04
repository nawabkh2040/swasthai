# SwasthAI Chat MVP - Verification Script
# This script checks if all required files and configurations are in place

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   SwasthAI Chat MVP - Installation Verification   ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Function to check file exists
function Test-FileExists {
    param($path, $description)
    if (Test-Path $path) {
        Write-Host "✓ $description" -ForegroundColor Green
        return $true
    } else {
        Write-Host "✗ $description - MISSING" -ForegroundColor Red
        return $false
    }
}

# Check Python installation
Write-Host "Checking Prerequisites..." -ForegroundColor Yellow
Write-Host "─────────────────────────" -ForegroundColor Gray
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python 3\.([8-9]|1[0-9])") {
        Write-Host "✓ Python $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "✗ Python 3.8+ required (found: $pythonVersion)" -ForegroundColor Red
        $allGood = $false
    }
} catch {
    Write-Host "✗ Python not found" -ForegroundColor Red
    $allGood = $false
}
Write-Host ""

# Check Core Python Files
Write-Host "Checking Core Backend Files..." -ForegroundColor Yellow
Write-Host "──────────────────────────────" -ForegroundColor Gray
$coreFiles = @(
    @{path="main.py"; desc="Main FastAPI application"},
    @{path="config.py"; desc="Configuration settings"},
    @{path="database.py"; desc="Database models"},
    @{path="auth.py"; desc="Authentication system"},
    @{path="schemas.py"; desc="Pydantic schemas"},
    @{path="ai_agent.py"; desc="AI agent (LangChain + LangGraph)"}
)

foreach ($file in $coreFiles) {
    if (-not (Test-FileExists $file.path $file.desc)) {
        $allGood = $false
    }
}
Write-Host ""

# Check Templates
Write-Host "Checking Frontend Templates..." -ForegroundColor Yellow
Write-Host "──────────────────────────────" -ForegroundColor Gray
$templates = @(
    @{path="templates/index.html"; desc="Home page"},
    @{path="templates/signup.html"; desc="Signup page"},
    @{path="templates/login.html"; desc="Login page"},
    @{path="templates/chat.html"; desc="Chat page"}
)

foreach ($template in $templates) {
    if (-not (Test-FileExists $template.path $template.desc)) {
        $allGood = $false
    }
}
Write-Host ""

# Check Static Files
Write-Host "Checking Static Assets..." -ForegroundColor Yellow
Write-Host "─────────────────────────" -ForegroundColor Gray
$staticFiles = @(
    @{path="static/css/style.css"; desc="Main stylesheet"},
    @{path="static/js/signup.js"; desc="Signup JavaScript"},
    @{path="static/js/login.js"; desc="Login JavaScript"},
    @{path="static/js/chat.js"; desc="Chat JavaScript"}
)

foreach ($file in $staticFiles) {
    if (-not (Test-FileExists $file.path $file.desc)) {
        $allGood = $false
    }
}
Write-Host ""

# Check Configuration Files
Write-Host "Checking Configuration Files..." -ForegroundColor Yellow
Write-Host "───────────────────────────────" -ForegroundColor Gray
if (-not (Test-FileExists "requirements.txt" "Python dependencies")) {
    $allGood = $false
}
if (-not (Test-FileExists ".env.example" "Environment template")) {
    $allGood = $false
}
if (-not (Test-FileExists ".gitignore" "Git ignore file")) {
    $allGood = $false
}
Write-Host ""

# Check Documentation
Write-Host "Checking Documentation..." -ForegroundColor Yellow
Write-Host "─────────────────────────" -ForegroundColor Gray
$docs = @(
    @{path="README.md"; desc="Main documentation"},
    @{path="QUICKSTART.md"; desc="Quick start guide"},
    @{path="DEPLOYMENT.md"; desc="Deployment guide"},
    @{path="PROJECT_SUMMARY.md"; desc="Project summary"},
    @{path="CHECKLIST.md"; desc="Development checklist"},
    @{path="ARCHITECTURE.md"; desc="Architecture diagrams"}
)

foreach ($doc in $docs) {
    if (-not (Test-FileExists $doc.path $doc.desc)) {
        $allGood = $false
    }
}
Write-Host ""

# Check Scripts
Write-Host "Checking Utility Scripts..." -ForegroundColor Yellow
Write-Host "───────────────────────────" -ForegroundColor Gray
if (-not (Test-FileExists "setup.ps1" "Setup script")) {
    $allGood = $false
}
if (-not (Test-FileExists "run.ps1" "Run script")) {
    $allGood = $false
}
Write-Host ""

# Check Environment Configuration
Write-Host "Checking Environment Setup..." -ForegroundColor Yellow
Write-Host "─────────────────────────────" -ForegroundColor Gray
if (Test-Path ".env") {
    Write-Host "✓ .env file exists" -ForegroundColor Green
    
    # Check if API key is configured
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "OPENAI_API_KEY=sk-" -or $envContent -match "GOOGLE_API_KEY=.{30,}") {
        Write-Host "✓ API key appears to be configured" -ForegroundColor Green
    } else {
        Write-Host "⚠ API key might not be configured" -ForegroundColor Yellow
        Write-Host "  Please ensure you've added your OPENAI_API_KEY or GOOGLE_API_KEY" -ForegroundColor Gray
    }
} else {
    Write-Host "⚠ .env file not found (copy from .env.example)" -ForegroundColor Yellow
    Write-Host "  Run: copy .env.example .env" -ForegroundColor Gray
}
Write-Host ""

# Check Virtual Environment
Write-Host "Checking Virtual Environment..." -ForegroundColor Yellow
Write-Host "───────────────────────────────" -ForegroundColor Gray
if (Test-Path "venv") {
    Write-Host "✓ Virtual environment exists" -ForegroundColor Green
    
    # Check if activated
    if ($env:VIRTUAL_ENV) {
        Write-Host "✓ Virtual environment is activated" -ForegroundColor Green
    } else {
        Write-Host "⚠ Virtual environment not activated" -ForegroundColor Yellow
        Write-Host "  Run: .\venv\Scripts\activate" -ForegroundColor Gray
    }
} else {
    Write-Host "⚠ Virtual environment not found" -ForegroundColor Yellow
    Write-Host "  Run: python -m venv venv" -ForegroundColor Gray
}
Write-Host ""

# Check if dependencies are installed
if (Test-Path "venv") {
    Write-Host "Checking Installed Dependencies..." -ForegroundColor Yellow
    Write-Host "──────────────────────────────────" -ForegroundColor Gray
    
    $pipList = & ".\venv\Scripts\pip.exe" list 2>&1
    
    $requiredPackages = @("fastapi", "uvicorn", "sqlalchemy", "langchain", "openai", "pydantic")
    $installedCount = 0
    
    foreach ($package in $requiredPackages) {
        if ($pipList -match $package) {
            $installedCount++
        }
    }
    
    if ($installedCount -eq $requiredPackages.Length) {
        Write-Host "✓ All required packages appear to be installed" -ForegroundColor Green
    } else {
        Write-Host "⚠ Some packages might be missing ($installedCount/$($requiredPackages.Length))" -ForegroundColor Yellow
        Write-Host "  Run: pip install -r requirements.txt" -ForegroundColor Gray
    }
    Write-Host ""
}

# Project Statistics
Write-Host "Project Statistics..." -ForegroundColor Yellow
Write-Host "────────────────────" -ForegroundColor Gray

$pythonFiles = (Get-ChildItem -Path . -Filter *.py -File).Count
$htmlFiles = (Get-ChildItem -Path templates -Filter *.html -File -ErrorAction SilentlyContinue).Count
$jsFiles = (Get-ChildItem -Path static/js -Filter *.js -File -ErrorAction SilentlyContinue).Count
$cssFiles = (Get-ChildItem -Path static/css -Filter *.css -File -ErrorAction SilentlyContinue).Count
$mdFiles = (Get-ChildItem -Path . -Filter *.md -File).Count

Write-Host "  Python files: $pythonFiles" -ForegroundColor Cyan
Write-Host "  HTML files: $htmlFiles" -ForegroundColor Cyan
Write-Host "  JavaScript files: $jsFiles" -ForegroundColor Cyan
Write-Host "  CSS files: $cssFiles" -ForegroundColor Cyan
Write-Host "  Documentation files: $mdFiles" -ForegroundColor Cyan
Write-Host ""

# Final Summary
Write-Host "╔════════════════════════════════════════════════════╗" -ForegroundColor Cyan
if ($allGood) {
    Write-Host "║              ✓ VERIFICATION PASSED                ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🎉 All required files are in place!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Ensure .env file is configured with API key" -ForegroundColor White
    Write-Host "2. Install dependencies: pip install -r requirements.txt" -ForegroundColor White
    Write-Host "3. Run the application: python main.py" -ForegroundColor White
    Write-Host "4. Open browser: http://localhost:8000" -ForegroundColor White
    Write-Host ""
    Write-Host "Quick Start: .\run.ps1" -ForegroundColor Cyan
} else {
    Write-Host "║              ✗ VERIFICATION FAILED                ║" -ForegroundColor Red
    Write-Host "╚════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "⚠️  Some files are missing. Please check the errors above." -ForegroundColor Red
    Write-Host ""
    Write-Host "Try running: .\setup.ps1" -ForegroundColor Yellow
}
Write-Host ""
Write-Host "For detailed instructions, see: README.md or QUICKSTART.md" -ForegroundColor Gray
Write-Host ""
