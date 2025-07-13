#!/bin/bash

# WhisprMate Development Environment Activation
# This script activates the uv virtual environment for development

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Creating one with uv..."
    uv venv
    echo "Installing requirements..."
    source .venv/bin/activate
    uv pip install -r requirements.txt
else
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

echo "Virtual environment activated!"
echo "You can now run Python commands in the WhisprMate environment."
echo ""
echo "To run the application:"
echo "  python -m streamlit run main.py"
echo ""
echo "To deactivate the environment:"
echo "  deactivate"

# Start a new shell with the activated environment
exec "$SHELL"
