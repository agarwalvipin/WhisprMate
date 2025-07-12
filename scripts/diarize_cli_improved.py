import argparse
import os

from dotenv import load_dotenv


def simulate_speaker_diarization(audio_file, segment_duration=10):
    """
    Simulate speaker diarization by creating alternating speaker segments
    """
    import soundfile as sf

    f = sf.SoundFile(audio_file)
    total_duration = len(f) / f.samplerate

    segments = []
    current_time = 0
    speaker_id = 0

    while current_time < total_duration:
        end_time = min(current_time + segment_duration, total_duration)
        segments.append(
            {
                "start": current_time,
                "end": end_time,
                "speaker": f"SPEAKER_{speaker_id:02d}",
            }
        )
        current_time = end_time
        speaker_id = (speaker_id + 1) % 2  # Alternate between SPEAKER_00 and SPEAKER_01

    return segments


def main():
    parser = argparse.ArgumentParser(
        description="Diarize and transcribe audio to SRT with speaker labels."
    )
    parser.add_argument("audio", help="Path to input audio file (wav/mp3)")
    parser.add_argument("-o", "--output", default="output.srt", help="Output SRT file")
    parser.add_argument(
        "--model",
        default="base",
        help="Whisper model size (tiny, base, small, medium, large)",
    )
    parser.add_argument(
        "--language", default=None, help="Language code (e.g., en, hi, etc.)"
    )
    parser.add_argument(
        "--no-diarization", action="store_true", help="Disable speaker diarization"
    )
    parser.add_argument(
        "--simulate-diarization",
        action="store_true",
        help="Simulate speaker diarization for testing",
    )
    parser.add_argument(
        "--hf-token", default=None, help="Hugging Face token for diarization"
    )
    parser.add_argument(
        "--segment-duration",
        type=int,
        default=10,
        help="Segment duration for simulated diarization (seconds)",
    )
    args = parser.parse_args()

    # Load .env if present
    load_dotenv()
    hf_token = args.hf_token or os.getenv("HF_TOKEN")

    if args.simulate_diarization:
        # Use simulated diarization for testing
        segments = simulate_speaker_diarization(args.audio, args.segment_duration)
    elif not args.no_diarization:
        from pyannote.audio import Pipeline

        if not hf_token:
            raise RuntimeError("Hugging Face token required for diarization.")
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1", use_auth_token=hf_token
        )
        diarization = pipeline(args.audio)
        segments = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            segments.append({"start": turn.start, "end": turn.end, "speaker": speaker})
    else:
        # No diarization: treat the whole file as one segment
        import soundfile as sf

        f = sf.SoundFile(args.audio)
        duration = len(f) / f.samplerate
        segments = [{"start": 0, "end": duration, "speaker": "SPEAKER_00"}]

    # Transcribe each segment with Whisper
    import soundfile as sf
    import whisper

    model = whisper.load_model(args.model)

    # Load the full audio file
    audio_data, sample_rate = sf.read(args.audio)

    srt_entries = []
    idx = 1
    for seg in segments:
        # Extract the segment from the audio
        start_sample = int(seg["start"] * sample_rate)
        end_sample = int(seg["end"] * sample_rate)
        segment_audio = audio_data[start_sample:end_sample].astype("float32")

        # Transcribe the segment
        result = model.transcribe(
            segment_audio,
            language=args.language,
            task="transcribe",
            verbose=False,
            fp16=False,
            temperature=0,
        )
        text = result["text"].strip()
        if text:
            srt_entries.append(
                {
                    "index": idx,
                    "start": seg["start"],
                    "end": seg["end"],
                    "speaker": seg["speaker"],
                    "text": f"{seg['speaker']}: {text}",
                }
            )
            idx += 1

    # Write SRT file
    def format_time(seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        ms = int((seconds - int(seconds)) * 1000)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    with open(args.output, "w", encoding="utf-8") as f:
        for entry in srt_entries:
            f.write(f"{entry['index']}\n")
            f.write(f"{format_time(entry['start'])} --> {format_time(entry['end'])}\n")
            f.write(f"{entry['text']}\n\n")

    print(f"SRT with speaker labels written to {args.output}")


if __name__ == "__main__":
    main()
