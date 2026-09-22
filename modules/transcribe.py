"""
Transcription Module - Speech-to-Text
وحدة التفريغ - تحويل الكلام إلى نص

Uses OpenAI Whisper for accurate Arabic speech transcription.
"""

import whisper
from pathlib import Path
import json
from datetime import timedelta


class Transcriber:
    """Transcribe audio from video using Whisper"""

    def __init__(self, model_name: str = "base"):
        """
        Initialize transcriber

        Args:
            model_name: Whisper model size (tiny, base, small, medium, large)
        """
        self.model = whisper.load_model(model_name)

    def transcribe(self, video_path: str, language: str = "ar") -> str:
        """
        Transcribe audio from video

        Args:
            video_path: Path to video file
            language: Language code (default: "ar" for Arabic)

        Returns:
            Transcribed text in Arabic
        """
        video_path = Path(video_path)

        if not video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

        print(f"   Transcribing: {video_path.name}")

        result = self.model.transcribe(
            str(video_path),
            language=language,
            task="transcribe",
            verbose=False
        )

        transcript_text = result.get("text", "").strip()
        return transcript_text

    def transcribe_with_timestamps(
        self,
        video_path: str,
        language: str = "ar"
    ) -> dict:
        """
        Transcribe with segment timestamps

        Args:
            video_path: Path to video file
            language: Language code

        Returns:
            Dict with text and segments (each with timestamp and text)
        """
        video_path = Path(video_path)

        result = self.model.transcribe(
            str(video_path),
            language=language,
            task="transcribe",
            verbose=False
        )

        segments = []
        for seg in result.get("segments", []):
            segments.append({
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"],
                "timestamp": self._format_timestamp(seg["start"]),
            })

        return {
            "text": result.get("text", "").strip(),
            "language": result.get("language", "ar"),
            "segments": segments,
            "duration": result.get("duration", 0),
        }

    def transcribe_to_file(
        self,
        video_path: str,
        output_path: str,
        language: str = "ar"
    ) -> None:
        """
        Transcribe and save to JSON file

        Args:
            video_path: Path to video file
            output_path: Path to save transcript (JSON)
            language: Language code
        """
        transcript_data = self.transcribe_with_timestamps(video_path, language)

        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(transcript_data, f, ensure_ascii=False, indent=2)

        print(f"   Transcript saved: {output_file}")

    @staticmethod
    def _format_timestamp(seconds: float) -> str:
        """Format seconds to HH:MM:SS"""
        td = timedelta(seconds=seconds)
        hours, remainder = divmod(int(td.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
