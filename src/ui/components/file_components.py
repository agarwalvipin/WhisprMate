"""File management UI components."""

from typing import List

import streamlit as st

from ...core.models import AudioFile
from ...services.file_manager import FileManagerService
from ...services.transcript_manager import TranscriptManagerService


class FileListComponent:
    """Component for displaying and managing audio files."""

    def __init__(
        self, file_manager: FileManagerService, transcript_manager: TranscriptManagerService
    ):
        """Initialize file list component.

        Args:
            file_manager: File manager service
            transcript_manager: Transcript manager service
        """
        self.file_manager = file_manager
        self.transcript_manager = transcript_manager

    def render_file_list(self, files: List[AudioFile]) -> None:
        """Render list of audio files.

        Args:
            files: List of audio files to display
        """
        if not files:
            st.info("📁 No audio files found. Upload your first file in the Upload tab!")
            return

        for file in files:
            self._render_file_card(file)

    def render_search_and_sort(self) -> tuple[str, str]:
        """Render search and sort controls.

        Returns:
            Tuple of (search_query, sort_option)
        """
        col1, col2 = st.columns([2, 1])

        with col1:
            search_query = st.text_input(
                "🔍 Search files", placeholder="Type to search...", key="file_search"
            )

        with col2:
            sort_options = [
                "Date created (newest)",
                "Date created (oldest)",
                "Title (A-Z)",
                "Title (Z-A)",
                "Duration (longest)",
                "Duration (shortest)",
            ]
            sort_option = st.selectbox("Sort by", sort_options, key="file_sort")

        return search_query, sort_option

    def _render_file_card(self, file: AudioFile) -> None:
        """Render individual file card.

        Args:
            file: Audio file to render
        """
        with st.container():
            # File card HTML
            created_date = file.created_at.strftime("%d/%m/%Y %H:%M") if file.created_at else "-"

            st.markdown(
                f"""
                <div class="file-card">
                    <div style="display: flex; justify-content: space-between;
                                align-items: center;">
                        <div>
                            <h4 style="margin: 0; color: #333;">{file.name}</h4>
                            <p style="margin: 5px 0; color: #666; font-size: 0.9em;">
                                📅 {created_date} •
                                ⏱️ {file.formatted_duration} •
                                📦 {file.formatted_size}
                            </p>
                        </div>
                    </div>
                </div>
            """,
                unsafe_allow_html=True,
            )

            # Action buttons
            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                if st.button("▶️ Play", key=f"play_{file.name}"):
                    st.session_state["player_file"] = file.name
                    st.session_state["current_page"] = "player"
                    st.rerun()

            with col2:
                if self.transcript_manager.transcript_exists(file):
                    transcript_content = self.transcript_manager.load_transcript(file)
                    if transcript_content:
                        st.download_button(
                            "📄 Download SRT",
                            transcript_content,
                            file_name=f"{file.name}.srt",
                            key=f"download_{file.name}",
                        )
                    else:
                        st.button(
                            "❌ No transcript", disabled=True, key=f"no_transcript_{file.name}"
                        )
                else:
                    st.button("❌ No transcript", disabled=True, key=f"no_transcript_{file.name}")

            with col3:
                if st.button("🗑️ Delete", key=f"delete_{file.name}"):
                    if self.file_manager.delete_file(file):
                        st.success(f"Deleted {file.name}")
                        st.rerun()
                    else:
                        st.error(f"Error deleting {file.name}")


class FileUploadComponent:
    """Component for file upload functionality."""

    def __init__(self, file_manager: FileManagerService):
        """Initialize file upload component.

        Args:
            file_manager: File manager service
        """
        self.file_manager = file_manager

    def render_upload_zone(self) -> None:
        """Render the file upload zone."""
        st.markdown(
            """
            <div class="upload-zone">
                <h3>🎵 Drag & Drop or Browse Files</h3>
                <p>Supported formats: WAV, MP3 • Max size: 50MB</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    def render_file_uploader(self) -> tuple[bool, AudioFile]:
        """Render file uploader and handle upload.

        Returns:
            Tuple of (file_uploaded, audio_file)
        """
        uploaded_file = st.file_uploader(
            "Choose an audio file",
            type=["wav", "mp3"],
            help="Upload a WAV or MP3 file for transcription and speaker diarization",
        )

        if uploaded_file is None:
            return False, None

        # Validate file size
        if uploaded_file.size > 50 * 1024 * 1024:
            st.error("❌ File too large. Please upload a file smaller than 50MB.")
            return False, None

        # Save file
        try:
            with st.spinner("💾 Saving file..."):
                audio_file = self.file_manager.save_uploaded_file(uploaded_file, uploaded_file.name)

            st.success(f"✅ Uploaded: {uploaded_file.name}")
            return True, audio_file

        except Exception as e:
            st.error(f"❌ Error uploading file: {str(e)}")
            return False, None

    def render_file_info(self, audio_file: AudioFile) -> None:
        """Render information about uploaded file.

        Args:
            audio_file: The uploaded audio file
        """
        if audio_file.duration_seconds:
            mins, secs = divmod(int(audio_file.duration_seconds), 60)
            st.info(f"📊 Duration: {mins}min {secs}sec")

    def render_processing_options(self) -> tuple[str, str]:
        """Render processing options controls.

        Returns:
            Tuple of (model_size, language)
        """
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

        return model_size, language
