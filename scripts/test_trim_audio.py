#!/usr/bin/env python3
"""
Test script for audio trimming functionality.
This creates a mock test to verify the script logic works.
"""

import tempfile
from pathlib import Path
import sys
import os

# Add the scripts directory to the path so we can import trim_audio
sys.path.insert(0, str(Path(__file__).parent))

def test_basic_functionality():
    """Test basic argument parsing and validation."""
    print("Testing basic functionality...")
    
    # Create a temporary file to simulate a WAV file
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
        temp_path = Path(temp_file.name)
        temp_file.write(b"fake wav data")
    
    try:
        # Import the functions from our script
        from trim_audio import validate_input_file, generate_output_filename, check_ffmpeg
        
        # Test file validation
        assert validate_input_file(temp_path) == True
        print("✓ File validation works")
        
        # Test output filename generation
        output_path = generate_output_filename(temp_path, 5.0)
        expected_suffix = "_trimmed_5.0m.wav"
        assert str(output_path).endswith(expected_suffix)
        print("✓ Output filename generation works")
        
        # Test with start time
        output_path_with_start = generate_output_filename(temp_path, 3.0, 1.5)
        expected_suffix_with_start = "_trimmed_1.5m-3.0m.wav"
        assert str(output_path_with_start).endswith(expected_suffix_with_start)
        print("✓ Output filename with start time works")
        
        # Test FFmpeg detection
        has_ffmpeg = check_ffmpeg()
        print(f"✓ FFmpeg detection works (found: {has_ffmpeg})")
        
        print("All basic functionality tests passed!")
        
    finally:
        # Clean up
        temp_path.unlink()

if __name__ == "__main__":
    test_basic_functionality()
