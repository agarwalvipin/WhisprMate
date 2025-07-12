"""Core domain models for the audio processing system."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Optional


class ProcessingStatus(Enum):
    """Status of audio processing."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class SupportedFormat(Enum):
    """Supported audio formats."""

    WAV = ".wav"
    MP3 = ".mp3"


@dataclass
class AudioFile:
    """Domain model for audio files."""

    name: str
    path: Path
    size_bytes: int
    duration_seconds: Optional[float] = None
    created_at: Optional[datetime] = None
    format: Optional[SupportedFormat] = None

    @property
    def size_mb(self) -> float:
        """Get file size in MB."""
        return self.size_bytes / (1024 * 1024)

    @property
    def size_kb(self) -> float:
        """Get file size in KB."""
        return self.size_bytes / 1024

    @property
    def formatted_size(self) -> str:
        """Get formatted file size string."""
        if self.size_mb >= 1:
            return f"{self.size_mb:.2f} MB"
        return f"{self.size_kb:.1f} KB"

    @property
    def formatted_duration(self) -> str:
        """Get formatted duration string."""
        if self.duration_seconds is None:
            return "-"
        mins, secs = divmod(int(self.duration_seconds), 60)
        return f"{mins}min {secs}s"


@dataclass
class ProcessingOptions:
    """Configuration for audio processing."""

    model_size: str = "base"
    language: str = "auto"
    enable_diarization: bool = True


@dataclass
class TranscriptionSegment:
    """A segment of transcribed audio with speaker information."""

    start_time: float
    end_time: float
    speaker_id: str
    text: str
    confidence: Optional[float] = None


@dataclass
class ProcessingResult:
    """Result of audio processing."""

    audio_file: AudioFile
    status: ProcessingStatus
    segments: List[TranscriptionSegment]
    error_message: Optional[str] = None
    processing_time_seconds: Optional[float] = None

    @property
    def srt_content(self) -> str:
        """Generate SRT content from segments."""
        srt_lines = []
        for i, segment in enumerate(self.segments, 1):
            start_srt = self._seconds_to_srt_time(segment.start_time)
            end_srt = self._seconds_to_srt_time(segment.end_time)

            srt_lines.extend(
                [str(i), f"{start_srt} --> {end_srt}", f"{segment.speaker_id}: {segment.text}", ""]
            )
        return "\n".join(srt_lines)

    @staticmethod
    def _seconds_to_srt_time(seconds: float) -> str:
        """Convert seconds to SRT time format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millisecs = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"


# Abstract interfaces following Dependency Inversion Principle


class AudioProcessorInterface(ABC):
    """Interface for audio processing services."""

    @abstractmethod
    async def process_audio(
        self, audio_file: AudioFile, options: ProcessingOptions
    ) -> ProcessingResult:
        """Process audio file and return transcription result."""
        pass

    @abstractmethod
    def estimate_processing_time(
        self, duration_seconds: float, options: ProcessingOptions
    ) -> float:
        """Estimate processing time in seconds."""
        pass


class FileManagerInterface(ABC):
    """Interface for file management operations."""

    @abstractmethod
    def save_uploaded_file(self, uploaded_file, filename: str) -> AudioFile:
        """Save uploaded file and return AudioFile instance."""
        pass

    @abstractmethod
    def get_audio_files(self) -> List[AudioFile]:
        """Get list of all audio files."""
        pass

    @abstractmethod
    def delete_file(self, audio_file: AudioFile) -> bool:
        """Delete audio file and associated files."""
        pass

    @abstractmethod
    def get_file_duration(self, file_path: Path) -> Optional[float]:
        """Get audio file duration in seconds."""
        pass


class TranscriptManagerInterface(ABC):
    """Interface for transcript management."""

    @abstractmethod
    def save_transcript(self, audio_file: AudioFile, result: ProcessingResult) -> Path:
        """Save transcript to file and return path."""
        pass

    @abstractmethod
    def load_transcript(self, audio_file: AudioFile) -> Optional[str]:
        """Load transcript content if it exists."""
        pass

    @abstractmethod
    def transcript_exists(self, audio_file: AudioFile) -> bool:
        """Check if transcript exists for audio file."""
        pass


class AuthenticationInterface(ABC):
    """Interface for authentication services."""

    @abstractmethod
    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        pass

    @abstractmethod
    def login(self, username: str, password: str) -> bool:
        """Authenticate user."""
        pass

    @abstractmethod
    def logout(self) -> None:
        """Log out user."""
        pass
