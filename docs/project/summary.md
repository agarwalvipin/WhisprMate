# Project Summary

## Overview

This project provides a complete workflow for audio transcription, speaker diarization, and interactive transcript visualization. It enables users to transcribe audio files, identify speakers, generate SRT subtitle files with speaker labels, and view/playback the results in a web-based UI.

---

## Features

- **Audio Transcription**: Uses OpenAI Whisper to transcribe audio files (WAV/MP3) to text.
- **Speaker Diarization**: Uses pyannote.audio to segment audio by speaker, labeling each segment (e.g., SPEAKER_00, SPEAKER_01).
- **Diarized SRT Generation**: CLI tool (`diarize_cli.py`) generates SRT files with speaker labels for each segment.
- **Web-based Audio Player**: [`player.html`](player.html) loads the audio and SRT, displaying the transcript as formatted dialogs, highlighting the current speaker's turn in sync with playback.
- **Configurable Workflow**: CLI supports options for model selection, language, diarization toggle, and Hugging Face token input.
- **.gitignore**: Excludes sensitive and large files (audio, .env, venv, etc.) from version control.

---

## Key Files

- [`diarize_cli_improved.py`](diarize_cli_improved.py): Main CLI tool for real speaker diarization and transcription
- [`player.html`](player.html): Web UI for audio playback with modern dialog-style transcript visualization
- [`real_diarized_output.srt`](real_diarized_output.srt): Example SRT file with real speaker diarization
- [`Reading 29- Analyzing Balance Sheets.wav`](Reading%2029-%20Analyzing%20Balance%20Sheets.wav): Sample audio file for testing
- `.env`: Contains Hugging Face API token for diarization (required)
- `.gitignore`: Excludes venv, cache files, and sensitive data from version control

---

## Workflow

1. **Transcribe & Diarize**:  
   Run the CLI tool:

   ```bash
   python diarize_cli_improved.py "audio.wav" -o "output.srt" --model base --language en
   ```

   This generates an SRT file with real speaker labels using AI-powered speaker diarization.

2. **View in Browser**:  
   Open [`player.html`](player.html) in a browser (using Live Server or Python HTTP server).  
   The UI displays the transcript as dialogs, highlighting the current speaker as the audio plays.

---

## Extensibility

- The CLI can be extended for more models, languages, or output formats.
- The UI can be enhanced for better dialog formatting, speaker color-coding, or search/filter features.

---

## Requirements

- Python 3.8+
- openai-whisper, pyannote.audio, python-dotenv, soundfile, whisper, torch, etc.
- Hugging Face account and API token for diarization.

---

## Example

- Input: `Reading 29- Analyzing Balance Sheets.wav`
- Output: `Reading 29- Analyzing Balance Sheets.srt` (with speaker labels)
- UI: [`player.html`](player.html) for interactive playback and dialog view
