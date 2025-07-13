#!/bin/bash
# Setup script for WhisprMate development environment using uv.
# This script creates a virtual environment and installs all dependencies.

set -e  # Exit on any error

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$PROJECT_ROOT/.venv"

echo "Setting up WhisprMate development environment..."

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed or not in PATH"
    echo "Please install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

cd "$PROJECT_ROOT"

# Create virtual environment
echo "Creating virtual environment..."
uv venv

# Install dependencies
echo "Installing dependencies..."
if [ -f "pyproject.toml" ]; then
    echo "Installing from pyproject.toml..."
    uv sync
elif [ -f "requirements.txt" ]; then
    echo "Installing from requirements.txt..."
    uv pip install -r requirements.txt
fi

# Install additional audio processing dependencies
echo "Installing audio processing dependencies..."
uv pip install soundfile

echo ""
echo "Setup complete! Virtual environment created at: $VENV_DIR"
echo ""
echo "To activate the environment manually:"
echo "  source $VENV_DIR/bin/activate"
echo ""
echo "To run the audio trimming script:"
echo "  ./scripts/trim_audio.sh input.wav 5"
echo "  # or"
echo "  uv run python scripts/trim_audio.py input.wav 5"
echo ""
