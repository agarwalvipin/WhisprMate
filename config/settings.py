"""Application configuration settings."""

import os
from pathlib import Path
from typing import List

from config.logging_config import get_logger

logger = get_logger("config")


class AppConfig:
    """Application configuration settings."""

    # File settings - Support environment variable for uploads directory
    _DEFAULT_UPLOAD_DIR: Path = Path("uploads")
    MAX_FILE_SIZE_MB: int = 50
    SUPPORTED_FORMATS: List[str] = ["wav", "mp3"]

    # Processing settings
    DEFAULT_MODEL_SIZE: str = "base"
    DEFAULT_LANGUAGE: str = "auto"
    CPU_MULTIPLIER: float = 3.0
    GPU_MULTIPLIER: float = 1.0

    # UI settings
    PAGE_TITLE: str = "Speaker Diarization App"
    LAYOUT: str = "wide"

    # Security settings
    ENABLE_AUTH: bool = False  # Set to True in production

    @classmethod
    def get_upload_dir(cls) -> Path:
        """Get upload directory path from environment variable or default.

        Environment Variables:
            UPLOADS_DIR: Custom path for uploads directory
            UPLOADS_HOST_PATH: Host path for Docker volume mapping

        Returns:
            Path: Upload directory path
        """
        # Check for custom uploads directory from environment
        uploads_dir = os.getenv("UPLOADS_DIR")
        if uploads_dir:
            upload_path = Path(uploads_dir)
            logger.info(f"Using custom uploads directory from UPLOADS_DIR: {upload_path}")
        else:
            # Check for host path mapping (useful for Docker)
            host_path = os.getenv("UPLOADS_HOST_PATH")
            if host_path:
                upload_path = Path("/app/uploads")  # Container path
                logger.info(f"Using Docker host path mapping: {host_path} -> {upload_path}")
            else:
                upload_path = cls._DEFAULT_UPLOAD_DIR
                logger.debug(f"Using default uploads directory: {upload_path}")

        # Create directory if it doesn't exist
        upload_path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Upload directory ensured: {upload_path}")

        return upload_path

    @classmethod
    def get_max_file_size_bytes(cls) -> int:
        """Get maximum file size in bytes."""
        return cls.MAX_FILE_SIZE_MB * 1024 * 1024

    @classmethod
    def is_supported_format(cls, filename: str) -> bool:
        """Check if file format is supported."""
        return any(filename.lower().endswith(f".{fmt}") for fmt in cls.SUPPORTED_FORMATS)


class UIConfig:
    """UI-specific configuration and styling."""

    MAIN_HEADER_CSS = """
        <style>
        .main-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
        }
        .main-header h1 {
            color: white;
            margin: 0;
            font-size: 2.5rem;
            font-weight: 600;
        }
        .main-header p {
            color: rgba(255,255,255,0.9);
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
        }
        .upload-zone {
            border: 2px dashed #667eea;
            border-radius: 10px;
            padding: 3rem;
            text-align: center;
            background: #f8f9ff;
            margin: 1rem 0;
        }
        .file-card {
            background: white;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-processing { background-color: #ff9800; }
        .status-completed { background-color: #4caf50; }
        .status-error { background-color: #f44336; }
        </style>
    """

    MENU_ITEMS = {
        "Get Help": "https://github.com/your-repo/issues",
        "Report a bug": "https://github.com/your-repo/issues",
        "About": (
            "# Speaker Diarization App\nTranscribe and identify speakers in audio files with AI."
        ),
    }

    SORT_OPTIONS = [
        "Date created (newest)",
        "Date created (oldest)",
        "Title (A-Z)",
        "Title (Z-A)",
        "Duration (longest)",
        "Duration (shortest)",
    ]

    MODEL_OPTIONS = ["tiny", "base", "small", "medium", "large"]
    LANGUAGE_OPTIONS = ["auto", "en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko"]
