#!/bin/bash

# Docker deployment script for Speaker Diarization App

set -e

# Configuration
IMAGE_NAME="whisprmate"
CONTAINER_NAME="whisprmate"
HOST_PORT="8501"
CONTAINER_PORT="8501"

# Default credentials (can be overridden with environment variables)
DEFAULT_USERNAME="${STREAMLIT_USERNAME:-admin}"
DEFAULT_PASSWORD="${STREAMLIT_PASSWORD:-admin}"

echo "🐳 Building and deploying Speaker Diarization App with Docker"
echo "=================================================="

# Function to check if container is running
check_container() {
    if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
        return 0
    else
        return 1
    fi
}

# Function to stop and remove existing container
cleanup_container() {
    if check_container; then
        echo "🛑 Stopping existing container..."
        docker stop "$CONTAINER_NAME"
    fi
    
    if docker ps -a -q -f name="$CONTAINER_NAME" | grep -q .; then
        echo "🗑️  Removing existing container..."
        docker rm "$CONTAINER_NAME"
    fi
}

# Build the Docker image
echo "🔨 Building Docker image..."
docker build -t "$IMAGE_NAME" .

# Stop and remove existing container if it exists
cleanup_container

# Create uploads directory if it doesn't exist
mkdir -p uploads data/samples

# Run the container
echo "🚀 Starting container..."
docker run -d \
    --name "$CONTAINER_NAME" \
    -p "$HOST_PORT:$CONTAINER_PORT" \
    -v "$(pwd)/uploads:/app/uploads" \
    -v "$(pwd)/data:/app/data" \
    -e STREAMLIT_USERNAME="$DEFAULT_USERNAME" \
    -e STREAMLIT_PASSWORD="$DEFAULT_PASSWORD" \
    $([ -f .env ] && echo "-v $(pwd)/.env:/app/.env:ro") \
    "$IMAGE_NAME" \
    streamlit run main.py \
    --server.port="$CONTAINER_PORT" \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.fileWatcherType=none \
    --browser.gatherUsageStats=false \
    -- \
    --username "$DEFAULT_USERNAME" \
    --password "$DEFAULT_PASSWORD"

echo "✅ Container started successfully!"
echo ""
echo "📋 Container Information:"
echo "  Name: $CONTAINER_NAME"
echo "  Image: $IMAGE_NAME"
echo "  Port: http://localhost:$HOST_PORT"
echo "  Username: $DEFAULT_USERNAME"
echo "  Password: $DEFAULT_PASSWORD"
echo ""
echo "🔍 Useful commands:"
echo "  View logs: docker logs $CONTAINER_NAME"
echo "  Stop app:  docker stop $CONTAINER_NAME"
echo "  Start app: docker start $CONTAINER_NAME"
echo "  Remove app: docker rm $CONTAINER_NAME"
echo ""
echo "🌐 Access the app at: http://localhost:$HOST_PORT"
