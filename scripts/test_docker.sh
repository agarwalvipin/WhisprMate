#!/bin/bash

# Docker Test Script for WhisprMate
echo "🧪 Testing WhisprMate Docker Container..."

# Test 1: Check if container is running
if docker ps --filter "name=whisprmate" --format "{{.Names}}" | grep -q "whisprmate"; then
    echo "✅ Container is running"
    CONTAINER_STATUS=$(docker ps --filter "name=whisprmate" --format "{{.Status}}")
    echo "   Status: $CONTAINER_STATUS"
else
    echo "❌ Container is not running"
    exit 1
fi

# Test 2: Check container health
HEALTH_STATUS=$(docker inspect whisprmate --format='{{.State.Health.Status}}' 2>/dev/null)
if [ "$HEALTH_STATUS" = "healthy" ]; then
    echo "✅ Container health check passed"
else
    echo "⚠️  Container health: $HEALTH_STATUS"
fi

# Test 3: Check if port is accessible
if ss -tulpn | grep -q ":8501"; then
    echo "✅ Port 8501 is accessible"
else
    echo "❌ Port 8501 is not accessible"
fi

# Test 4: Test HTTP response
echo "🌐 Testing HTTP response..."
if command -v curl >/dev/null 2>&1; then
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8501)
    if [ "$HTTP_STATUS" = "200" ]; then
        echo "✅ HTTP response: $HTTP_STATUS (OK)"
    else
        echo "⚠️  HTTP response: $HTTP_STATUS"
    fi
    
    # Test if it contains expected content
    if curl -s http://localhost:8501 | grep -q "Speaker Diarization\|WhisprMate"; then
        echo "✅ Application content detected"
    else
        echo "⚠️  Application may still be loading"
    fi
else
    echo "ℹ️  curl not available for HTTP testing"
fi

# Test 5: Check container logs for errors
echo "📝 Checking container logs for errors..."
ERROR_COUNT=$(docker logs whisprmate 2>&1 | grep -i "error\|exception\|traceback" | wc -l)
if [ "$ERROR_COUNT" -eq 0 ]; then
    echo "✅ No errors found in logs"
else
    echo "⚠️  Found $ERROR_COUNT potential errors in logs"
    echo "   Recent log entries:"
    docker logs whisprmate --tail 10
fi

# Test 6: Test environment variables
echo "🔧 Checking environment variables..."
USERNAME=$(docker exec whisprmate printenv STREAMLIT_USERNAME 2>/dev/null || echo "not set")
echo "   STREAMLIT_USERNAME: $USERNAME"

# Test 7: Check mounted volumes
echo "📁 Checking mounted volumes..."
VOLUMES=$(docker inspect whisprmate --format='{{range .Mounts}}{{.Source}}:{{.Destination}} {{end}}')
echo "   Mounted volumes: $VOLUMES"

echo ""
echo "🎉 Docker test completed!"
echo "📍 Access your application at: http://localhost:8501"
echo "🔑 Login credentials: dockeruser / dockerpass"
echo ""
echo "📊 Container Info:"
docker stats whisprmate --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
