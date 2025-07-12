# Speaker Diarization Project

A clean, modern tool for audio transcription with speaker identification and interactive playback.

## 🚀 Quick Start

1. **Run Speaker Diarization:**

   ```bash
   python diarize_cli_improved.py "your_audio.wav" -o "output.srt" --model base --language en
   ```

2. **View Results:**
   Open `player.html` in your browser to see the interactive transcript with speaker dialogs.

## 📁 Project Structure

```
notta/
├── diarize_cli_improved.py    # Main CLI tool for diarization
├── player.html               # Web player with dialog UI
├── real_diarized_output.srt  # Example output with real speakers
├── Reading 29...wav          # Sample audio file
├── .env                      # HuggingFace token (required)
├── summary.md               # Detailed project documentation
└── venv/                    # Python virtual environment
```

## ✨ Features

- **Real Speaker Diarization**: Uses AI to identify actual speakers in audio
- **Modern Dialog UI**: Chat-bubble style transcript with timestamps
- **Audio Sync**: Highlights current speaker while playing
- **Multiple Formats**: Supports WAV, MP3 audio files
- **Configurable**: Multiple Whisper model sizes available

## 🔧 Requirements

- Python virtual environment (`venv/`)
- HuggingFace token in `.env` file
- Audio file (WAV/MP3)

## 📖 Documentation

This project includes comprehensive documentation organized in the [`docs/`](docs/) directory:

- **📋 [Project Overview](docs/project/summary.md)** - Detailed project documentation and features
- **🏗️ [Architecture](docs/architecture/ARCHITECTURE.md)** - Technical architecture and design principles
- **💻 [Contributing](docs/development/CONTRIBUTING.md)** - How to contribute to the project
- **📅 [Development Plan](docs/project/plan.md)** - Roadmap and planned enhancements
- **🎨 [UI Improvements](docs/project/UI_IMPROVEMENTS.md)** - UI/UX design documentation

For a complete documentation index, see [`docs/README.md`](docs/README.md)

---
