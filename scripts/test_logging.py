#!/usr/bin/env python3
"""
Simple test script to verify logging configuration works.
Run this to test logging before running the full application.
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.logging_config import get_logger, setup_logging


def test_logging():
    """Test the logging configuration."""
    print("🧪 Testing WhisprMate logging configuration...")

    # Setup logging
    setup_logging(log_level="DEBUG")

    # Test different loggers
    main_logger = get_logger("main")
    audio_logger = get_logger("audio")
    auth_logger = get_logger("auth")
    file_logger = get_logger("file")
    transcript_logger = get_logger("transcript")

    # Test different log levels
    print("\n📝 Testing log levels:")
    main_logger.debug("This is a DEBUG message")
    main_logger.info("This is an INFO message")
    main_logger.warning("This is a WARNING message")
    main_logger.error("This is an ERROR message")

    print("\n🎙️ Testing audio logger:")
    audio_logger.info("Audio processing initialized")
    audio_logger.debug("Processing audio file: test.wav")
    audio_logger.warning("No HF_TOKEN found, using simulation mode")

    print("\n🔐 Testing auth logger:")
    auth_logger.info("Authentication service started")
    auth_logger.debug("Login attempt for user: admin")

    print("\n📁 Testing file logger:")
    file_logger.info("File manager initialized")
    file_logger.debug("Upload directory created: /app/uploads")

    print("\n📄 Testing transcript logger:")
    transcript_logger.info("Saving transcript for audio.wav")
    transcript_logger.debug("Transcript saved successfully")

    print("\n✅ Logging test completed!")
    print("📋 Check the logs/ directory for log files")

    # Show log directory contents
    logs_dir = Path("logs")
    if logs_dir.exists():
        print(f"\n📂 Log files in {logs_dir}:")
        for log_file in logs_dir.glob("*.log"):
            size = log_file.stat().st_size
            print(f"  - {log_file.name} ({size} bytes)")


if __name__ == "__main__":
    test_logging()
