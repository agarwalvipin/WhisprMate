"""Audio processing service implementation."""

import os
import re
import subprocess
from pathlib import Path
from typing import Tuple

from config.logging_config import get_logger

from ..core.models import (
    AudioFile,
    AudioProcessorInterface,
    ProcessingOptions,
    ProcessingResult,
    ProcessingStatus,
    TranscriptionSegment,
)

logger = get_logger("audio")


class AudioProcessorService(AudioProcessorInterface):
    """Service for processing audio files with speaker diarization."""

    def __init__(self, diarize_script_path: str = "scripts/diarize_cli_improved.py"):
        """Initialize the audio processor service.

        Args:
            diarize_script_path: Path to the diarization script
        """
        self.diarize_script_path = diarize_script_path
        logger.info(f"AudioProcessorService initialized with script path: {diarize_script_path}")

        # Verify script exists
        if not Path(diarize_script_path).exists():
            logger.warning(f"Diarization script not found at: {diarize_script_path}")
        else:
            logger.debug(f"Diarization script verified at: {diarize_script_path}")

    async def process_audio(
        self, audio_file: AudioFile, options: ProcessingOptions
    ) -> ProcessingResult:
        """Process audio file and return transcription result.

        Args:
            audio_file: The audio file to process
            options: Processing configuration options

        Returns:
            ProcessingResult with transcription data
        """
        logger.info(f"Starting audio processing for: {audio_file.name}")
        logger.debug(
            f"Processing options: model={options.model_size}, "
            f"language={options.language}, diarization={options.enable_diarization}"
        )

        srt_path = audio_file.path.with_suffix(audio_file.path.suffix + ".srt")
        logger.debug(f"Output SRT path: {srt_path}")

        try:
            success, message = self._run_diarization(str(audio_file.path), str(srt_path), options)

            if success:
                logger.info(f"Diarization completed successfully for: {audio_file.name}")
                segments = self._parse_srt_file(srt_path)
                logger.info(f"Parsed {len(segments)} transcript segments")
                return ProcessingResult(
                    audio_file=audio_file, status=ProcessingStatus.COMPLETED, segments=segments
                )
            else:
                logger.error(f"Diarization failed for {audio_file.name}: {message}")
                return ProcessingResult(
                    audio_file=audio_file,
                    status=ProcessingStatus.FAILED,
                    segments=[],
                    error_message=message,
                )

        except Exception as e:
            logger.exception(f"Unexpected error processing {audio_file.name}: {str(e)}")
            return ProcessingResult(
                audio_file=audio_file,
                status=ProcessingStatus.FAILED,
                segments=[],
                error_message=str(e),
            )

    def estimate_processing_time(
        self, duration_seconds: float, options: ProcessingOptions
    ) -> float:
        """Estimate processing time in seconds.

        Args:
            duration_seconds: Duration of audio file
            options: Processing options (affects processing speed)

        Returns:
            Estimated processing time in seconds
        """
        # Base multiplier depends on model size
        multipliers = {"tiny": 1.0, "base": 2.0, "small": 3.0, "medium": 4.0, "large": 5.0}

        base_multiplier = multipliers.get(options.model_size, 3.0)

        # Additional time for diarization
        if options.enable_diarization:
            base_multiplier *= 1.5

        return duration_seconds * base_multiplier

    def _run_diarization(
        self, audio_path: str, srt_path: str, options: ProcessingOptions
    ) -> Tuple[bool, str]:
        """Run the diarization script.

        Args:
            audio_path: Path to input audio file
            srt_path: Path to output SRT file
            options: Processing options

        Returns:
            Tuple of (success, message)
        """
        logger.debug(f"Starting diarization for: {audio_path}")

        try:
            cmd = [
                "uv",
                "run",
                "python",
                self.diarize_script_path,
                audio_path,
                "-o",
                srt_path,
                "--model",
                options.model_size,
            ]

            if options.language != "auto":
                cmd.extend(["--language", options.language])
                logger.debug(f"Using language: {options.language}")

            if not options.enable_diarization:
                cmd.append("--no-diarization")
                logger.debug("Diarization disabled")
            else:
                # Check if HF_TOKEN is available, if not use simulation mode
                hf_token = os.getenv("HF_TOKEN")
                if not hf_token:
                    cmd.append("--simulate-diarization")
                    logger.warning("No HF_TOKEN found, using simulation mode for diarization")
                else:
                    logger.debug("Using real diarization with HF_TOKEN")

            logger.info(f"Executing command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            logger.info("Diarization command completed successfully")
            logger.debug(f"Command output: {result.stdout}")
            if result.stderr:
                logger.debug(f"Command stderr: {result.stderr}")
            return True, result.stdout

        except subprocess.CalledProcessError as e:
            logger.error(f"Diarization command failed with exit code {e.returncode}")
            logger.error(f"Command stderr: {e.stderr}")
            logger.error(f"Command stdout: {e.stdout}")
            return False, e.stderr
        except Exception as e:
            logger.error(f"Unexpected error running diarization: {str(e)}")
            return False, str(e)

    def _parse_srt_file(self, srt_path: Path):
        """Parse SRT file and return list of transcription segments.

        Args:
            srt_path: Path to SRT file

        Returns:
            List of TranscriptionSegment objects
        """
        logger.debug(f"Parsing SRT file: {srt_path}")

        if not srt_path.exists():
            logger.warning(f"SRT file does not exist: {srt_path}")
            return []

        segments = []

        try:
            with open(srt_path, "r", encoding="utf-8") as f:
                content = f.read()

            logger.debug(f"SRT file content length: {len(content)} characters")

            # Parse SRT format
            pattern = (
                r"(\d+)\s+"
                r"(\d{2}:\d{2}:\d{2},\d{3})\s-->\s(\d{2}:\d{2}:\d{2},\d{3})\s+"
                r"(.*?)(?=\n\n|\n*$)"
            )

            matches = re.findall(pattern, content, re.DOTALL)
            logger.debug(f"Found {len(matches)} SRT segments")

            for i, match in enumerate(matches):
                start_time = self._srt_time_to_seconds(match[1])
                end_time = self._srt_time_to_seconds(match[2])
                text = match[3].strip()

                # Extract speaker from text
                speaker_id = "SPEAKER_00"
                if text.startswith("SPEAKER_"):
                    parts = text.split(":", 1)
                    if len(parts) == 2:
                        speaker_id = parts[0]
                        text = parts[1].strip()

                segments.append(
                    TranscriptionSegment(
                        start_time=start_time, end_time=end_time, speaker_id=speaker_id, text=text
                    )
                )

                if i < 3:  # Log first few segments for debugging
                    logger.debug(
                        f"Segment {i + 1}: {speaker_id} ({start_time:.2f}-{end_time:.2f}s): "
                        f"{text[:50]}..."
                    )

            logger.info(f"Successfully parsed {len(segments)} segments from SRT file")
            return segments

        except Exception as e:
            logger.error(f"Error parsing SRT file {srt_path}: {str(e)}")
            return []

    @staticmethod
    def _srt_time_to_seconds(srt_time: str) -> float:
        """Convert SRT time format to seconds.

        Args:
            srt_time: Time in SRT format (HH:MM:SS,mmm)

        Returns:
            Time in seconds as float
        """
        time_part, ms_part = srt_time.split(",")
        h, m, s = map(int, time_part.split(":"))
        ms = int(ms_part)

        return h * 3600 + m * 60 + s + ms / 1000.0
