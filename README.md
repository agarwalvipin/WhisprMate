# Speaker Diarization Project

A clean, modern tool for audio transcription with speaker identification and interactive playback.

## � Prerequisites

### HuggingFace Token (Recommended for Real Speaker Diarization)

For accurate speaker diarization, you need a HuggingFace token:

1. **Create Account**: Sign up at [HuggingFace](https://huggingface.co/)
2. **Get Token**: Visit [Settings > Access Tokens](https://huggingface.co/settings/tokens)
3. **Accept License**: Go to [pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1) and accept the user agreement
4. **Set Environment Variable**: 
   ```bash
   # Create .env file
   cp .env.example .env
   # Edit .env and add your token:
   HF_TOKEN=your_actual_token_here
   ```

**Note**: Without a token, the application will automatically use simulation mode for demonstration purposes.

## �🚀 Quick Start

### Option 1: Web Interface (Streamlit)

Run the interactive web application:

```bash
# With default credentials (admin/admin)
streamlit run main.py

# With custom credentials
streamlit run main.py -- --username YOUR_USERNAME --password YOUR_PASSWORD
```

Then login using the provided credentials to access the full application.

### Option 2: Docker Deployment

Deploy the application using Docker for isolated and consistent environments:

```bash
# Quick deployment with script
./scripts/deploy.sh

# Or manual Docker commands
docker build -t WhisprMate .
docker run -p 8501:8501 -v $(pwd)/uploads:/app/uploads WhisprMate
```

Then access the application at http://localhost:8501

### Option 3: Command Line Interface

1. **Run Speaker Diarization:**

   ```bash
   python scripts/diarize_cli_improved.py "your_audio.wav" -o "output.srt" --model base --language en
   ```

2. **View Results:**
   Open `static/player.html` in your browser to see the interactive transcript with speaker dialogs.

## 🔐 Authentication

The web application includes a login system with configurable credentials:

- **Default Username**: `admin`
- **Default Password**: `admin`
- **Custom Credentials**: Use `--username` and `--password` arguments
- **Quick Login**: Use the "Use Defaults" button for rapid access

For detailed authentication setup, see [docs/AUTHENTICATION.md](docs/AUTHENTICATION.md).

## 📁 Project Structure

```
WhisprMate/
├── scripts/
│   └── diarize_cli_improved.py    # Main CLI tool for diarization
├── static/
│   └── player.html               # Web player with dialog UI
├── src/                          # Source code modules
│   ├── core/                     # Core models and interfaces
│   ├── services/                 # Business logic services
│   ├── ui/                       # UI components
│   └── utils/                    # Utility functions
├── docs/                         # Comprehensive documentation
├── tests/                        # Unit and integration tests
├── main.py                       # Streamlit web application
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker container configuration
└── docker-compose.yml           # Docker compose configuration
```

## ✨ Features

- **Real Speaker Diarization**: Uses AI to identify actual speakers in audio
- **Modern Dialog UI**: Chat-bubble style transcript with timestamps
- **Audio Sync**: Highlights current speaker while playing
- **Multiple Formats**: Supports WAV, MP3 audio files
- **Configurable**: Multiple Whisper model sizes available

## 🔧 Requirements

- Python 3.11+ environment
- Audio file (WAV/MP3)
- **Optional**: HuggingFace token for real speaker diarization (simulation mode available without token)
- **Docker** (for containerized deployment)

## 📖 Documentation

This project includes comprehensive documentation organized in the [`docs/`](docs/) directory:

- **📋 [Project Overview](docs/project/summary.md)** - Detailed project documentation and features
- **🏗️ [Architecture](docs/architecture/ARCHITECTURE.md)** - Technical architecture and design principles
- **💻 [Contributing](docs/development/CONTRIBUTING.md)** - How to contribute to the project
- **📅 [Development Plan](docs/project/plan.md)** - Roadmap and planned enhancements
- **🎨 [UI Improvements](docs/project/UI_IMPROVEMENTS.md)** - UI/UX design documentation

For a complete documentation index, see [`docs/README.md`](docs/README.md)

---
