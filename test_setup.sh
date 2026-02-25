#!/bin/bash
# test_setup.sh
# Linux Setup Verification Script for DJ Set Curator

echo "================================================"
echo "  DJ Set Curator - Setup Verification (Linux)"
echo "================================================"

ALL_GOOD=true

# Check Python
echo ""
echo "[1/7] Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo "  OK $PYTHON_VERSION"
else
    echo "  FAIL Python3 not found"
    echo "    Install: sudo dnf install python3 -y"
    ALL_GOOD=false
fi

# Check Git
echo ""
echo "[2/7] Checking Git..."
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version 2>&1)
    echo "  OK $GIT_VERSION"
else
    echo "  FAIL Git not found"
    echo "    Install: sudo dnf install git -y"
    ALL_GOOD=false
fi

# Check Temporal CLI
echo ""
echo "[3/7] Checking Temporal CLI..."
if command -v temporal &> /dev/null; then
    TEMPORAL_VERSION=$(temporal --version 2>&1)
    echo "  OK $TEMPORAL_VERSION"
else
    echo "  FAIL Temporal CLI not found"
    echo "    Install: curl -sSf https://temporal.download/cli.sh | sh"
    echo "    Then add to PATH: export PATH=\"\$HOME/.temporalio/bin:\$PATH\""
    ALL_GOOD=false
fi

# Check virtual environment
echo ""
echo "[4/7] Checking virtual environment..."
if [ -f "venv/bin/python" ]; then
    echo "  OK Virtual environment exists"
else
    echo "  FAIL Virtual environment not found"
    echo "    Run: python3 -m venv venv"
    ALL_GOOD=false
fi

# Check if venv is activated
echo ""
echo "[5/7] Checking if venv is activated..."
if [ -n "$VIRTUAL_ENV" ]; then
    echo "  OK Virtual environment is activated"
else
    echo "  WARN Virtual environment NOT activated"
    echo "    Run: source venv/bin/activate"
fi

# Check Python dependencies
echo ""
echo "[6/7] Checking Python dependencies..."
if [ -f "venv/bin/python" ]; then
    TEMPORALIO_CHECK=$(venv/bin/python -c "import temporalio; print('OK')" 2>&1)
    if [ "$TEMPORALIO_CHECK" = "OK" ]; then
        echo "  OK temporalio package installed"
    else
        echo "  FAIL temporalio package not found"
        echo "    Run: pip install -r requirements.txt"
        ALL_GOOD=false
    fi
else
    echo "  WARN Skipping (venv not found)"
fi

# Check required project files
echo ""
echo "[7/7] Checking project files..."
REQUIRED_FILES=(
    "workflow.py"
    "activities.py"
    "worker.py"
    "demo_progress_monitoring.py"
    "tracks_enriched.json"
    "camelot.py"
    "sequencer.py"
    "scoring.py"
    "justifier.py"
)

MISSING_FILES=0
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  OK $file"
    else
        echo "  FAIL $file MISSING"
        ((MISSING_FILES++))
        ALL_GOOD=false
    fi
done

# Final summary
echo ""
echo "================================================"
if [ "$ALL_GOOD" = true ]; then
    echo "  SUCCESS All checks passed! Ready to run demo."
    echo ""
    echo "Next steps:"
    echo "  1. Terminal 1: temporal server start-dev"
    echo "  2. Terminal 2: python worker.py"
    echo "  3. Terminal 3: python demo_progress_monitoring.py"
    echo "  4. Terminal 4: firefox http://localhost:8233"
else
    echo "  WARNING Setup incomplete. Fix issues above."
fi
echo "================================================"
