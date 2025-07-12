#!/bin/bash

# Simple Docker build script for Speaker Diarization App

set -e

IMAGE_NAME="whisprmate"
TAG="${1:-latest}"

echo "🔨 Building Docker image: $IMAGE_NAME:$TAG"
echo "============================================="

# Build the image
docker build -t "$IMAGE_NAME:$TAG" .

echo "✅ Build completed successfully!"
echo ""
echo "🚀 To run the container:"
echo "  docker run -p 8501:8501 $IMAGE_NAME:$TAG"
echo ""
echo "🌐 Then access the app at: http://localhost:8501"
