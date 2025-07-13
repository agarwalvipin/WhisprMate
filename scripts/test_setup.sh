#!/bin/bash

# Test script to verify the uv environment setup
echo "Testing WhisprMate setup with uv..."

# Check if .venv directory exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found"
    exit 1
fi

echo "✅ Virtual environment found"

# Activate environment and check Python version
source .venv/bin/activate

echo "Python version: $(python --version)"
echo "Virtual environment: $VIRTUAL_ENV"

# Check required packages
echo "Checking required packages..."

for package in streamlit soundfile python-dotenv; do
    if python -c "import $package" 2>/dev/null; then
        echo "✅ $package installed"
    else
        echo "❌ $package not found"
    fi
done

echo "✅ Environment setup test completed!"

# Show usage instructions
echo ""
echo "To run the application:"
echo "  ./run_app.sh"
echo ""
echo "Or manually:"
echo "  source .venv/bin/activate"
echo "  python -m streamlit run main.py"
