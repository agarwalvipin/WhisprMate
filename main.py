"""Main application entry point using refactored architecture."""

import streamlit as st

from config.settings import AppConfig, UIConfig
from src.services.audio_processor import AudioProcessorService
from src.services.auth_service import AuthenticationService
from src.services.file_manager import FileManagerService
from src.services.transcript_manager import TranscriptManagerService
from src.ui.components.auth import AuthComponent
from src.ui.components.file_components import FileListComponent, FileUploadComponent
from src.utils.helpers import filter_audio_files, sort_audio_files


class SpeakerDiarizationApp:
    """Main application class following SOLID principles."""

    def __init__(self):
        """Initialize the application with dependency injection."""
        # Initialize services (Dependency Injection)
        self.auth_service = AuthenticationService(enable_auth=AppConfig.ENABLE_AUTH)
        self.file_manager = FileManagerService()
        self.transcript_manager = TranscriptManagerService()
        self.audio_processor = AudioProcessorService()

        # Initialize UI components
        self.auth_component = AuthComponent(self.auth_service)
        self.file_list_component = FileListComponent(self.file_manager, self.transcript_manager)
        self.file_upload_component = FileUploadComponent(self.file_manager)

        # Initialize session state
        self._init_session_state()

    def _init_session_state(self) -> None:
        """Initialize Streamlit session state."""
        if "current_page" not in st.session_state:
            st.session_state.current_page = "dashboard"

    def run(self) -> None:
        """Run the main application."""
        # Configure Streamlit page
        st.set_page_config(
            page_title=AppConfig.PAGE_TITLE,
            layout=AppConfig.LAYOUT,
            initial_sidebar_state="expanded",
            menu_items=UIConfig.MENU_ITEMS,
        )

        # Apply custom CSS
        st.markdown(UIConfig.MAIN_HEADER_CSS, unsafe_allow_html=True)

        # Check authentication
        if not self.auth_component.require_authentication():
            return

        # Render header
        self._render_header()

        # Handle navigation
        page = st.session_state.current_page
        if page == "player":
            self._show_player_page()
            return

        # Main content with tabs
        tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📤 Upload", "⚙️ Processing Status"])

        with tab1:
            self._show_dashboard()

        with tab2:
            self._show_upload_section()

        with tab3:
            self._show_processing_status()

    def _render_header(self) -> None:
        """Render application header."""
        st.markdown(
            """
            <div class="main-header">
                <h1>🎙️ Speaker Diarization & Transcription</h1>
                <p>
                   Upload audio files and get AI-powered transcriptions with
                   speaker identification
                </p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    def _show_dashboard(self) -> None:
        """Display the main dashboard with file management."""
        st.header("📊 My Audio Files")

        # Search and sort controls
        search_query, sort_option = self.file_list_component.render_search_and_sort()

        # Get and process files
        files = self.file_manager.get_audio_files()
        files = filter_audio_files(files, search_query)
        files = sort_audio_files(files, sort_option)

        # Display files
        self.file_list_component.render_file_list(files)

    def _show_upload_section(self) -> None:
        """Display the file upload interface."""
        st.header("📤 Upload Audio File")

        # Upload zone
        self.file_upload_component.render_upload_zone()

        # File uploader
        file_uploaded, audio_file = self.file_upload_component.render_file_uploader()

        if file_uploaded and audio_file:
            # Show file info
            self.file_upload_component.render_file_info(audio_file)

            # Processing options
            model_size, language = self.file_upload_component.render_processing_options()

            # Start processing button
            if st.button("🚀 Start Processing", type="primary"):
                self._process_audio_file(audio_file, model_size, language)

    def _show_processing_status(self) -> None:
        """Display processing status and system information."""
        st.header("⚙️ Processing Status")

        # System metrics (placeholder)
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
        self._show_processing_queue()

    def _show_processing_queue(self) -> None:
        """Show current processing queue status."""
        files = self.file_manager.get_audio_files()
        processing_files = []
        completed_files = []

        for file in files:
            if self.transcript_manager.transcript_exists(file):
                completed_files.append(file)
            else:
                processing_files.append(file)

        if processing_files:
            st.warning(f"⏳ {len(processing_files)} files waiting to be processed")
            for file in processing_files:
                st.markdown(
                    f"""
                    <div style="padding: 10px; background: #fff3cd;
                                border-radius: 5px; margin: 5px 0;">
                        <span class="status-indicator status-processing"></span>
                        <strong>{file.name}</strong> - Waiting for processing
                    </div>
                """,
                    unsafe_allow_html=True,
                )

        if completed_files:
            st.success(f"✅ {len(completed_files)} files processed successfully")
            for file in completed_files:
                st.markdown(
                    f"""
                    <div style="padding: 10px; background: #d4edda;
                                border-radius: 5px; margin: 5px 0;">
                        <span class="status-indicator status-completed"></span>
                        <strong>{file.name}</strong> - Processing completed
                    </div>
                """,
                    unsafe_allow_html=True,
                )

        if not processing_files and not completed_files:
            st.info("📝 No files in queue. Upload files to get started!")

    def _process_audio_file(self, audio_file, model_size: str, language: str) -> None:
        """Process audio file with given options."""
        from src.core.models import ProcessingOptions

        # Create processing options
        options = ProcessingOptions(
            model_size=model_size, language=language, enable_diarization=True
        )

        # Estimate processing time
        if audio_file.duration_seconds:
            estimated_time = self.audio_processor.estimate_processing_time(
                audio_file.duration_seconds, options
            )
            st.info(f"⏱️ Estimated processing time: {estimated_time:.0f} seconds")

        # Process the file
        with st.spinner("🤖 Processing audio... This may take a few minutes."):
            try:
                # In a real async implementation, this would be await
                # For now, we'll use a synchronous approach
                import asyncio

                result = asyncio.run(self.audio_processor.process_audio(audio_file, options))

                if result.status.value == "completed":
                    # Save transcript
                    self.transcript_manager.save_transcript(audio_file, result)

                    st.success("🎉 Processing complete!")
                    st.balloons()

                    # Show preview
                    if result.srt_content:
                        preview = result.srt_content[:500] + "..."
                        st.subheader("📄 Transcript Preview")
                        st.text_area(
                            "Transcript Preview",
                            preview,
                            height=150,
                            disabled=True,
                            label_visibility="collapsed",
                        )

                        col1, col2 = st.columns(2)
                        with col1:
                            st.download_button(
                                "📄 Download Full Transcript",
                                result.srt_content,
                                file_name=f"{audio_file.name}.srt",
                            )
                        with col2:
                            if st.button("▶️ Open Player"):
                                st.session_state["player_file"] = audio_file.name
                                st.session_state["current_page"] = "player"
                                st.rerun()
                else:
                    st.error(f"❌ Processing failed: {result.error_message}")

            except Exception as e:
                st.error(f"❌ Processing error: {str(e)}")

    def _show_player_page(self) -> None:
        """Display the enhanced audio player interface."""
        if "player_file" not in st.session_state:
            st.error("No file selected for playback")
            return

        player_file = st.session_state["player_file"]

        # Find the audio file
        files = self.file_manager.get_audio_files()
        audio_file = next((f for f in files if f.name == player_file), None)

        if not audio_file:
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

        # Check if transcript exists
        if self.transcript_manager.transcript_exists(audio_file):
            transcript = self.transcript_manager.load_transcript(audio_file)
            if transcript:
                # Create interactive audio player with transcript
                self._render_interactive_player(audio_file, transcript)

                # Download button for transcript
                st.download_button(
                    "📄 Download Transcript",
                    transcript,
                    file_name=f"{player_file}.srt",
                    mime="text/plain",
                )
        else:
            st.warning("⚠️ Transcript not available. Please process this file first.")

    def _render_interactive_player(self, audio_file, transcript: str) -> None:
        """Render the interactive audio player with transcript dialog."""
        import base64

        from src.utils.helpers import get_audio_mime_type

        # Read and encode audio file
        with open(audio_file.path, "rb") as f:
            audio_bytes = f.read()

        audio_base64 = base64.b64encode(audio_bytes).decode()
        audio_mime = get_audio_mime_type(audio_file.name)

        # Escape transcript content for JavaScript
        transcript_escaped = (
            transcript.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        )

        # Create the interactive player HTML
        player_html = (
            f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <title>Audio Player with Transcript</title>
          <style>
            body {{
              font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
              margin: 0;
              background-color: #ffffff;
              padding: 10px;
            }}
            .player-container {{
              background: white;
              border-radius: 8px;
              padding: 0;
              margin-bottom: 10px;
              border: 1px solid #e0e0e0;
              box-shadow: 0 2px 4px rgba(0,0,0,0.1);
              overflow: visible;
              min-height: 80px;
            }}
            #transcript {{
              max-height: 600px;
              overflow-y: auto;
              background: white;
              padding: 0;
              margin: 0;
            }}
            .dialog {{
              display: flex;
              align-items: flex-start;
              margin: 0;
              padding: 12px 16px;
              gap: 12px;
              border-bottom: 1px solid #f0f0f0;
            }}
            .dialog:last-child {{
              border-bottom: none;
            }}
            .timestamp {{
              font-size: 11px;
              color: #666;
              min-width: 35px;
              margin-top: 2px;
              font-weight: 500;
            }}
            .speaker-avatar {{
              width: 20px;
              height: 20px;
              border-radius: 50%;
              display: flex;
              align-items: center;
              justify-content: center;
              color: white;
              font-weight: bold;
              font-size: 9px;
              flex-shrink: 0;
              margin-top: 0px;
            }}
            .speaker-0 .speaker-avatar {{ background-color: #4A90E2; }}
            .speaker-1 .speaker-avatar {{ background-color: #E24A4A; }}
            .content {{
              flex: 1;
              margin-left: 6px;
            }}
            .speaker-name {{
              font-weight: 600;
              font-size: 13px;
              color: #333;
              margin-bottom: 2px;
            }}
            .speaker-0 .speaker-name {{ color: #4A90E2; }}
            .speaker-1 .speaker-name {{ color: #E24A4A; }}
            .text {{
              color: #333;
              line-height: 1.4;
              font-size: 13px;
              margin: 0;
            }}
            .active {{
              background-color: #E3F2FD;
              border-left: 3px solid #2196F3;
            }}
            audio {{
              width: 100%;
              height: auto;
              min-height: 54px;
              margin: 0;
              padding: 8px;
              border-radius: 8px 8px 0 0;
              outline: none;
              display: block;
              background: #f8f9fa;
            }}
            audio::-webkit-media-controls-panel {{
              background-color: #f8f9fa;
              border-radius: 8px 8px 0 0;
            }}
            audio::-webkit-media-controls-enclosure {{
              background-color: #f8f9fa;
              border-radius: 8px 8px 0 0;
            }}
            .progress-container {{
              background: #f5f5f5;
              padding: 8px 16px;
              border-top: 1px solid #e0e0e0;
              display: flex;
              align-items: center;
              gap: 10px;
              font-size: 12px;
              color: #666;
            }}
            .time-display {{
              font-family: monospace;
              font-size: 11px;
            }}
          </style>
        </head>
        <body>
          <div class="player-container">
            <audio id="audio" controls preload="metadata">
              <source src="data:{audio_mime};base64,{audio_base64}" type="{audio_mime}">
              Your browser does not support the audio element.
            </audio>
            <div class="progress-container">
              <span class="time-display" id="current-time">00:00</span>
              <span>/</span>
              <span class="time-display" id="total-time">00:00</span>
            </div>
          </div>
          <div id="transcript"></div>
          <script>
            function parseSRT(data) {{
              const srt = [];
              const regex = /(\\d+)\\s+(\\d{{2}}:\\d{{2}}:\\d{{2}},\\d{{3}})\\s-->\\s+"""
            + f"""(\\d{{2}}:\\d{{2}}:\\d{{2}},\\d{{3}})\\s+([\\s\\S]*?)(?=\\n{{2,}}|$)/g;
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

            // Parse the transcript data
            const srtText = "{transcript_escaped}";
            const cues = parseSRT(srtText);
            const transcriptDiv = document.getElementById('transcript');

            // Group consecutive segments by speaker
            const groupedCues = [];
            let currentGroup = null;

            cues.forEach((cue, i) => {{
              if (!currentGroup || currentGroup.speaker !== cue.speaker) {{
                // Start a new group
                currentGroup = {{
                  speaker: cue.speaker,
                  start: cue.start,
                  end: cue.end,
                  texts: [cue.text],
                  originalIndices: [i]
                }};
                groupedCues.push(currentGroup);
              }} else {{
                // Add to existing group
                currentGroup.end = cue.end;
                currentGroup.texts.push(cue.text);
                currentGroup.originalIndices.push(i);
              }}
            }});

            // Render grouped dialogs
            groupedCues.forEach((group, groupIndex) => {{
              const div = document.createElement('div');
              div.className = 'dialog speaker-' + (group.speaker.endsWith("0") ? "0" : "1");
              div.id = 'group-' + groupIndex;
              div.dataset.originalIndices = group.originalIndices.join(',');

              // Format time for display
              const formatTime = (seconds) => {{
                const mins = Math.floor(seconds / 60);
                const secs = Math.floor(seconds % 60);
                return `${{mins.toString().padStart(2, '0')}}:${{secs.toString().padStart(2, '0')}}`;
              }};

              // Determine speaker number and name
              const speakerNum = group.speaker.endsWith("0") ? "1" : "2";
              const speakerName = `Speaker ${{speakerNum}}`;

              // Combine texts with paragraph breaks
              const combinedText = group.texts.map(text => `<p style="margin: 0 0 8px 0; line-height: 1.4;">${{text}}</p>`).join('');

              div.innerHTML = `
                <span class="timestamp">${{formatTime(group.start)}}</span>
                <div class="speaker-avatar">${{speakerNum}}</div>
                <div class="content">
                  <div class="speaker-name">${{speakerName}}</div>
                  <div class="text">${{combinedText}}</div>
                </div>
              `;
              transcriptDiv.appendChild(div);
            }});

            // Audio time update handler
            const audio = document.getElementById('audio');
            const currentTimeDisplay = document.getElementById('current-time');
            const totalTimeDisplay = document.getElementById('total-time');
            
            // Variables to track user interaction with scroll
            let userIsScrolling = false;
            let scrollTimeout;
            let lastActiveElement = null;
            
            // Format time for display
            const formatTimeDisplay = (seconds) => {{
              const mins = Math.floor(seconds / 60);
              const secs = Math.floor(seconds % 60);
              return `${{mins.toString().padStart(2, '0')}}:${{secs.toString().padStart(2, '0')}}`;
            }};
            
            // Update duration when metadata loads
            audio.addEventListener('loadedmetadata', () => {{
              totalTimeDisplay.textContent = formatTimeDisplay(audio.duration);
            }});
            
            // Detect user scrolling
            transcriptDiv.addEventListener('scroll', () => {{
              userIsScrolling = true;
              clearTimeout(scrollTimeout);
              // Reset user scrolling flag after 3 seconds of no scrolling
              scrollTimeout = setTimeout(() => {{
                userIsScrolling = false;
              }}, 3000);
            }});
            
            audio.ontimeupdate = () => {{
              // Update time display
              currentTimeDisplay.textContent = formatTimeDisplay(audio.currentTime);
              
              // Update active transcript segment
              groupedCues.forEach((group, groupIndex) => {{
                const div = document.getElementById('group-' + groupIndex);
                if (audio.currentTime >= group.start && audio.currentTime <= group.end) {{
                  div.classList.add('active');
                  
                  // Only auto-scroll if user is not manually scrolling
                  // and this is a new active element
                  if (!userIsScrolling && div !== lastActiveElement) {{
                    div.scrollIntoView({{ 
                      block: 'nearest', 
                      behavior: 'smooth',
                      inline: 'nearest'
                    }});
                    lastActiveElement = div;
                  }}
                }} else {{
                  div.classList.remove('active');
                }}
              }});
            }};
            
            // Click to seek functionality for grouped dialogs
            groupedCues.forEach((group, groupIndex) => {{
              const div = document.getElementById('group-' + groupIndex);
              div.style.cursor = 'pointer';
              div.addEventListener('click', () => {{
                audio.currentTime = group.start;
              }});
            }});
          </script>
        </body>
        </html>
        """
        )

        # Display the interactive player
        st.components.v1.html(player_html, height=700, scrolling=True)


def main():
    """Main entry point."""
    app = SpeakerDiarizationApp()
    app.run()


if __name__ == "__main__":
    main()
