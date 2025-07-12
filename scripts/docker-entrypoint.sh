#!/bin/bash
set -e

# Docker entrypoint script to handle permissions and startup

echo "🐳 WhisprMate Docker Entrypoint"
echo "================================="

# Function to check and fix directory permissions
fix_permissions() {
    local dir_path="$1"
    local dir_name="$2"
    
    echo "📁 Checking $dir_name directory: $dir_path"
    
    if [ -d "$dir_path" ]; then
        # Check if we can write to the directory
        if [ -w "$dir_path" ]; then
            echo "✅ $dir_name directory is writable"
        else
            echo "⚠️  $dir_name directory exists but is not writable"
            echo "   Attempting to fix permissions..."
            
            # Try to fix permissions (will work if we have sudo or are root)
            if chmod 755 "$dir_path" 2>/dev/null; then
                echo "✅ Fixed $dir_name directory permissions"
            else
                echo "❌ Cannot fix $dir_name directory permissions"
                echo "   The application will use fallback directories"
            fi
        fi
    else
        echo "📂 Creating $dir_name directory: $dir_path"
        if mkdir -p "$dir_path" 2>/dev/null; then
            chmod 755 "$dir_path" 2>/dev/null || true
            echo "✅ Created $dir_name directory"
        else
            echo "❌ Cannot create $dir_name directory"
            echo "   The application will use fallback directories"
        fi
    fi
}

# Check and fix permissions for key directories
fix_permissions "/app/uploads" "uploads"
fix_permissions "/app/logs" "logs"
fix_permissions "/app/data" "data"

# Set ownership to app user if we're running as root
if [ "$(id -u)" = "0" ]; then
    echo "🔧 Running as root, setting ownership to app user..."
    chown -R app:app /app/uploads /app/logs /app/data 2>/dev/null || true
    echo "🔄 Switching to app user..."
    exec gosu app "$@"
fi

# Test write permissions with current user
echo "🧪 Testing write permissions..."
test_write() {
    local dir_path="$1"
    local dir_name="$2"
    
    local test_file="$dir_path/.write_test_$$"
    if touch "$test_file" 2>/dev/null; then
        rm -f "$test_file" 2>/dev/null || true
        echo "✅ $dir_name directory write test successful"
        return 0
    else
        echo "❌ $dir_name directory write test failed"
        return 1
    fi
}

test_write "/app/uploads" "uploads"
test_write "/app/logs" "logs"

# Display environment info
echo "📋 Environment Information:"
echo "   User: $(whoami) ($(id))"
echo "   Working Directory: $(pwd)"
echo "   Upload Directory: /app/uploads"
echo "   Logs Directory: /app/logs"
echo "   Python: $(python --version 2>&1)"

# Display volume mount information
echo "📦 Volume Mount Information:"
if mountpoint -q /app/uploads 2>/dev/null; then
    echo "   /app/uploads is mounted from host"
else
    echo "   /app/uploads using container filesystem"
fi

if mountpoint -q /app/logs 2>/dev/null; then
    echo "   /app/logs is mounted from host"  
else
    echo "   /app/logs using container filesystem"
fi

echo "================================="
echo "🚀 Starting WhisprMate Application"
echo ""

# Execute the main command
exec "$@"
