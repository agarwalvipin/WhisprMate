#!/bin/bash
# Shell wrapper for the audio trimming script using uv virtual environment.

set -e  # Exit on any error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PYTHON_SCRIPT="$SCRIPT_DIR/trim_audio.py"
VENV_DIR="$PROJECT_ROOT/.venv"

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: trim_audio.py not found at $PYTHON_SCRIPT"
    exit 1
fi

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed or not in PATH"
    echo "Please install uv: https://github.com/astral-sh/uv"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment with uv..."
    cd "$PROJECT_ROOT"
    uv venv
fi

# Sync dependencies if pyproject.toml or requirements.txt exists
cd "$PROJECT_ROOT"
if [ -f "pyproject.toml" ] || [ -f "requirements.txt" ]; then
    echo "Syncing dependencies..."
    uv sync 2>/dev/null || {
        echo "Warning: Could not sync dependencies, trying to install soundfile..."
        uv pip install soundfile
    }
fi

# Run the Python script using uv
echo "Running audio trimming script..."
uv run python "$PYTHON_SCRIPT" "$@"
