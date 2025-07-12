# Use Python 3.11 slim base image for better performance and smaller size
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies for audio processing
RUN apt-get update && apt-get install -y \
    # Audio processing libraries
    ffmpeg \
    libsndfile1 \
    libsox-fmt-all \
    sox \
    # Build dependencies
    gcc \
    g++ \
    make \
    # Git for installing packages from git repos
    git \
    # curl for health checks
    curl \
    # gosu for proper user switching in entrypoint
    gosu \
    # Clean up to reduce image size
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    # Install additional ML dependencies for audio processing
    pip install \
    openai-whisper \
    pyannote.audio \
    torch \
    torchaudio \
    --extra-index-url https://download.pytorch.org/whl/cpu

# Copy the application code
COPY . .

# Create necessary directories with proper permissions
RUN mkdir -p uploads data/samples static templates logs && \
    # Make scripts executable
    chmod +x scripts/*.sh && \
    chmod +x run_tests.py && \
    # Set proper permissions for directories
    chmod -R 777 uploads logs data

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app

# Set up entrypoint script
RUN chmod +x scripts/docker-entrypoint.sh

# Don't switch to app user yet - let entrypoint handle it
# USER app

# Expose Streamlit port
EXPOSE 8501

# Health check to ensure the app is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Default command to run the Streamlit app
ENTRYPOINT ["./scripts/docker-entrypoint.sh"]
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true", "--server.fileWatcherType=none", "--browser.gatherUsageStats=false"]
