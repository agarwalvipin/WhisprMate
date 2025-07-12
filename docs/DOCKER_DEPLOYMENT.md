# Docker Deployment Guide

This guide explains how to containerize and deploy the Speaker Diarization App using Docker.

## 🐳 Quick Start

### Option 1: Using the deployment script (Recommended)

```bash
# Build and run the container with default settings
./scripts/deploy.sh

# With custom credentials
STREAMLIT_USERNAME=myuser STREAMLIT_PASSWORD=mypass ./scripts/deploy.sh
```

### Option 2: Manual Docker commands

```bash
# Build the image
docker build -t WhisprMate .

# Run the container
docker run -d \
  --name WhisprMate \
  -p 8501:8501 \
  -v $(pwd)/uploads:/app/uploads \
  WhisprMate
```

## 📋 Docker Configuration

### Dockerfile Features

- **Base Image**: Python 3.11 slim for optimal performance
- **System Dependencies**: Includes ffmpeg, libsndfile for audio processing
- **ML Libraries**: OpenAI Whisper, pyannote.audio, PyTorch (CPU version)
- **Security**: Non-root user, minimal attack surface
- **Health Checks**: Built-in health monitoring
- **Optimizations**: Multi-stage build, layer caching

### Environment Variables

| Variable              | Default | Description                                      |
| --------------------- | ------- | ------------------------------------------------ |
| `STREAMLIT_USERNAME`  | `admin` | Default login username                           |
| `STREAMLIT_PASSWORD`  | `admin` | Default login password                           |
| `HF_TOKEN`            | -       | HuggingFace token for speaker diarization        |
| `LOG_LEVEL`           | `INFO`  | Logging level (DEBUG, INFO, WARNING, ERROR)     |
| `UPLOADS_HOST_PATH`   | -       | Custom host directory path for uploads mapping  |
| `LOGS_HOST_PATH`      | -       | Custom host directory path for logs mapping     |
| `UPLOADS_DIR`         | -       | Container uploads directory override             |
| `LOG_FILE`            | -       | Custom log file path                             |

### Ports

- **8501**: Streamlit web interface

### Volumes

- `/app/uploads`: User uploaded audio files (configurable via UPLOADS_HOST_PATH)
- `/app/logs`: Application and error logs (configurable via LOGS_HOST_PATH)
- `/app/data`: Sample data and outputs
- `/app/.env`: Environment variables file (optional)

## 🚀 Volume Mapping & Persistent Storage

### Custom Upload Directories

Map uploads to custom host directories for persistent storage:

```bash
# Basic volume mapping
docker run -p 8501:8501 \
  -v /custom/uploads:/app/uploads \
  -v /custom/logs:/app/logs \
  whisprmate

# Using environment variables
docker run -p 8501:8501 \
  -e UPLOADS_HOST_PATH=/custom/uploads \
  -e LOGS_HOST_PATH=/custom/logs \
  -v /custom/uploads:/app/uploads \
  -v /custom/logs:/app/logs \
  whisprmate

# Network storage example (NFS/SMB)
docker run -p 8501:8501 \
  -e UPLOADS_HOST_PATH=/mnt/network-storage/uploads \
  -e LOGS_HOST_PATH=/mnt/network-storage/logs \
  -v /mnt/network-storage/uploads:/app/uploads \
  -v /mnt/network-storage/logs:/app/logs \
  whisprmate
```

### Docker Compose with Custom Paths

```bash
# Set environment variables before running
export UPLOADS_HOST_PATH=/shared/storage/uploads
export LOGS_HOST_PATH=/shared/storage/logs
docker-compose up -d

# Or inline
UPLOADS_HOST_PATH=/custom/path LOGS_HOST_PATH=/custom/logs docker-compose up -d
```

### Testing Volume Mapping

Use the provided test script to verify volume mapping:

