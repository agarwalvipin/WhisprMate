"""File management service implementation."""

from datetime import datetime
from pathlib import Path
from typing import List, Optional

import soundfile as sf

from config.logging_config import get_logger
from config.settings import AppConfig

from ..core.models import AudioFile, FileManagerInterface, SupportedFormat

logger = get_logger("file")


class FileManagerService(FileManagerInterface):
    """Service for managing audio files and uploads."""

    def __init__(self, upload_dir: Optional[Path] = None):
        """Initialize the file manager service.

        Args:
            upload_dir: Directory for uploaded files (defaults to config)
        """
        self.upload_dir = upload_dir or AppConfig.get_upload_dir()
        logger.info(f"FileManagerService initialized with upload directory: {self.upload_dir}")

        # Ensure upload directory exists
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Upload directory ensured: {self.upload_dir}")

    def save_uploaded_file(self, uploaded_file, filename: str) -> AudioFile:
        """Save uploaded file and return AudioFile instance.

        Args:
            uploaded_file: Streamlit uploaded file object
            filename: Name for the saved file

        Returns:
            AudioFile instance with metadata
        """
        file_path = self.upload_dir / filename

        # Save the file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Get file metadata
        size_bytes = file_path.stat().st_size
        created_at = datetime.fromtimestamp(file_path.stat().st_mtime)
        duration = self.get_file_duration(file_path)

        # Determine format
        file_format = None
        if filename.lower().endswith(".wav"):
            file_format = SupportedFormat.WAV
        elif filename.lower().endswith(".mp3"):
            file_format = SupportedFormat.MP3

        return AudioFile(
            name=filename,
            path=file_path,
            size_bytes=size_bytes,
            duration_seconds=duration,
            created_at=created_at,
            format=file_format,
        )

    def get_audio_files(self) -> List[AudioFile]:
        """Get list of all audio files.

        Returns:
            List of AudioFile instances
        """
        audio_files = []

        if not self.upload_dir.exists():
            return audio_files

        for file_path in self.upload_dir.iterdir():
            if file_path.is_file() and AppConfig.is_supported_format(file_path.name):
                try:
                    size_bytes = file_path.stat().st_size
                    created_at = datetime.fromtimestamp(file_path.stat().st_mtime)
                    duration = self.get_file_duration(file_path)

                    # Determine format
                    file_format = None
                    if file_path.name.lower().endswith(".wav"):
                        file_format = SupportedFormat.WAV
                    elif file_path.name.lower().endswith(".mp3"):
                        file_format = SupportedFormat.MP3

                    audio_file = AudioFile(
                        name=file_path.name,
                        path=file_path,
                        size_bytes=size_bytes,
                        duration_seconds=duration,
                        created_at=created_at,
                        format=file_format,
                    )
                    audio_files.append(audio_file)

                except Exception:
                    # Skip files that can't be processed
                    continue

        return audio_files

    def delete_file(self, audio_file: AudioFile) -> bool:
        """Delete audio file and associated files.

        Args:
            audio_file: The audio file to delete

        Returns:
            True if deletion was successful
        """
        try:
            # Delete main audio file
            if audio_file.path.exists():
                audio_file.path.unlink()

            # Delete associated SRT file if it exists
            srt_path = audio_file.path.with_suffix(audio_file.path.suffix + ".srt")
            if srt_path.exists():
                srt_path.unlink()

            return True

        except Exception:
            return False

    def get_file_duration(self, file_path: Path) -> Optional[float]:
        """Get audio file duration in seconds.

        Args:
            file_path: Path to audio file

        Returns:
            Duration in seconds or None if unable to determine
        """
        try:
            with sf.SoundFile(str(file_path)) as f:
                return len(f) / f.samplerate
        except Exception:
            return None

    def file_exists(self, filename: str) -> bool:
        """Check if file exists in upload directory.

        Args:
            filename: Name of file to check

        Returns:
            True if file exists
        """
        return (self.upload_dir / filename).exists()

    def get_transcript_path(self, audio_file: AudioFile) -> Path:
        """Get path for transcript file.

        Args:
            audio_file: Audio file to get transcript path for

        Returns:
            Path for transcript file
        """
        return audio_file.path.with_suffix(audio_file.path.suffix + ".srt")

    def cleanup_orphaned_files(self) -> int:
        """Clean up orphaned transcript files.

        Returns:
            Number of files cleaned up
        """
        cleaned = 0

        if not self.upload_dir.exists():
            return cleaned

        # Find SRT files without corresponding audio files
        for file_path in self.upload_dir.glob("*.srt"):
            # Check if original audio file exists
            audio_name = file_path.name.replace(".srt", "")
            audio_path = self.upload_dir / audio_name

            if not audio_path.exists():
                try:
                    file_path.unlink()
                    cleaned += 1
                except Exception:
                    continue

        return cleaned
