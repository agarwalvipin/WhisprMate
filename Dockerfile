# Use custom base image with uv and system dependencies pre-installed
FROM whisprmate-base:latest

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Copy only dependency files first for better cache utilization
COPY pyproject.toml requirements.txt ./

# Install Python dependencies using uv
RUN uv venv && \
    uv pip install -r requirements.txt && \
    uv pip install \
    openai-whisper \
    pyannote.audio \
    torch \
    torchaudio \
    --extra-index-url https://download.pytorch.org/whl/cpu

# Copy the rest of the application code
COPY . .

# Create necessary directories with proper permissions and make scripts executable
RUN mkdir -p uploads data/samples static templates logs && \
    chmod +x scripts/*.sh && \
    chmod +x run_tests.py && \
    chmod -R 777 uploads logs data

# Set up entrypoint script
RUN chmod +x scripts/docker-entrypoint.sh

# Don't switch to app user yet - let entrypoint handle it
# USER app

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["./scripts/docker-entrypoint.sh"]
CMD ["uv", "run", "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true", "--server.fileWatcherType=none", "--browser.gatherUsageStats=false"]
