#!/bin/bash

# Quick Test Script for WhisprMate Application
echo "🧪 Testing WhisprMate Application..."

# Test 1: Check if virtual environment exists
if [ -d ".venv" ]; then
    echo "✅ Virtual environment found"
else
    echo "❌ Virtual environment not found"
    exit 1
fi

# Test 2: Check if application is running
if ss -tulpn | grep -q ":850[1-3]"; then
    echo "✅ Streamlit application is running"
    PORT=$(ss -tulpn | grep ":850[1-3]" | head -1 | sed 's/.*:\([0-9]*\).*/\1/')
    echo "   Running on port: $PORT"
else
    echo "❌ No Streamlit application found running"
fi

# Test 3: Check key files
FILES=("main.py" "requirements.txt" "run_app.sh" "activate_env.sh")
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
    fi
done

# Test 4: Quick accessibility test
if command -v curl >/dev/null 2>&1; then
    echo "🌐 Testing application accessibility..."
    if curl -s "http://localhost:$PORT" | grep -q "Speaker Diarization\|WhisprMate"; then
        echo "✅ Application is accessible and responding"
    else
        echo "⚠️  Application may not be fully loaded yet"
    fi
else
    echo "ℹ️  curl not available for accessibility test"
fi

echo ""
echo "🎉 Test completed!"
echo "📍 Access your application at: http://localhost:$PORT"
echo "🔑 Login credentials: testuser / testpass"
