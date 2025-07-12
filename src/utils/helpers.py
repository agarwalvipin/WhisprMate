"""Utility functions for file operations and formatting."""

import base64
from typing import List, Tuple

from ..core.models import AudioFile


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string
    """
    if size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes} B"


def format_duration(duration_seconds: float) -> str:
    """Format duration in human-readable format.

    Args:
        duration_seconds: Duration in seconds

    Returns:
        Formatted duration string
    """
    if duration_seconds is None:
        return "-"

    hours = int(duration_seconds // 3600)
    minutes = int((duration_seconds % 3600) // 60)
    seconds = int(duration_seconds % 60)

    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"


def sort_audio_files(files: List[AudioFile], sort_option: str) -> List[AudioFile]:
    """Sort audio files based on the given option.

    Args:
        files: List of audio files to sort
        sort_option: Sort option string

    Returns:
        Sorted list of audio files
    """
    if sort_option == "Date created (newest)":
        return sorted(files, key=lambda x: x.created_at or 0, reverse=True)
    elif sort_option == "Date created (oldest)":
        return sorted(files, key=lambda x: x.created_at or 0)
    elif sort_option == "Title (A-Z)":
        return sorted(files, key=lambda x: x.name.lower())
    elif sort_option == "Title (Z-A)":
        return sorted(files, key=lambda x: x.name.lower(), reverse=True)
    elif sort_option == "Duration (longest)":
        return sorted(files, key=lambda x: x.duration_seconds or 0, reverse=True)
    elif sort_option == "Duration (shortest)":
        return sorted(files, key=lambda x: x.duration_seconds or 0)
    else:
        return files


def filter_audio_files(files: List[AudioFile], search_query: str) -> List[AudioFile]:
    """Filter audio files based on search query.

    Args:
        files: List of audio files to filter
        search_query: Search query string

    Returns:
        Filtered list of audio files
    """
    if not search_query:
        return files

    query_lower = search_query.lower()
    return [file for file in files if query_lower in file.name.lower()]


def estimate_processing_time(duration_seconds: float, model_size: str = "base") -> str:
    """Estimate processing time for audio file.

    Args:
        duration_seconds: Duration of audio file
        model_size: Whisper model size

    Returns:
        Formatted estimated time string
    """
    if duration_seconds is None:
        return "Unknown"

    # Multipliers based on model size (CPU processing)
    multipliers = {"tiny": 1.0, "base": 2.0, "small": 3.0, "medium": 4.0, "large": 5.0}

    multiplier = multipliers.get(model_size, 3.0)
    estimated_seconds = duration_seconds * multiplier

    return format_duration(estimated_seconds)


def validate_file_upload(uploaded_file, max_size_mb: int = 50) -> Tuple[bool, str]:
    """Validate uploaded file.

    Args:
        uploaded_file: Streamlit uploaded file object
        max_size_mb: Maximum file size in MB

    Returns:
        Tuple of (is_valid, error_message)
    """
    if uploaded_file is None:
        return False, "No file uploaded"

    # Check file size
    max_size_bytes = max_size_mb * 1024 * 1024
    if uploaded_file.size > max_size_bytes:
        return False, f"File too large. Maximum size is {max_size_mb}MB"

    # Check file extension
    allowed_extensions = [".wav", ".mp3"]
    file_extension = "." + uploaded_file.name.split(".")[-1].lower()
    if file_extension not in allowed_extensions:
        return False, f"Unsupported file format. Allowed: {', '.join(allowed_extensions)}"

    return True, ""


def encode_audio_for_player(audio_bytes: bytes) -> str:
    """Encode audio bytes for HTML player.

    Args:
        audio_bytes: Raw audio bytes

    Returns:
        Base64 encoded audio string
    """
    return base64.b64encode(audio_bytes).decode()


def get_audio_mime_type(filename: str) -> str:
    """Get MIME type for audio file.

    Args:
        filename: Name of audio file

    Returns:
        MIME type string
    """
    if filename.lower().endswith(".wav"):
        return "audio/wav"
    elif filename.lower().endswith(".mp3"):
        return "audio/mp3"
    else:
        return "audio/mpeg"
