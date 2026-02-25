# test_setup.ps1
# Windows Setup Verification Script for DJ Set Curator

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  DJ Set Curator - Setup Verification" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

$allGood = $true

# Check Python
Write-Host "`n[1/7] Checking Python..." -ForegroundColor Yellow
$pythonCheck = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCheck) {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Python not found" -ForegroundColor Red
    Write-Host "    Install from: https://python.org" -ForegroundColor Gray
    $allGood = $false
}

# Check Git
Write-Host "`n[2/7] Checking Git..." -ForegroundColor Yellow
$gitCheck = Get-Command git -ErrorAction SilentlyContinue
if ($gitCheck) {
    $gitVersion = git --version 2>&1
    Write-Host "  ✓ $gitVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Git not found" -ForegroundColor Red
    Write-Host "    Install from: https://git-scm.com" -ForegroundColor Gray
    $allGood = $false
}

# Check Temporal CLI
Write-Host "`n[3/7] Checking Temporal CLI..." -ForegroundColor Yellow
$temporalCheck = Get-Command temporal -ErrorAction SilentlyContinue
if ($temporalCheck) {
    $temporalVersion = temporal --version 2>&1
    Write-Host "  ✓ $temporalVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Temporal CLI not found" -ForegroundColor Red
    Write-Host "    Install from: https://github.com/temporalio/cli/releases" -ForegroundColor Gray
    $allGood = $false
}

# Check virtual environment
Write-Host "`n[4/7] Checking virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv\Scripts\python.exe") {
    Write-Host "  ✓ Virtual environment exists" -ForegroundColor Green
} else {
    Write-Host "  ✗ Virtual environment not found" -ForegroundColor Red
    Write-Host "    Run: python -m venv venv" -ForegroundColor Gray
    $allGood = $false
}

# Check if venv is activated
Write-Host "`n[5/7] Checking if venv is activated..." -ForegroundColor Yellow
if ($env:VIRTUAL_ENV) {
    Write-Host "  ✓ Virtual environment is activated" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Virtual environment NOT activated" -ForegroundColor Yellow
    Write-Host "    Run: .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
}

# Check Python dependencies
Write-Host "`n[6/7] Checking Python dependencies..." -ForegroundColor Yellow
if (Test-Path "venv\Scripts\python.exe") {
    $temporalioInstalled = & "venv\Scripts\python.exe" -c "import temporalio; print('OK')" 2>&1
    if ($temporalioInstalled -eq "OK") {
        Write-Host "  ✓ temporalio package installed" -ForegroundColor Green
    } else {
        Write-Host "  ✗ temporalio package not found" -ForegroundColor Red
        Write-Host "    Run: pip install -r requirements.txt" -ForegroundColor Gray
        $allGood = $false
    }
} else {
    Write-Host "  ⚠ Skipping (venv not found)" -ForegroundColor Yellow
}

# Check required project files
Write-Host "`n[7/7] Checking project files..." -ForegroundColor Yellow
$requiredFiles = @(
    "workflow.py",
    "activities.py",
    "worker.py",
    "demo_progress_monitoring.py",
    "tracks_enriched.json",
    "camelot.py",
    "sequencer.py",
    "scoring.py",
    "justifier.py"
)

$missingFiles = 0
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file MISSING" -ForegroundColor Red
        $missingFiles++
        $allGood = $false
    }
}

# Final summary
Write-Host "`n================================================" -ForegroundColor Cyan
if ($allGood) {
    Write-Host "  ✅ All checks passed! Ready to run demo." -ForegroundColor Green
    Write-Host "`nNext steps:" -ForegroundColor Yellow
    Write-Host "  1. Terminal 1: temporal server start-dev" -ForegroundColor White
    Write-Host "  2. Terminal 2: python worker.py" -ForegroundColor White
    Write-Host "  3. Terminal 3: python demo_progress_monitoring.py" -ForegroundColor White
    Write-Host "  4. Terminal 4: start http://localhost:8233" -ForegroundColor White
} else {
    Write-Host "  ⚠ Setup incomplete. Fix issues above." -ForegroundColor Yellow
}
Write-Host "================================================" -ForegroundColor Cyan
