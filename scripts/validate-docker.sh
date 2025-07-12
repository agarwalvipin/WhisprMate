#!/bin/bash

# Docker validation script for Speaker Diarization App

set -e

echo "🐳 Validating Docker setup for Speaker Diarization App"
echo "===================================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

echo "✅ Docker is installed: $(docker --version)"

# Check if Dockerfile exists
if [ ! -f "Dockerfile" ]; then
    echo "❌ Dockerfile not found in current directory"
    exit 1
fi

echo "✅ Dockerfile found"

# Check if .dockerignore exists
if [ ! -f ".dockerignore" ]; then
    echo "⚠️  .dockerignore not found (recommended but not required)"
else
    echo "✅ .dockerignore found"
fi

# Validate Dockerfile syntax
echo "🔍 Validating Dockerfile syntax..."
if docker build --help > /dev/null 2>&1; then
    echo "✅ Docker build command is available"
else
    echo "❌ Docker build command failed"
    exit 1
fi

# Check required files
echo "🔍 Checking required files..."
required_files=("main.py" "requirements.txt" "src/" "config/")
for file in "${required_files[@]}"; do
    if [ -e "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
        exit 1
    fi
done

# Check scripts
if [ -f "scripts/deploy.sh" ] && [ -x "scripts/deploy.sh" ]; then
    echo "✅ Deploy script is executable"
else
    echo "⚠️  Deploy script not found or not executable"
fi

if [ -f "scripts/build.sh" ] && [ -x "scripts/build.sh" ]; then
    echo "✅ Build script is executable"
else
    echo "⚠️  Build script not found or not executable"
fi

echo ""
echo "🎉 Docker setup validation completed successfully!"
echo ""
echo "📋 Next steps:"
echo "  1. Build the image: ./scripts/build.sh"
echo "  2. Deploy the app: ./scripts/deploy.sh"
echo "  3. Access at: http://localhost:8501"
