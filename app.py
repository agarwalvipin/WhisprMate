"""
🚨 LEGACY CODE - REFACTORED VERSION AVAILABLE 🚨

This is the original monolithic application code.
A refactored version using SOLID principles is available in main.py

To run the refactored version: streamlit run main.py
To see the architecture: see ARCHITECTURE.md

The refactored version provides:
- Better separation of concerns
- Improved testability
- Cleaner code organization
- Type safety
- Dependency injection
- Reusable components

This file is kept for reference and comparison purposes.
"""

import os
import subprocess

import soundfile as sf
import streamlit as st

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# --- Authentication Placeholder ---
def login():
    st.session_state["authenticated"] = True


def logout():
    st.session_state["authenticated"] = False


def auth_ui():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    with st.sidebar:
        st.markdown("### 🔐 Authentication")
        if st.session_state.authenticated:
            st.success("✅ Logged in as user")
            if st.button("🚪 Logout"):
                st.session_state.authenticated = False
                st.rerun()
        else:
            st.info("🔒 Please log in to continue.")
            if st.button("🔑 Login"):
                st.session_state.authenticated = True
                st.rerun()


def run_diarization(audio_path, srt_path):
    try:
        result = subprocess.run(
            [
                "python",
                "diarize_cli_improved.py",
                audio_path,
                "-o",
                srt_path,
                "--model",
                "base",
                "--language",
                "en",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr


def read_srt(srt_path):
    if not os.path.exists(srt_path):
        return ""
    with open(srt_path, "r", encoding="utf-8") as f:
        return f.read()


def get_audio_duration(file_path):
    try:
        with sf.SoundFile(file_path) as f:
            return len(f) / f.samplerate
    except Exception:
        return None


def estimate_transcription_time(duration_sec, multiplier=3.0):
    # multiplier: 3.0 for CPU, 1.0 for GPU (adjust as needed)
    if duration_sec is None:
        return None
    est_sec = duration_sec * multiplier
    mins = int(est_sec // 60)
    secs = int(est_sec % 60)
    return f"{mins} min {secs} sec"


# --- Main App ---
def main():
    st.set_page_config(
        page_title="Speaker Diarization App",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com/your-repo/issues",
            "Report a bug": "https://github.com/your-repo/issues",
            "About": "# Speaker Diarization App\nTranscribe and identify speakers in audio files with AI.",
        },
    )

    # Custom CSS for better styling
    st.markdown(
        """
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
    """,
        unsafe_allow_html=True,
    )

    # Header
    st.markdown(
        """
        <div class="main-header">
            <h1>🎙️ Speaker Diarization & Transcription</h1>
            <p>Upload audio files and get AI-powered transcriptions with speaker identification</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Initialize session state
    if "current_page" not in st.session_state:
        st.session_state.current_page = "dashboard"

    # For demo purposes, skip auth
    st.session_state.authenticated = True

    # Navigation
    page = st.session_state.current_page
    if page == "player":
        show_player_page()
        return

    # Main content with tabs
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📤 Upload", "⚙️ Processing Status"])

    with tab1:
        show_dashboard()

    with tab2:
        show_upload_section()

    with tab3:
        show_processing_status()


def show_dashboard():
    """Display the main dashboard with file management"""
    st.header("📊 My Audio Files")

    # Search and filter section
    col1, col2 = st.columns([2, 1])
    with col1:
        search_query = st.text_input("🔍 Search files", placeholder="Type to search...")
    with col2:
        sort_options = [
            "Date created (newest)",
            "Date created (oldest)",
            "Title (A-Z)",
            "Title (Z-A)",
            "Duration (longest)",
            "Duration (shortest)",
        ]
        sort_option = st.selectbox("Sort by", sort_options)

    # Get files and build data
    files = [f for f in os.listdir(UPLOAD_DIR) if f.lower().endswith((".wav", ".mp3"))]

    if not files:
        st.info("📁 No audio files found. Upload your first file in the Upload tab!")
        return

    file_rows = []
    for file in files:
        audio_path = os.path.join(UPLOAD_DIR, file)
        duration = get_audio_duration(audio_path)
        duration_str = f"{int(duration // 60)}min {int(duration % 60)}s" if duration else "-"

        try:
            import datetime

            created = datetime.datetime.fromtimestamp(os.path.getmtime(audio_path)).strftime(
                "%d/%m/%Y %H:%M"
            )
        except Exception:
            created = "-"

        file_size = os.path.getsize(audio_path)
        size_str = (
            f"{file_size / 1024:.1f} KB"
            if file_size < 1024 * 1024
            else f"{file_size / 1024 / 1024:.2f} MB"
        )

        file_rows.append(
            {
                "title": file,
                "duration": duration_str,
                "created": created,
                "creator": "vipin agarwal",
                "duration_val": duration or 0,
                "created_val": os.path.getmtime(audio_path) if duration else 0,
                "size": size_str,
                "audio_path": audio_path,
            }
        )

    # Filter by search
    if search_query:
        file_rows = [row for row in file_rows if search_query.lower() in row["title"].lower()]

    # Sort files
    if sort_option == "Date created (newest)":
        file_rows.sort(key=lambda x: x["created_val"], reverse=True)
    elif sort_option == "Date created (oldest)":
        file_rows.sort(key=lambda x: x["created_val"])
    elif sort_option == "Title (A-Z)":
        file_rows.sort(key=lambda x: x["title"].lower())
    elif sort_option == "Title (Z-A)":
        file_rows.sort(key=lambda x: x["title"].lower(), reverse=True)
    elif sort_option == "Duration (longest)":
        file_rows.sort(key=lambda x: x["duration_val"], reverse=True)
    elif sort_option == "Duration (shortest)":
        file_rows.sort(key=lambda x: x["duration_val"])

    # Display files in cards
    for row in file_rows:
        with st.container():
            st.markdown(
                f"""
                <div class="file-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h4 style="margin: 0; color: #333;">{row["title"]}</h4>
                            <p style="margin: 5px 0; color: #666; font-size: 0.9em;">
                                📅 {row["created"]} • ⏱️ {row["duration"]} • 📦 {row["size"]}
                            </p>
                        </div>
                        <div style="display: flex; gap: 10px;">
                            <!-- Play button will be added here -->
                        </div>
                    </div>
                </div>
            """,
                unsafe_allow_html=True,
            )

            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("▶️ Play", key=f"play_{row['title']}"):
                    st.session_state["player_file"] = row["title"]
                    st.session_state["current_page"] = "player"
                    st.rerun()
            with col2:
                srt_path = row["audio_path"] + ".srt"
                if os.path.exists(srt_path):
                    with open(srt_path, "r", encoding="utf-8") as f:
                        transcript = f.read()
                    st.download_button(
                        "📄 Download SRT",
                        transcript,
                        file_name=f"{row['title']}.srt",
                        key=f"download_{row['title']}",
                    )
                else:
                    st.button(
                        "❌ No transcript", disabled=True, key=f"no_transcript_{row['title']}"
                    )
            with col3:
                if st.button("🗑️ Delete", key=f"delete_{row['title']}"):
                    try:
                        os.remove(row["audio_path"])
                        srt_path = row["audio_path"] + ".srt"
                        if os.path.exists(srt_path):
                            os.remove(srt_path)
                        st.success(f"Deleted {row['title']}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting file: {e}")


def show_upload_section():
    """Display the file upload interface"""
    st.header("📤 Upload Audio File")

    st.markdown(
        """
        <div class="upload-zone">
            <h3>🎵 Drag & Drop or Browse Files</h3>
            <p>Supported formats: WAV, MP3 • Max size: 50MB</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Choose an audio file",
        type=["wav", "mp3"],
        help="Upload a WAV or MP3 file for transcription and speaker diarization",
    )

    if uploaded_file:
        # File size check
        if uploaded_file.size > 50 * 1024 * 1024:
            st.error("❌ File too large. Please upload a file smaller than 50MB.")
            return

        # Save file
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with st.spinner("💾 Saving file..."):
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

        st.success(f"✅ Uploaded: {uploaded_file.name}")

        # Show file info
        duration = get_audio_duration(file_path)
        if duration:
            mins, secs = divmod(int(duration), 60)
            st.info(f"📊 Duration: {mins}min {secs}sec")

            # Estimate processing time
            est_time = estimate_transcription_time(duration)
            if est_time:
                st.info(f"⏱️ Estimated processing time: {est_time}")

        # Processing options
        st.subheader("🔧 Processing Options")
        col1, col2 = st.columns(2)
        with col1:
            model_size = st.selectbox(
                "Whisper Model",
                ["tiny", "base", "small", "medium", "large"],
                index=1,
                help="Larger models are more accurate but slower",
            )
        with col2:
            language = st.selectbox(
                "Language",
                ["auto", "en", "es", "fr", "de", "it", "pt", "ru", "ja", "ko"],
                help="Auto-detect or specify language",
            )

        # Start processing
        if st.button("🚀 Start Processing", type="primary"):
            srt_path = file_path + ".srt"

            with st.spinner("🤖 Processing audio... This may take a few minutes."):
                progress_bar = st.progress(0)

                # Simulate progress (in real implementation, you'd get actual progress)
                import time

                for i in range(100):
                    time.sleep(0.1)
                    progress_bar.progress(i + 1)

                # Run actual processing
                ok, msg = run_diarization(file_path, srt_path)

            if ok:
                st.success("🎉 Processing complete!")
                st.balloons()

                # Show results preview
                if os.path.exists(srt_path):
                    with open(srt_path, "r", encoding="utf-8") as f:
                        transcript_preview = f.read()[:500] + "..."

                    st.subheader("📄 Transcript Preview")
                    st.text_area(
                        "Transcript Preview",
                        transcript_preview,
                        height=150,
                        disabled=True,
                        label_visibility="collapsed",
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            "📄 Download Full Transcript",
                            transcript_preview,
                            file_name=f"{uploaded_file.name}.srt",
                        )
                    with col2:
                        if st.button("▶️ Open Player"):
                            st.session_state["player_file"] = uploaded_file.name
                            st.session_state["current_page"] = "player"
                            st.rerun()
            else:
                st.error(f"❌ Processing failed: {msg}")


def show_processing_status():
    """Display processing status and system information"""
    st.header("⚙️ Processing Status")

    # System status
    st.subheader("🖥️ System Information")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("CPU Usage", "45%", "2%")
    with col2:
        st.metric("Memory Usage", "2.1 GB", "0.3 GB")
    with col3:
        st.metric("Available Storage", "15.2 GB", "-0.5 GB")

    # Processing queue
    st.subheader("📋 Processing Queue")

    # Check for files currently being processed
    processing_files = []
    completed_files = []

    for file in os.listdir(UPLOAD_DIR):
        if file.lower().endswith((".wav", ".mp3")):
            audio_path = os.path.join(UPLOAD_DIR, file)
            srt_path = audio_path + ".srt"

            if os.path.exists(srt_path):
                completed_files.append(file)
            else:
                processing_files.append(file)

    if processing_files:
        st.warning(f"⏳ {len(processing_files)} files waiting to be processed")
        for file in processing_files:
            st.markdown(
                f"""
                <div style="padding: 10px; background: #fff3cd; border-radius: 5px; margin: 5px 0;">
                    <span class="status-indicator status-processing"></span>
                    <strong>{file}</strong> - Waiting for processing
                </div>
            """,
                unsafe_allow_html=True,
            )

    if completed_files:
        st.success(f"✅ {len(completed_files)} files processed successfully")
        for file in completed_files:
            st.markdown(
                f"""
                <div style="padding: 10px; background: #d4edda; border-radius: 5px; margin: 5px 0;">
                    <span class="status-indicator status-completed"></span>
                    <strong>{file}</strong> - Processing completed
                </div>
            """,
                unsafe_allow_html=True,
            )

    if not processing_files and not completed_files:
        st.info("📝 No files in queue. Upload files to get started!")

    # Error logs
    st.subheader("🐛 Recent Errors")
    if st.button("Clear Error Logs"):
        st.success("Error logs cleared")
    else:
        st.info("No errors recorded")


def show_player_page():
    """Display the enhanced audio player interface"""
    if "player_file" not in st.session_state:
        st.error("No file selected for playback")
        return

    player_file = st.session_state["player_file"]
    audio_path = os.path.join(UPLOAD_DIR, player_file)

    if not os.path.exists(audio_path):
        st.error(f"Audio file not found: {player_file}")
        return

    # Header with back button
    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("← Back"):
            st.session_state["current_page"] = "dashboard"
            st.rerun()
    with col2:
        st.title(f"🎵 {player_file}")

    # Audio player
    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()

    st.audio(
        audio_bytes, format="audio/wav" if player_file.lower().endswith(".wav") else "audio/mp3"
    )

    # Transcript section
    srt_path = audio_path + ".srt"
    if os.path.exists(srt_path):
        with open(srt_path, "r", encoding="utf-8") as f:
            transcript = f.read()

        st.subheader("📄 Interactive Transcript")

        # Enhanced HTML player with waveform
        import base64

        import streamlit.components.v1 as components

        audio_b64 = base64.b64encode(audio_bytes).decode()
        audio_ext = "wav" if player_file.lower().endswith(".wav") else "mp3"
        transcript_b64 = base64.b64encode(transcript.encode()).decode()

        player_html = create_enhanced_player_html(audio_b64, audio_ext, transcript_b64)
        components.html(player_html, height=600)

        # Download options
        st.download_button(
            "📄 Download Transcript", transcript, file_name=f"{player_file}.srt", mime="text/plain"
        )
    else:
        st.warning("⚠️ Transcript not available. Please process this file first.")


def create_enhanced_player_html(audio_b64, audio_ext, transcript_b64):
    """Create enhanced HTML player with waveform visualization"""
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Enhanced Audio Player</title>
        <script src="https://unpkg.com/wavesurfer.js"></script>
        <style>
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0; 
                padding: 20px;
                background: #f8f9fa;
            }}
            #waveform {{ 
                width: 100%; 
                height: 120px; 
                margin-bottom: 20px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                padding: 20px;
            }}
            #controls {{
                display: flex;
                justify-content: center;
                gap: 15px;
                margin-bottom: 20px;
            }}
            .control-btn {{
                background: #667eea;
                color: white;
                border: none;
                border-radius: 25px;
                padding: 10px 20px;
                cursor: pointer;
                font-size: 14px;
                transition: all 0.3s ease;
            }}
            .control-btn:hover {{
                background: #5a6fd8;
                transform: translateY(-2px);
            }}
            #transcript {{ 
                max-height: 400px; 
                overflow-y: auto; 
                background: white;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            .dialog {{ 
                display: flex;
                align-items: flex-start;
                margin: 15px 0; 
                padding: 15px;
                border-radius: 10px;
                transition: all 0.3s ease;
                cursor: pointer;
            }}
            .dialog:hover {{
                background: #f8f9ff;
                transform: translateX(5px);
            }}
            .timestamp {{
                font-size: 12px;
                color: #666;
                min-width: 50px;
                margin-top: 4px;
                font-weight: 600;
                background: #e9ecef;
                padding: 2px 8px;
                border-radius: 12px;
            }}
            .speaker-avatar {{
                width: 36px;
                height: 36px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
                font-size: 14px;
                flex-shrink: 0;
                margin: 0 15px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            }}
            .speaker-0 .speaker-avatar {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
            .speaker-1 .speaker-avatar {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }}
            .content {{ flex: 1; }}
            .speaker-name {{
                font-weight: 700;
                font-size: 15px;
                color: #333;
                margin-bottom: 6px;
            }}
            .speaker-0 .speaker-name {{ color: #667eea; }}
            .speaker-1 .speaker-name {{ color: #f5576c; }}
            .text {{
                color: #444;
                line-height: 1.6;
                font-size: 15px;
            }}
            .active {{
                background: linear-gradient(135deg, #fff3e0 0%, #ffe0b3 100%);
                border-left: 4px solid #ff9800;
                box-shadow: 0 4px 15px rgba(255, 152, 0, 0.2);
                transform: translateX(10px);
            }}
            .waveform-container {{
                position: relative;
            }}
            .time-display {{
                display: flex;
                justify-content: space-between;
                margin-top: 10px;
                font-size: 12px;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="waveform-container">
            <div id="waveform"></div>
            <div class="time-display">
                <span id="current-time">0:00</span>
                <span id="total-time">0:00</span>
            </div>
        </div>
        
        <div id="controls">
            <button class="control-btn" onclick="wavesurfer.playPause()">⏯️ Play/Pause</button>
            <button class="control-btn" onclick="wavesurfer.stop()">⏹️ Stop</button>
            <button class="control-btn" onclick="wavesurfer.skip(-10)">⏪ -10s</button>
            <button class="control-btn" onclick="wavesurfer.skip(10)">⏩ +10s</button>
        </div>
        
        <div id="transcript"></div>
        
        <script>
            var wavesurfer = WaveSurfer.create({{
                container: '#waveform',
                waveColor: '#667eea',
                progressColor: '#f5576c',
                cursorColor: '#333',
                barWidth: 3,
                barRadius: 3,
                responsive: true,
                height: 80,
                normalize: true,
                backend: 'WebAudio'
            }});

            wavesurfer.load("data:audio/{audio_ext};base64,{audio_b64}");

            // Time display updates
            wavesurfer.on('audioprocess', function(time) {{
                document.getElementById('current-time').textContent = formatTime(time);
            }});
            
            wavesurfer.on('ready', function() {{
                document.getElementById('total-time').textContent = formatTime(wavesurfer.getDuration());
            }});

            function formatTime(seconds) {{
                const mins = Math.floor(seconds / 60);
                const secs = Math.floor(seconds % 60);
                return `${{mins}}:${{secs.toString().padStart(2, '0')}}`;
            }}

            function parseSRT(data) {{
                const srt = [];
                const regex = /(\\d+)\\s+(\\d{{2}}:\\d{{2}}:\\d{{2}},\\d{{3}})\\s-->\\s(\\d{{2}}:\\d{{2}}:\\d{{2}},\\d{{3}})\\s+([\\s\\S]*?)(?=\\n{{2,}}|$)/g;
                let match;
                while ((match = regex.exec(data)) !== null) {{
                    let text = match[4].replace(/\\n/g, ' ');
                    let speaker = "SPEAKER";
                    const speakerMatch = text.match(/^(SPEAKER_\\d+):\\s*/);
                    if (speakerMatch) {{
                        speaker = speakerMatch[1];
                        text = text.replace(/^(SPEAKER_\\d+):\\s*/, "");
                    }}
                    srt.push({{
                        index: parseInt(match[1]),
                        start: toSeconds(match[2]),
                        end: toSeconds(match[3]),
                        speaker,
                        text
                    }});
                }}
                return srt;
            }}

            function toSeconds(time) {{
                const [h, m, s] = time.replace(',', ':').split(':').map(Number);
                return h * 3600 + m * 60 + s;
            }}

            // Load transcript
            fetch("data:text/plain;base64,{transcript_b64}")
                .then(res => res.text())
                .then(srtText => {{
                    const cues = parseSRT(srtText);
                    const transcriptDiv = document.getElementById('transcript');
                    
                    cues.forEach((cue, i) => {{
                        const div = document.createElement('div');
                        div.className = 'dialog speaker-' + (cue.speaker.endsWith("0") ? "0" : "1");
                        div.id = 'cue-' + i;
                        
                        const speakerNum = cue.speaker.endsWith("0") ? "1" : "2";
                        const speakerName = `Speaker ${{speakerNum}}`;
                        
                        div.innerHTML = `
                            <span class="timestamp">${{formatTime(cue.start)}}</span>
                            <div class="speaker-avatar">${{speakerNum}}</div>
                            <div class="content">
                                <div class="speaker-name">${{speakerName}}</div>
                                <div class="text">${{cue.text}}</div>
                            </div>
                        `;
                        
                        div.onclick = () => {{
                            const progress = cue.start / wavesurfer.getDuration();
                            wavesurfer.seekTo(progress);
                        }};
                        
                        transcriptDiv.appendChild(div);
                    }});

                    // Highlight current segment
                    wavesurfer.on('audioprocess', function(time) {{
                        cues.forEach((cue, i) => {{
                            const div = document.getElementById('cue-' + i);
                            if (time >= cue.start && time <= cue.end) {{
                                div.classList.add('active');
                                div.scrollIntoView({{ block: 'center', behavior: 'smooth' }});
                            }} else {{
                                div.classList.remove('active');
                            }}
                        }});
                    }});
                }});
        </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    main()
