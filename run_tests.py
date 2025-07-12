#!/usr/bin/env python3
"""
Test runner for the Speaker Diarization project.
Runs all tests and provides coverage information.
"""

import sys
import os
import subprocess
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def run_tests():
    """Run all tests in the project."""
    print("🧪 Running Speaker Diarization Tests")
    print("=" * 50)
    
    # Change to project directory
    os.chdir(project_root)
    
    # Run unit tests
    print("\n📋 Running Unit Tests...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/unit/", "-v", "--tb=short"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Unit tests passed!")
            print(result.stdout)
        else:
            # Check if it's a pytest not found error
            if "No module named pytest" in result.stderr:
                raise FileNotFoundError("pytest not available")
            print("❌ Unit tests failed!")
            print(result.stdout)
            print(result.stderr)
    except (FileNotFoundError, subprocess.SubprocessError):
        print("⚠️  pytest not found. Running tests directly...")
        # Fallback to running tests directly
        test_files = list(Path("tests/unit").glob("test_*.py"))
        for test_file in test_files:
            print(f"\n🔍 Running {test_file.name}...")
            try:
                result = subprocess.run([sys.executable, str(test_file)], 
                                     capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {test_file.name} passed")
                    print(result.stdout)
                else:
                    print(f"❌ {test_file.name} failed")
                    print(result.stderr)
            except Exception as e:
                print(f"❌ Error running {test_file.name}: {e}")
    
    # Run integration tests if they exist
    integration_tests = list(Path("tests/integration").glob("test_*.py"))
    if integration_tests:
        print("\n🔗 Running Integration Tests...")
        for test_file in integration_tests:
            print(f"🔍 Running {test_file.name}...")
            try:
                result = subprocess.run([sys.executable, str(test_file)], 
                                     capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {test_file.name} passed")
                else:
                    print(f"❌ {test_file.name} failed")
                    print(result.stderr)
            except Exception as e:
                print(f"❌ Error running {test_file.name}: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Test run completed!")


if __name__ == "__main__":
    run_tests()
