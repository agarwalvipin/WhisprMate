#!/bin/bash

# Example script showing how to run the app with custom credentials

echo "Starting Speaker Diarization App with custom authentication..."
echo "Username: myuser"
echo "Password: mypassword"
echo ""

# Run the app with custom credentials
streamlit run main.py -- --username myuser --password mypassword
