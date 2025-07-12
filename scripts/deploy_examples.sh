#!/bin/bash

# WhisprMate Deployment Examples
# Demonstrates different ways to deploy with custom upload directories

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 WhisprMate Deployment Examples${NC}"
echo "=================================="

# Example 1: Use specific host directories
echo ""
echo "📁 Example 1: Custom host directories"
echo "UPLOADS_HOST_PATH=/home/user/whisprmate/uploads \\"
echo "LOGS_HOST_PATH=/home/user/whisprmate/logs \\"
echo "DATA_HOST_PATH=/home/user/whisprmate/data \\"
echo "./scripts/deploy.sh"

# Example 2: Use environment variables from .env file
echo ""
echo "📁 Example 2: Using .env file"
echo "# Create/edit .env file with:"
echo "cat << EOF > .env"
echo "UPLOADS_HOST_PATH=/custom/uploads/path"
echo "LOGS_HOST_PATH=/custom/logs/path"
echo "DATA_HOST_PATH=/custom/data/path"
echo "LOG_LEVEL=DEBUG"
echo "HF_TOKEN=your_token_here"
echo "EOF"
echo ""
echo "# Then run:"
echo "./scripts/deploy.sh"

# Example 3: Docker Compose with custom paths
echo ""
echo "📁 Example 3: Docker Compose"
echo "UPLOADS_HOST_PATH=/shared/whisprmate/uploads \\"
echo "LOGS_HOST_PATH=/shared/whisprmate/logs \\"
echo "docker-compose up -d"

# Example 4: Network storage
echo ""
echo "📁 Example 4: Network storage (NFS/SMB mount)"
echo "# First mount your network storage"
echo "# sudo mount -t nfs server:/exports/whisprmate /mnt/whisprmate"
echo "UPLOADS_HOST_PATH=/mnt/whisprmate/uploads \\"
echo "LOGS_HOST_PATH=/mnt/whisprmate/logs \\"
echo "./scripts/deploy.sh"

# Example 5: Docker with external volume
echo ""
echo "📁 Example 5: Docker external volume"
echo "# Create external volume"
echo "docker volume create whisprmate_uploads"
echo "docker volume create whisprmate_logs"
echo ""
echo "# Run with external volumes"
echo "docker run -d \\"
echo "  --name whisprmate \\"
echo "  -p 8501:8501 \\"
echo "  -v whisprmate_uploads:/app/uploads \\"
echo "  -v whisprmate_logs:/app/logs \\"
echo "  -e LOG_LEVEL=INFO \\"
echo "  whisprmate"

echo ""
echo "🔧 Configuration Tips:"
echo "  - Set UPLOADS_HOST_PATH for custom upload location"
echo "  - Set LOGS_HOST_PATH for centralized logging"
echo "  - Use absolute paths for host directories"
echo "  - Ensure directories have proper permissions"
echo "  - Use .env file for persistent configuration"

# Interactive deployment option
echo ""
read -p "🚀 Run a custom deployment now? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    read -p "📁 Enter uploads host path (default: ./uploads): " uploads_path
    read -p "📄 Enter logs host path (default: ./logs): " logs_path
    read -p "📊 Enter data host path (default: ./data): " data_path
    read -p "🔍 Enter log level (DEBUG/INFO/WARNING/ERROR, default: INFO): " log_level
    
    # Set defaults if empty
    uploads_path=${uploads_path:-./uploads}
    logs_path=${logs_path:-./logs}
    data_path=${data_path:-./data}
    log_level=${log_level:-INFO}
    
    echo ""
    echo "🚀 Deploying with custom settings..."
    export UPLOADS_HOST_PATH="$uploads_path"
    export LOGS_HOST_PATH="$logs_path"
    export DATA_HOST_PATH="$data_path"
    export LOG_LEVEL="$log_level"
    
    ./scripts/deploy.sh
fi
