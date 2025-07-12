# Docker Volume Mapping Guide

## Overview

WhisprMate supports flexible Docker volume mapping to enable persistent storage, custom directory paths, and integration with network storage systems.

## Features

- **Persistent Upload Storage**: User files persist across container restarts
- **Custom Host Directories**: Map uploads and logs to any host directory
- **Environment Variable Configuration**: Flexible deployment configuration
- **Network Storage Support**: Compatible with NFS, SMB, and cloud storage
- **Automated Testing**: Comprehensive validation scripts

## Configuration

### Environment Variables

| Variable            | Default     | Description                                    |
| ------------------- | ----------- | ---------------------------------------------- |
| `UPLOADS_HOST_PATH` | `./uploads` | Host directory path for uploads mapping       |
| `LOGS_HOST_PATH`    | `./logs`    | Host directory path for logs mapping          |
| `UPLOADS_DIR`       | `/app/uploads` | Container uploads directory override        |

### Volume Mappings

| Container Path  | Host Path (Default) | Purpose                     |
| --------------- | ------------------- | --------------------------- |
| `/app/uploads`  | `./uploads`         | User uploaded audio files   |
| `/app/logs`     | `./logs`            | Application and error logs   |
| `/app/data`     | `./data`            | Sample data and outputs     |

## Basic Usage

### Docker Run Commands

```bash
# Basic volume mapping
docker run -p 8501:8501 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/logs:/app/logs \
  whisprmate

# Custom directories
docker run -p 8501:8501 \
  -v /custom/uploads:/app/uploads \
  -v /custom/logs:/app/logs \
  whisprmate

# With environment variables
docker run -p 8501:8501 \
  -e UPLOADS_HOST_PATH=/custom/uploads \
  -e LOGS_HOST_PATH=/custom/logs \
  -v /custom/uploads:/app/uploads \
  -v /custom/logs:/app/logs \
  whisprmate
```

### Docker Compose

```yaml
# docker-compose.yml example
version: '3.8'
services:
  whisprmate:
    build: .
    ports:
      - "8501:8501"
    environment:
      - UPLOADS_HOST_PATH=${UPLOADS_HOST_PATH:-./uploads}
      - LOGS_HOST_PATH=${LOGS_HOST_PATH:-./logs}
    volumes:
      - ${UPLOADS_HOST_PATH:-./uploads}:/app/uploads
      - ${LOGS_HOST_PATH:-./logs}:/app/logs
```

```bash
# Usage with environment variables
UPLOADS_HOST_PATH=/data/uploads \
LOGS_HOST_PATH=/data/logs \
docker-compose up -d
```

## Advanced Deployment Scenarios

### Network Storage Integration

```bash
# NFS storage
UPLOADS_HOST_PATH=/mnt/nfs-storage/whisprmate/uploads \
LOGS_HOST_PATH=/mnt/nfs-storage/whisprmate/logs \
docker run -p 8501:8501 \
  -v /mnt/nfs-storage/whisprmate/uploads:/app/uploads \
  -v /mnt/nfs-storage/whisprmate/logs:/app/logs \
  whisprmate

# SMB/CIFS storage
UPLOADS_HOST_PATH=/mnt/smb-share/uploads \
LOGS_HOST_PATH=/mnt/smb-share/logs \
docker run -p 8501:8501 \
  -v /mnt/smb-share/uploads:/app/uploads \
  -v /mnt/smb-share/logs:/app/logs \
  whisprmate
```

### Multi-Environment Setup

```bash
# Development environment
UPLOADS_HOST_PATH=/home/dev/whisprmate/uploads \
LOGS_HOST_PATH=/home/dev/whisprmate/logs \
LOG_LEVEL=DEBUG \
./scripts/deploy.sh

# Staging environment
UPLOADS_HOST_PATH=/var/staging/whisprmate/uploads \
LOGS_HOST_PATH=/var/staging/whisprmate/logs \
LOG_LEVEL=INFO \
./scripts/deploy.sh

# Production environment
UPLOADS_HOST_PATH=/var/production/whisprmate/uploads \
LOGS_HOST_PATH=/var/production/whisprmate/logs \
LOG_LEVEL=WARNING \
./scripts/deploy.sh
```

### Shared Storage for Multiple Instances

```bash
# Multiple containers sharing storage
SHARED_UPLOADS=/shared/storage/whisprmate/uploads
SHARED_LOGS=/shared/storage/whisprmate/logs

# Instance 1
docker run -d --name whisprmate-1 -p 8501:8501 \
  -v $SHARED_UPLOADS:/app/uploads \
  -v $SHARED_LOGS:/app/logs \
  whisprmate

# Instance 2
docker run -d --name whisprmate-2 -p 8502:8501 \
  -v $SHARED_UPLOADS:/app/uploads \
  -v $SHARED_LOGS:/app/logs \
  whisprmate
```

## Testing & Validation

### Automated Testing

Use the comprehensive test script to validate volume mapping:

```bash
# Run all volume mapping tests
./scripts/test_volume_mapping.sh

# Expected output:
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

### Manual Testing

```bash
# Test 1: Host to Container Mapping
echo "test content" > uploads/test.txt
docker exec container_name cat /app/uploads/test.txt

# Test 2: Container to Host Mapping
docker exec container_name sh -c "echo 'from container' > /app/uploads/container_test.txt"
cat uploads/container_test.txt

# Test 3: Persistence Across Restarts
echo "persistence test" > uploads/persist_test.txt
docker restart container_name
docker exec container_name cat /app/uploads/persist_test.txt

