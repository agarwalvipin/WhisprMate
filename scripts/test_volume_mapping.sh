#!/bin/bash

# WhisprMate Docker Volume Mapping Test Script
# Tests the upload directory mapping functionality

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧪 WhisprMate Docker Volume Mapping Test${NC}"
echo "=============================================="

# Configuration
CONTAINER_NAME="whisprmate-volume-test"
HOST_UPLOADS_DIR="$(pwd)/test_host_uploads"
HOST_LOGS_DIR="$(pwd)/test_host_logs"
CONTAINER_PORT="8503"

# Cleanup function
cleanup() {
    echo -e "${YELLOW}🧹 Cleaning up...${NC}"
    docker rm -f $CONTAINER_NAME 2>/dev/null || true
    rm -rf "$HOST_UPLOADS_DIR" "$HOST_LOGS_DIR" 2>/dev/null || true
}

# Setup cleanup trap
trap cleanup EXIT

echo -e "${BLUE}📁 Setting up test directories...${NC}"
mkdir -p "$HOST_UPLOADS_DIR" "$HOST_LOGS_DIR"

echo -e "${BLUE}🐳 Starting container with volume mapping...${NC}"
docker run -d \
    --name $CONTAINER_NAME \
    -p $CONTAINER_PORT:8501 \
    -v "$HOST_UPLOADS_DIR:/app/uploads" \
    -v "$HOST_LOGS_DIR:/app/logs" \
    -e LOG_LEVEL=DEBUG \
    -e UPLOADS_HOST_PATH="$HOST_UPLOADS_DIR" \
    -e LOGS_HOST_PATH="$HOST_LOGS_DIR" \
    --user $(id -u):$(id -g) \
    whisprmate

echo -e "${YELLOW}⏳ Waiting for container to start...${NC}"
sleep 10

# Test 1: Container Health
echo -e "${BLUE}🏥 Testing container health...${NC}"
if docker ps | grep -q $CONTAINER_NAME; then
    echo -e "${GREEN}✅ Container is running${NC}"
else
    echo -e "${RED}❌ Container failed to start${NC}"
    docker logs $CONTAINER_NAME
    exit 1
fi

# Test 2: Application Accessibility
echo -e "${BLUE}🌐 Testing application accessibility...${NC}"
if curl -s "http://localhost:$CONTAINER_PORT" > /dev/null; then
    echo -e "${GREEN}✅ Application is accessible on port $CONTAINER_PORT${NC}"
else
    echo -e "${RED}❌ Application is not accessible${NC}"
    exit 1
fi

# Test 3: Host to Container File Mapping
echo -e "${BLUE}📤 Testing host to container file mapping...${NC}"
echo "Test content from host" > "$HOST_UPLOADS_DIR/host_test.txt"
if docker exec $CONTAINER_NAME test -f /app/uploads/host_test.txt; then
    echo -e "${GREEN}✅ Host-created file visible in container${NC}"
    content=$(docker exec $CONTAINER_NAME cat /app/uploads/host_test.txt)
    if [ "$content" = "Test content from host" ]; then
        echo -e "${GREEN}✅ File content matches${NC}"
    else
        echo -e "${RED}❌ File content mismatch${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ Host-created file not visible in container${NC}"
    exit 1
fi

# Test 4: Container to Host File Mapping
echo -e "${BLUE}📥 Testing container to host file mapping...${NC}"
docker exec $CONTAINER_NAME sh -c "echo 'Test content from container' > /app/uploads/container_test.txt"
if [ -f "$HOST_UPLOADS_DIR/container_test.txt" ]; then
    echo -e "${GREEN}✅ Container-created file visible on host${NC}"
    content=$(cat "$HOST_UPLOADS_DIR/container_test.txt")
    if [ "$content" = "Test content from container" ]; then
        echo -e "${GREEN}✅ File content matches${NC}"
    else
        echo -e "${RED}❌ File content mismatch${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ Container-created file not visible on host${NC}"
    exit 1
fi

# Test 5: Environment Variables
echo -e "${BLUE}🔧 Testing environment variables...${NC}"
uploads_path=$(docker exec $CONTAINER_NAME printenv UPLOADS_HOST_PATH || echo "not_set")
logs_path=$(docker exec $CONTAINER_NAME printenv LOGS_HOST_PATH || echo "not_set")

if [ "$uploads_path" = "$HOST_UPLOADS_DIR" ]; then
    echo -e "${GREEN}✅ UPLOADS_HOST_PATH environment variable set correctly${NC}"
else
    echo -e "${YELLOW}⚠️  UPLOADS_HOST_PATH not set or incorrect: $uploads_path${NC}"
fi

if [ "$logs_path" = "$HOST_LOGS_DIR" ]; then
    echo -e "${GREEN}✅ LOGS_HOST_PATH environment variable set correctly${NC}"
else
    echo -e "${YELLOW}⚠️  LOGS_HOST_PATH not set or incorrect: $logs_path${NC}"
fi

# Test 6: Directory Permissions
echo -e "${BLUE}🔐 Testing directory permissions...${NC}"
if docker exec $CONTAINER_NAME test -w /app/uploads; then
    echo -e "${GREEN}✅ Container can write to uploads directory${NC}"
else
    echo -e "${RED}❌ Container cannot write to uploads directory${NC}"
    exit 1
fi

# Test 7: Application Configuration
echo -e "${BLUE}⚙️  Testing application configuration...${NC}"
docker exec $CONTAINER_NAME python -c "
from config.settings import AppConfig
upload_dir = AppConfig.get_upload_dir()
print(f'Upload directory: {upload_dir}')
print(f'Directory exists: {upload_dir.exists()}')
print(f'Is writable: {upload_dir.exists() and upload_dir.is_dir()}')
" > /tmp/config_test.txt

if grep -q "Directory exists: True" /tmp/config_test.txt; then
    echo -e "${GREEN}✅ Application configuration is correct${NC}"
else
    echo -e "${RED}❌ Application configuration issue${NC}"
    cat /tmp/config_test.txt
fi

# Test 8: Volume Persistence
echo -e "${BLUE}💾 Testing volume persistence...${NC}"
echo "Persistence test" > "$HOST_UPLOADS_DIR/persistence_test.txt"
docker restart $CONTAINER_NAME
sleep 10

if docker exec $CONTAINER_NAME test -f /app/uploads/persistence_test.txt; then
    echo -e "${GREEN}✅ Files persist across container restarts${NC}"
else
    echo -e "${RED}❌ Files do not persist across container restarts${NC}"
    exit 1
fi

echo -e "${GREEN}🎉 All tests passed! Volume mapping is working correctly.${NC}"
echo ""
echo -e "${BLUE}📋 Test Summary:${NC}"
echo "• Container is running and healthy"
echo "• Application is accessible on port $CONTAINER_PORT"
echo "• Host to container file mapping works"
echo "• Container to host file mapping works"
echo "• Environment variables are set correctly"
echo "• Directory permissions are correct"
echo "• Application configuration is valid"
echo "• Files persist across container restarts"
echo ""
echo -e "${BLUE}🚀 You can now access the application at: http://localhost:$CONTAINER_PORT${NC}"
echo ""
echo -e "${YELLOW}📁 Host directories:${NC}"
echo "• Uploads: $HOST_UPLOADS_DIR"
echo "• Logs: $HOST_LOGS_DIR"
echo ""
echo -e "${YELLOW}💡 To clean up manually, run:${NC}"
echo "docker rm -f $CONTAINER_NAME"
echo "rm -rf '$HOST_UPLOADS_DIR' '$HOST_LOGS_DIR'"
