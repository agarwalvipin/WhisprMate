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

| Variable             | Default | Description                               |
| -------------------- | ------- | ----------------------------------------- |
| `STREAMLIT_USERNAME` | `admin` | Default login username                    |
| `STREAMLIT_PASSWORD` | `admin` | Default login password                    |
| `HF_TOKEN`           | -       | HuggingFace token for speaker diarization |

### Ports

- **8501**: Streamlit web interface

### Volumes

- `/app/uploads`: User uploaded audio files
- `/app/data`: Sample data and outputs
- `/app/.env`: Environment variables file (optional)

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

---

For more deployment options and advanced configurations, see the main [README.md](../README.md) and [project documentation](../docs/).