# Test 4: Log File Creation
docker exec container_name python -c "
from config.logging_config import get_logger
logger = get_logger('test')
logger.info('Test log message')
"
cat logs/whisprmate_*.log | grep "Test log message"
```

### Interactive Deployment Guide

Use the interactive script for guided deployment:

```bash
./scripts/deploy_examples.sh

# Provides scenarios for:
# 1. Basic development setup
# 2. Production deployment with custom paths
# 3. Network storage integration
# 4. Multi-environment configuration
# 5. Shared storage setup
```

## Permission Management

### Docker User Mapping

For proper file permissions, especially in production:

```bash
# Run with specific user/group
docker run -p 8501:8501 \
  --user $(id -u):$(id -g) \
  -v /custom/uploads:/app/uploads \
  -v /custom/logs:/app/logs \
  whisprmate

# Create directories with proper permissions
sudo mkdir -p /var/whisprmate/{uploads,logs}
sudo chown $(id -u):$(id -g) /var/whisprmate/{uploads,logs}
sudo chmod 755 /var/whisprmate/{uploads,logs}
```

### SELinux Considerations

On SELinux-enabled systems:

```bash
# Set SELinux context for Docker volumes
sudo setsebool -P container_manage_cgroup on
sudo semanage fcontext -a -t container_file_t "/var/whisprmate(/.*)?"
sudo restorecon -R /var/whisprmate
```

## Backup and Recovery

### Backup Strategies

```bash
# Simple backup of uploads
tar -czf whisprmate-backup-$(date +%Y%m%d).tar.gz uploads/ logs/

# Rsync to remote location
rsync -av uploads/ user@backup-server:/backups/whisprmate/uploads/
rsync -av logs/ user@backup-server:/backups/whisprmate/logs/

# Database-style backup with timestamps
BACKUP_DIR="/backups/whisprmate/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r uploads/ "$BACKUP_DIR/"
cp -r logs/ "$BACKUP_DIR/"
```

### Recovery Procedures

```bash
# Restore from backup
tar -xzf whisprmate-backup-20250712.tar.gz

# Restore specific files
rsync -av backup-server:/backups/whisprmate/uploads/ uploads/

# Container restart after restoration
docker restart whisprmate-container
```

## Monitoring and Maintenance

### Storage Monitoring

```bash
# Monitor disk usage
df -h uploads/ logs/

# Check directory sizes
du -sh uploads/ logs/

# Monitor file count
find uploads/ -type f | wc -l
find logs/ -type f | wc -l

# Monitor recent activity
find uploads/ -type f -mtime -1  # Files modified in last 24 hours
find logs/ -type f -mtime -7     # Log files from last week
```

### Log Rotation

```bash
# Manual log rotation
mkdir -p logs/archive
mv logs/whisprmate_*.log logs/archive/
# Application will create new log files automatically

# Automated rotation with logrotate
# /etc/logrotate.d/whisprmate
/var/whisprmate/logs/whisprmate_*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 appuser appgroup
}
```

### Cleanup Scripts

```bash
# Clean old uploads (older than 30 days)
find uploads/ -type f -mtime +30 -delete

# Clean old logs (keep last 7 days)
find logs/ -name "whisprmate_*.log" -mtime +7 -delete

# Clean temporary files
find uploads/ -name "*.tmp" -delete
find uploads/ -name ".DS_Store" -delete
```

## Troubleshooting

### Common Issues

1. **Permission Denied Errors**
   ```bash
   # Check directory permissions
   ls -la uploads/ logs/
   
   # Fix permissions
   sudo chown -R $(id -u):$(id -g) uploads/ logs/
   sudo chmod -R 755 uploads/ logs/
   ```

2. **Files Not Appearing**
   ```bash
   # Check volume mounts
   docker inspect container_name | grep -A 10 "Mounts"
   
   # Verify paths inside container
   docker exec container_name ls -la /app/uploads /app/logs
   ```

3. **Storage Full**
   ```bash
   # Check disk space
   df -h /var/whisprmate
   
   # Clean up old files
   find /var/whisprmate -type f -mtime +30 -delete
   ```

4. **SELinux Denials**
   ```bash
   # Check SELinux logs
   sudo ausearch -m avc -ts recent
   
   # Allow Docker access
   sudo setsebool -P container_manage_cgroup on
   ```

### Debug Commands

```bash
# Test volume mapping
./scripts/test_volume_mapping.sh

# Check container environment
docker exec container_name env | grep -E "(UPLOADS|LOGS)"

# Verify application configuration
docker exec container_name python -c "
from config.settings import AppConfig
print('Upload dir:', AppConfig.get_upload_dir())
print('Logs dir:', AppConfig.get_logs_dir())
"

# Monitor real-time file changes
docker exec container_name tail -f /app/logs/whisprmate_*.log
```

## Best Practices

### Security

- Use non-root user in containers
- Set appropriate file permissions (644 for files, 755 for directories)
- Regularly audit access to mapped directories
- Use read-only mounts where appropriate

### Performance

- Use local storage for frequently accessed files
- Consider SSD storage for uploads directory
- Implement log rotation to prevent disk space issues
- Monitor I/O performance on mapped volumes

### Reliability

- Use redundant storage for critical data
- Implement regular backups
- Test disaster recovery procedures
- Monitor storage health and capacity

### Scalability

- Plan for growth in upload volume
- Consider distributed storage solutions
- Implement automated cleanup policies
- Use container orchestration for multi-instance deployments

This volume mapping system provides flexible, persistent storage solutions that can adapt to various deployment scenarios while maintaining data integrity and performance.
