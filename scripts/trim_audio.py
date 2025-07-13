#!/usr/bin/env python3
"""
Audio trimming script for WhisprMate.

This script trims WAV files to a specified duration in minutes.
It supports both FFmpeg and soundfile backends for audio processing.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

try:
    import soundfile as sf
    HAS_SOUNDFILE = True
except ImportError:
    HAS_SOUNDFILE = False


def check_ffmpeg() -> bool:
    """Check if FFmpeg is available in the system."""
    try:
        subprocess.run(
            ["ffmpeg", "-version"], 
            capture_output=True, 
            check=True,
            timeout=10
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False


def trim_with_ffmpeg(
    input_file: Path, 
    output_file: Path, 
    duration_minutes: float,
    start_time: float = 0.0
) -> bool:
    """
    Trim audio file using FFmpeg.
    
    Args:
        input_file: Path to input WAV file
        output_file: Path to output WAV file
        duration_minutes: Duration to trim in minutes
        start_time: Start time offset in minutes (default: 0.0)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Convert minutes to seconds for FFmpeg
        start_seconds = start_time * 60
        duration_seconds = duration_minutes * 60
        
        cmd = [
            "ffmpeg",
            "-i", str(input_file),
            "-ss", str(start_seconds),
            "-t", str(duration_seconds),
            "-c", "copy",  # Copy without re-encoding for speed
            "-y",  # Overwrite output file
            str(output_file)
        ]
        
        print(f"Running FFmpeg command: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode != 0:
            print(f"FFmpeg error: {result.stderr}")
            return False
            
        print(f"Successfully trimmed audio with FFmpeg")
        return True
        
    except subprocess.TimeoutExpired:
        print("FFmpeg operation timed out")
        return False
    except Exception as e:
        print(f"Error using FFmpeg: {e}")
        return False


def trim_with_soundfile(
    input_file: Path, 
    output_file: Path, 
    duration_minutes: float,
    start_time: float = 0.0
) -> bool:
    """
    Trim audio file using soundfile.
    
    Args:
        input_file: Path to input WAV file
        output_file: Path to output WAV file
        duration_minutes: Duration to trim in minutes
        start_time: Start time offset in minutes (default: 0.0)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Read audio file info
        with sf.SoundFile(input_file) as f:
            sample_rate = f.samplerate
            channels = f.channels
            total_frames = len(f)
            total_duration = total_frames / sample_rate
            
        print(f"Input file info: {total_duration:.2f}s, {sample_rate}Hz, {channels} channels")
        
        # Calculate frame positions
        start_frame = int(start_time * 60 * sample_rate)
        duration_frames = int(duration_minutes * 60 * sample_rate)
        
        # Validate bounds
        if start_frame >= total_frames:
            print(f"Error: Start time ({start_time:.2f} min) exceeds file duration ({total_duration/60:.2f} min)")
            return False
            
        end_frame = min(start_frame + duration_frames, total_frames)
        actual_duration = (end_frame - start_frame) / sample_rate / 60
        
        print(f"Trimming from {start_time:.2f} min for {actual_duration:.2f} min")
        
        # Read and write audio data
        with sf.SoundFile(input_file) as f:
            f.seek(start_frame)
            data = f.read(frames=end_frame - start_frame)
            
        sf.write(output_file, data, sample_rate)
        
        print(f"Successfully trimmed audio with soundfile")
        return True
        
    except Exception as e:
        print(f"Error using soundfile: {e}")
        return False


def validate_input_file(file_path: Path) -> bool:
    """Validate that the input file exists and is a WAV file."""
    if not file_path.exists():
        print(f"Error: Input file does not exist: {file_path}")
        return False
        
    if not file_path.is_file():
        print(f"Error: Path is not a file: {file_path}")
        return False
        
    if file_path.suffix.lower() != '.wav':
        print(f"Warning: File does not have .wav extension: {file_path}")
        
    return True


def generate_output_filename(input_file: Path, duration_minutes: float, start_time: float = 0.0) -> Path:
    """Generate output filename based on input file and trimming parameters."""
    stem = input_file.stem
    suffix = input_file.suffix
    
    if start_time > 0:
        output_name = f"{stem}_trimmed_{start_time:.1f}m-{duration_minutes:.1f}m{suffix}"
    else:
        output_name = f"{stem}_trimmed_{duration_minutes:.1f}m{suffix}"
        
    return input_file.parent / output_name


def main():
    """Main function to handle command line arguments and execute trimming."""
    parser = argparse.ArgumentParser(
        description="Trim WAV files to specified duration in minutes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Trim to 5 minutes from the beginning
  python trim_audio.py input.wav 5
  
  # Trim to 3 minutes starting from 2 minutes
  python trim_audio.py input.wav 3 --start 2
  
  # Specify custom output file
  python trim_audio.py input.wav 5 --output trimmed_audio.wav
  
  # Force use of soundfile backend
  python trim_audio.py input.wav 5 --backend soundfile
        """
    )
    
    parser.add_argument(
        "input_file",
        type=Path,
        help="Path to input WAV file"
    )
    
    parser.add_argument(
        "duration",
        type=float,
        help="Duration to trim in minutes"
    )
    
    parser.add_argument(
        "--start",
        type=float,
        default=0.0,
        help="Start time offset in minutes (default: 0.0)"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output file path (default: auto-generated)"
    )
    
    parser.add_argument(
        "--backend",
        choices=["auto", "ffmpeg", "soundfile"],
        default="auto",
        help="Audio processing backend to use (default: auto)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    if args.duration <= 0:
        print("Error: Duration must be positive")
        sys.exit(1)
        
    if args.start < 0:
        print("Error: Start time cannot be negative")
        sys.exit(1)
        
    if not validate_input_file(args.input_file):
        sys.exit(1)
    
    # Generate output filename if not provided
    if args.output is None:
        args.output = generate_output_filename(args.input_file, args.duration, args.start)
        
    if args.verbose:
        print(f"Input file: {args.input_file}")
        print(f"Output file: {args.output}")
        print(f"Duration: {args.duration} minutes")
        print(f"Start time: {args.start} minutes")
        print(f"Backend: {args.backend}")
    
    # Check available backends
    has_ffmpeg = check_ffmpeg()
    has_soundfile = HAS_SOUNDFILE
    
    if args.verbose:
        print(f"FFmpeg available: {has_ffmpeg}")
        print(f"soundfile available: {has_soundfile}")
    
    # Select backend
    backend = args.backend
    if backend == "auto":
        if has_ffmpeg:
            backend = "ffmpeg"
        elif has_soundfile:
            backend = "soundfile"
        else:
            print("Error: No audio processing backend available")
            print("Please install FFmpeg or soundfile library")
            sys.exit(1)
    
    # Validate selected backend
    if backend == "ffmpeg" and not has_ffmpeg:
        print("Error: FFmpeg not available")
        sys.exit(1)
    elif backend == "soundfile" and not has_soundfile:
        print("Error: soundfile library not available")
        print("Install with: pip install soundfile")
        sys.exit(1)
    
    # Perform trimming
    print(f"Trimming audio using {backend} backend...")
    
    success = False
    if backend == "ffmpeg":
        success = trim_with_ffmpeg(args.input_file, args.output, args.duration, args.start)
    elif backend == "soundfile":
        success = trim_with_soundfile(args.input_file, args.output, args.duration, args.start)
    
    if success:
        print(f"Audio trimmed successfully!")
        print(f"Output saved to: {args.output}")
        
        # Show file sizes
        input_size = args.input_file.stat().st_size / (1024 * 1024)
        output_size = args.output.stat().st_size / (1024 * 1024)
        print(f"Input size: {input_size:.1f} MB")
        print(f"Output size: {output_size:.1f} MB")
    else:
        print("Error: Failed to trim audio file")
        sys.exit(1)


if __name__ == "__main__":
    main()