```bash
# Run comprehensive volume mapping tests
./scripts/test_volume_mapping.sh

# Interactive deployment examples
./scripts/deploy_examples.sh
```

## 🔧 Logging Configuration

### Logging Levels

The application supports multiple logging levels for debugging and monitoring:

```bash
# Debug mode with detailed logging
docker run -p 8501:8501 \
  -e LOG_LEVEL=DEBUG \
  -v $(pwd)/logs:/app/logs \
  whisprmate

# Production mode with info logging
docker run -p 8501:8501 \
  -e LOG_LEVEL=INFO \
  -v /var/logs/whisprmate:/app/logs \
  whisprmate
```

### Log File Structure

- **Application logs**: `logs/whisprmate_YYYYMMDD_HHMMSS.log`
- **Error logs**: `logs/errors.log`
- **Service logs**: Component-specific logging for auth, audio processing, file management

## 🚀 Deployment Options

### Development Deployment

For local development and testing:

```bash
# Build and run with hot reload disabled
docker run -p 8501:8501 \
  -v $(pwd)/uploads:/app/uploads \
  WhisprMate
```

### Production Deployment

For production environments:

```bash
# Run with resource limits and restart policy
docker run -d \
  --name speaker-diarization-prod \
  --restart unless-stopped \
  --memory 2g \
  --cpus 2 \
  -p 8501:8501 \
  -v /var/app/uploads:/app/uploads \
  -v /var/app/data:/app/data \
  -e STREAMLIT_USERNAME=secure_user \
  -e STREAMLIT_PASSWORD=secure_password \
  WhisprMate
```

### With External HuggingFace Token

For speaker diarization functionality:

```bash
# Using environment variable
docker run -d \
  --name WhisprMate \
  -p 8501:8501 \
  -e HF_TOKEN=your_huggingface_token \
  WhisprMate

# Or mount .env file
docker run -d \
  --name WhisprMate \
  -p 8501:8501 \
  -v $(pwd)/.env:/app/.env:ro \
  WhisprMate
```

## 🔧 Build Options

### Standard Build

```bash
# Build with default settings
docker build -t WhisprMate .
```

### Custom Build Arguments

```bash
# Build with specific Python version
docker build \
  --build-arg PYTHON_VERSION=3.10 \
  -t WhisprMate:python3.10 .
```

### Multi-platform Build

```bash
# Build for multiple architectures
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t WhisprMate:multi-arch .
```

## 📊 Container Management

### Monitoring

```bash
# View container logs
docker logs WhisprMate

# Follow logs in real-time
docker logs -f WhisprMate

# Check container status
docker ps

# Check container resource usage
docker stats WhisprMate
```

### Maintenance

```bash
# Stop the container
docker stop WhisprMate

# Start the container
docker start WhisprMate

# Restart the container
docker restart WhisprMate

# Remove the container
docker rm WhisprMate

# Remove the image
docker rmi WhisprMate
```

### Health Checks

The container includes built-in health checks:

```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' WhisprMate

# View health check logs
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' WhisprMate
```

## 🛠️ Troubleshooting

### Common Issues

1. **Container won't start**

   ```bash
   # Check logs for errors
   docker logs WhisprMate

   # Verify image was built correctly
   docker images | grep WhisprMate
   ```

2. **Audio processing fails**

   ```bash
   # Ensure ffmpeg is working
   docker exec -it WhisprMate ffmpeg -version

   # Check audio file permissions
   docker exec -it WhisprMate ls -la uploads/
   ```

3. **Memory issues**

   ```bash
   # Increase memory limits
   docker run --memory 4g WhisprMate

   # Monitor memory usage
   docker stats WhisprMate
   ```

### Debug Mode

Run container in interactive mode for debugging:

```bash
# Start container with bash shell
docker run -it --entrypoint /bin/bash WhisprMate

# Or execute shell in running container
docker exec -it WhisprMate /bin/bash
```

## 🔒 Security Considerations

### Production Security

