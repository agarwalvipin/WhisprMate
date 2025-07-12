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

        # Audio player
        with open(audio_file.path, "rb") as f:
            audio_bytes = f.read()

        st.audio(
            audio_bytes, format="audio/wav" if player_file.lower().endswith(".wav") else "audio/mp3"
        )

        # Transcript section
        if self.transcript_manager.transcript_exists(audio_file):
            transcript = self.transcript_manager.load_transcript(audio_file)
            if transcript:
                st.subheader("📄 Transcript")
                st.text_area(
                    "Transcript Content",
                    transcript,
                    height=300,
                    disabled=True,
                    label_visibility="collapsed",
                )

                st.download_button(
                    "📄 Download Transcript",
                    transcript,
                    file_name=f"{player_file}.srt",
                    mime="text/plain",
                )
        else:
            st.warning("⚠️ Transcript not available. Please process this file first.")


def main():
    """Main entry point."""
    app = SpeakerDiarizationApp()
    app.run()


if __name__ == "__main__":
    main()
