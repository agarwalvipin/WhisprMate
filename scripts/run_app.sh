#!/bin/bash

# WhisprMate Application Runner
# This script activates the uv virtual environment and runs the Streamlit app

set -e

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

# Default values
PORT=8501
HOST=0.0.0.0
USERNAME=${STREAMLIT_USERNAME:-admin}
PASSWORD=${STREAMLIT_PASSWORD:-admin}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --port)
            PORT="$2"
            shift 2
            ;;
        --host)
            HOST="$2"
            shift 2
            ;;
        --username)
            USERNAME="$2"
            shift 2
            ;;
        --password)
            PASSWORD="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --port PORT       Port to run on (default: 8501)"
            echo "  --host HOST       Host to bind to (default: 0.0.0.0)"
            echo "  --username USER   Default username (default: admin)"
            echo "  --password PASS   Default password (default: admin)"
            echo "  -h, --help        Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo "Starting WhisprMate application..."
echo "  Host: $HOST"
echo "  Port: $PORT"
echo "  Username: $USERNAME"
echo "  Access URL: http://localhost:$PORT"
echo ""
echo "Press Ctrl+C to stop the application"

# Export environment variables for the app
export STREAMLIT_USERNAME="$USERNAME"
export STREAMLIT_PASSWORD="$PASSWORD"

# Run the application
python -m streamlit run main.py \
    --server.port "$PORT" \
    --server.address "$HOST" \
    -- \
    --username "$USERNAME" \
    --password "$PASSWORD"
