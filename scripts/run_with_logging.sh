#!/bin/bash

# Example script to run WhisprMate with different logging levels

# For debugging - verbose logging
echo "🔍 Running with DEBUG logging..."
LOG_LEVEL=DEBUG streamlit run main.py -- --username admin --password admin

# For production - minimal logging  
# LOG_LEVEL=WARNING streamlit run main.py -- --username admin --password admin

# For development - balanced logging
# LOG_LEVEL=INFO streamlit run main.py -- --username admin --password admin

# To save logs to a specific file
# LOG_FILE=logs/whisprmate_debug.log LOG_LEVEL=DEBUG streamlit run main.py

# Example Docker run with logging
# docker run -p 8501:8501 \
#   -e LOG_LEVEL=DEBUG \
#   -e LOG_FILE=/app/logs/whisprmate.log \
#   -v $(pwd)/logs:/app/logs \
#   whisprmate
