# Logging System Documentation

## Overview

WhisprMate includes a comprehensive logging system designed for debugging, monitoring, and troubleshooting in both development and production environments.

## Architecture

### Centralized Configuration

The logging system is centralized in `config/logging_config.py` and provides:

- **Multiple log levels**: DEBUG, INFO, WARNING, ERROR
- **Multiple output destinations**: Console, file, error-specific
- **Timestamped log files**: Automatic timestamp-based file naming
- **Component-specific loggers**: Separate loggers for different services

### Log File Structure

```
logs/
├── whisprmate_20250712_143022.log    # Main application log (timestamped)
├── errors.log                        # Error-specific entries
└── [component]_*.log                 # Component-specific logs (if configured)
```

## Configuration

### Environment Variables

| Variable         | Default | Description                                    |
| ---------------- | ------- | ---------------------------------------------- |
| `LOG_LEVEL`      | `INFO`  | Global logging level                           |
| `LOGS_HOST_PATH` | `./logs`| Host directory for log files (Docker)         |
| `LOG_FILE`       | -       | Override default log file path                 |

### Log Levels

- **DEBUG**: Detailed debugging information
  - File operations and paths
  - Processing steps and intermediate results
  - Configuration loading details
  - Request/response data

- **INFO**: General application flow
  - Application startup/shutdown
  - User authentication events
  - File upload/processing completion
  - Service initialization

- **WARNING**: Important notices and fallbacks
  - Missing HuggingFace token (simulation mode)
  - Configuration fallbacks
  - Performance warnings
  - Deprecated feature usage

- **ERROR**: Error conditions and failures
  - Processing failures
  - Authentication errors
  - File system errors
  - Service unavailability

## Usage Examples

### Basic Usage

```python
from config.logging_config import get_logger

# Get a logger for your component
logger = get_logger(__name__)

# Log at different levels
logger.debug("Detailed debug information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred")
```

### Service-Specific Logging

```python
# Audio processing service
from config.logging_config import get_logger
logger = get_logger('audio_processor')

logger.info("Starting audio processing for file: %s", filename)
logger.debug("Processing with model: %s, language: %s", model, language)
logger.warning("HF_TOKEN not found, using simulation mode")
logger.error("Failed to process audio: %s", str(error))
```

### Application Startup

```python
# Main application
from config.logging_config import setup_logging, get_logger

# Initialize logging system
setup_logging()
logger = get_logger('main')

logger.info("WhisprMate application starting")
logger.info("Logging configured - Level: %s", log_level)
```

## Development Usage

### Local Development

```bash
# Debug mode
LOG_LEVEL=DEBUG streamlit run main.py

# Info mode (default)
streamlit run main.py

# Custom log file
LOG_FILE=debug.log LOG_LEVEL=DEBUG streamlit run main.py
```

### Docker Development

```bash
# Debug logging in container
docker run -p 8501:8501 \
  -e LOG_LEVEL=DEBUG \
  -v $(pwd)/logs:/app/logs \
  whisprmate

# View logs in real-time
docker logs -f container_name

# Access log files
cat logs/whisprmate_*.log | tail -50
```

## Production Usage

### Production Logging

```bash
# Production deployment with info logging
docker run -d \
  --name whisprmate-prod \
  -e LOG_LEVEL=INFO \
  -v /var/logs/whisprmate:/app/logs \
  whisprmate

# Log rotation and monitoring
# Use logrotate for automatic log rotation
# Monitor error.log for critical issues
```

### Log Monitoring

```bash
# Monitor error logs
tail -f logs/errors.log

# Search for specific errors
grep -i "error\|failed" logs/whisprmate_*.log

# Monitor specific component
grep "audio_processor" logs/whisprmate_*.log | tail -20

# Check application startup
grep "WhisprMate application starting" logs/whisprmate_*.log
```

## Log Analysis

### Common Log Patterns

```bash
# Authentication events
grep "User.*authenticated\|Login attempt" logs/whisprmate_*.log

# File processing
grep "Processing.*file\|Upload completed" logs/whisprmate_*.log

# Errors and warnings
grep -E "(ERROR|WARNING)" logs/whisprmate_*.log

# Performance monitoring
grep "Processing time\|Duration" logs/whisprmate_*.log
```

### Debug Session Example

```bash
# Start debug session
LOG_LEVEL=DEBUG streamlit run main.py

# Upload a file and check logs
tail -f logs/whisprmate_*.log | grep -E "(DEBUG|upload|process)"

# Check for specific errors
grep -A 5 -B 5 "ERROR" logs/whisprmate_*.log
```

## Integration with External Tools

### Log Aggregation

For production environments, integrate with log aggregation tools:

```yaml
# Example: Fluentd configuration
<source>
  @type tail
  path /var/logs/whisprmate/whisprmate_*.log
  pos_file /var/log/fluentd/whisprmate.log.pos
  tag whisprmate.app
  format multiline
  format_firstline /^\d{4}-\d{2}-\d{2}/
</source>
```

### Monitoring Alerts

```bash
# Example: Monitor error rate
ERROR_COUNT=$(grep -c "ERROR" logs/whisprmate_*.log)
if [ $ERROR_COUNT -gt 10 ]; then
    echo "High error rate detected: $ERROR_COUNT errors"
    # Send alert
fi
```

## Troubleshooting

### Common Issues

1. **Logs not appearing**
   - Check LOG_LEVEL environment variable
   - Verify logs directory permissions
   - Ensure logging is initialized with `setup_logging()`

2. **Log files not created**
   - Check directory permissions (especially in Docker)
   - Verify LOGS_HOST_PATH is correctly mounted
   - Check disk space availability

3. **Missing log entries**
   - Verify correct logger name usage
   - Check if log level is appropriate
   - Ensure logger is called after setup_logging()

### Debug Commands

```bash
# Check logging configuration
python -c "
from config.logging_config import setup_logging, get_logger
setup_logging()
logger = get_logger('test')
logger.info('Test message')
print('Logging test completed')
"

# Verify log file creation
ls -la logs/

# Check log permissions in Docker
docker exec container_name ls -la /app/logs/
docker exec container_name whoami
```

## Best Practices

### Development

- Use DEBUG level for detailed troubleshooting
- Log important state changes and decisions
- Include relevant context (file names, user IDs, etc.)
- Avoid logging sensitive information (passwords, tokens)

### Production

- Use INFO or WARNING level for production
- Implement log rotation to manage disk space
- Monitor error logs for critical issues
- Set up alerts for high error rates

### Code Guidelines

```python
# Good logging practices
logger.info("Processing audio file: %s", filename)
logger.debug("Configuration loaded: %s", config_dict)
logger.warning("Using fallback configuration due to: %s", reason)
logger.error("Failed to process %s: %s", filename, str(exception))

# Avoid
logger.info(f"Processing {filename}")  # Use % formatting
logger.debug("Starting processing...")  # Too vague
logger.error("Error occurred")  # No context
```

## Configuration Reference

### Complete Configuration Example

```python
# config/logging_config.py usage
import logging
from config.logging_config import setup_logging, get_logger

# Initialize logging (call once at application start)
setup_logging()

# Get loggers for different components
main_logger = get_logger('main')
auth_logger = get_logger('auth')
audio_logger = get_logger('audio_processor')

# Use throughout application
main_logger.info("Application initialized")
auth_logger.info("User %s authenticated", username)
audio_logger.debug("Processing with parameters: %s", params)
```

This logging system provides comprehensive visibility into application behavior while maintaining performance and security best practices.
