"""Transcript management service implementation."""

from pathlib import Path
from typing import Optional

from config.logging_config import get_logger

from ..core.models import AudioFile, ProcessingResult, TranscriptManagerInterface

logger = get_logger("transcript")


class TranscriptManagerService(TranscriptManagerInterface):
    """Service for managing transcripts and SRT files."""

    def save_transcript(self, audio_file: AudioFile, result: ProcessingResult) -> Path:
        """Save transcript to file and return path.

        Args:
            audio_file: The audio file the transcript belongs to
            result: Processing result with transcript data

        Returns:
            Path to saved transcript file
        """
        srt_path = audio_file.path.with_suffix(audio_file.path.suffix + ".srt")
        logger.info(f"Saving transcript for {audio_file.name} to {srt_path}")

        try:
            with open(srt_path, "w", encoding="utf-8") as f:
                f.write(result.srt_content)

            logger.debug(f"Transcript saved successfully: {srt_path}")
            return srt_path
        except Exception as e:
            logger.error(f"Failed to save transcript to {srt_path}: {str(e)}")
            raise

    def load_transcript(self, audio_file: AudioFile) -> Optional[str]:
        """Load transcript content if it exists.

        Args:
            audio_file: The audio file to load transcript for

        Returns:
            Transcript content or None if not found
        """
        srt_path = audio_file.path.with_suffix(audio_file.path.suffix + ".srt")

        if not srt_path.exists():
            return None

        try:
            with open(srt_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None

    def transcript_exists(self, audio_file: AudioFile) -> bool:
        """Check if transcript exists for audio file.

        Args:
            audio_file: The audio file to check

        Returns:
            True if transcript exists
        """
        srt_path = audio_file.path.with_suffix(audio_file.path.suffix + ".srt")
        return srt_path.exists()

    def get_transcript_path(self, audio_file: AudioFile) -> Path:
        """Get transcript file path for audio file.

        Args:
            audio_file: The audio file

        Returns:
            Path to transcript file (may not exist)
        """
        return audio_file.path.with_suffix(audio_file.path.suffix + ".srt")

    def delete_transcript(self, audio_file: AudioFile) -> bool:
        """Delete transcript file if it exists.

        Args:
            audio_file: The audio file whose transcript to delete

        Returns:
            True if deletion was successful or file didn't exist
        """
        srt_path = audio_file.path.with_suffix(audio_file.path.suffix + ".srt")

        if not srt_path.exists():
            return True

        try:
            srt_path.unlink()
            return True
        except Exception:
            return False