1. **Use non-default credentials**

   ```bash
   -e STREAMLIT_USERNAME=your_secure_username \
   -e STREAMLIT_PASSWORD=your_secure_password
   ```

2. **Limit container resources**

   ```bash
   --memory 2g --cpus 2
   ```

3. **Use read-only volumes where possible**

   ```bash
   -v $(pwd)/.env:/app/.env:ro
   ```

4. **Run with user namespace mapping**
   ```bash
   --user $(id -u):$(id -g)
   ```

### Network Security

For production deployments, consider using a reverse proxy:

```bash
# Run on localhost only
docker run -p 127.0.0.1:8501:8501 WhisprMate
```

## 📈 Performance Optimization

### Resource Allocation

```bash
# For CPU-intensive workloads
docker run --cpus 4 --memory 4g WhisprMate

# For GPU support (if available)
docker run --gpus all WhisprMate
```

### Storage Optimization

```bash
# Use named volumes for better performance
docker volume create speaker-uploads
docker run -v speaker-uploads:/app/uploads WhisprMate
```

## 🔄 Updates and Maintenance

### Updating the Application

```bash
# Pull latest code and rebuild
git pull origin main
docker build -t WhisprMate:latest .

# Stop old container and start new one
docker stop WhisprMate
docker rm WhisprMate
./scripts/deploy.sh
```

### Backup and Restore

```bash
# Backup uploads directory
docker cp WhisprMate:/app/uploads ./backup-uploads

# Restore uploads directory
docker cp ./backup-uploads WhisprMate:/app/uploads
```

## 🧪 Testing & Validation

### Volume Mapping Tests

Use the comprehensive test script to validate your Docker setup:

```bash
# Run all volume mapping tests
./scripts/test_volume_mapping.sh

# Test Output Example:
# 🧪 WhisprMate Docker Volume Mapping Test
# ==============================================
# ✅ Container is running
# ✅ Application is accessible on port 8503
# ✅ Host-created file visible in container
# ✅ Container-created file visible on host
# ✅ Environment variables set correctly
# ✅ Directory permissions are correct
# ✅ Application configuration is valid
# ✅ Files persist across container restarts
```

### Interactive Deployment

Use the interactive deployment script for guided setup:

```bash
# Run interactive deployment with examples
./scripts/deploy_examples.sh

# Provides scenarios for:
# 1. Basic development setup
# 2. Production deployment
# 3. Network storage integration
# 4. Custom directory mapping
# 5. Multi-environment configurations
```

### Manual Testing

```bash
# Test file creation from host
echo "test from host" > uploads/host_test.txt
docker exec container_name cat /app/uploads/host_test.txt

# Test file creation from container
docker exec container_name sh -c "echo 'test from container' > /app/uploads/container_test.txt"
cat uploads/container_test.txt

# Test logging
docker exec container_name python -c "
from config.logging_config import get_logger
logger = get_logger('test')
logger.info('Test log message')
"
cat logs/whisprmate_*.log | tail -5
```

## 📁 Script Reference

### Available Scripts

- **`./scripts/test_volume_mapping.sh`** - Comprehensive volume mapping validation
- **`./scripts/deploy_examples.sh`** - Interactive deployment scenarios  
- **`./scripts/deploy.sh`** - Standard deployment script
- **`./scripts/build.sh`** - Image building script
- **`./scripts/validate-docker.sh`** - Setup validation

### Script Usage Examples

```bash
# Quick validation
./scripts/validate-docker.sh

# Standard deployment
./scripts/deploy.sh

# Custom deployment with paths
UPLOADS_HOST_PATH=/data/uploads LOGS_HOST_PATH=/data/logs ./scripts/deploy.sh

# Interactive guided setup
./scripts/deploy_examples.sh

# Comprehensive testing
./scripts/test_volume_mapping.sh
```

---

For more deployment options and advanced configurations, see the main [README.md](../README.md) and [project documentation](../docs/).
