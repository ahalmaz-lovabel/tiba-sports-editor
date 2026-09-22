"""
Caption Generation Module
وحدة إنشاء الكابشنات

Generates professional bilingual captions with Academy branding.
"""

import json
from pathlib import Path
from typing import Optional, List, Dict
from datetime import timedelta


class CaptionGenerator:
    """Generate professional captions with timestamps and translations"""

    # Tiba Academy brand colors
    COLORS = {
        "navy": "#1A3A52",
        "orange": "#FF6B35",
        "white": "#FFFFFF",
        "black": "#000000",
    }

    def __init__(self):
        """Initialize caption generator"""
        self.font_size = 32
        self.line_height = 1.5

    def generate(
        self,
        transcript: str,
        translation: str,
        video_path: str,
        output_path: str,
        style: str = "bilingual"
    ) -> str:
        """
        Generate caption file (SRT format)

        Args:
            transcript: Arabic transcript
            translation: English translation
            video_path: Path to video (for metadata)
            output_path: Path to save caption file
            style: Caption style (bilingual, arabic_only, english_only)

        Returns:
            Path to generated caption file
        """
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Create SRT file
        video_name = Path(video_path).stem
        srt_path = output_dir / f"{video_name}_captions.srt"

        # Parse transcript into segments (simplified)
        segments = self._create_segments(transcript, translation)

        # Write SRT file
        with open(srt_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(segments, 1):
                f.write(f"{i}\n")
                f.write(f"{segment['time_start']} --> {segment['time_end']}\n")

                if style == "bilingual":
                    f.write(f"{segment['arabic']}\n{segment['english']}\n")
                elif style == "arabic_only":
                    f.write(f"{segment['arabic']}\n")
                elif style == "english_only":
                    f.write(f"{segment['english']}\n")

                f.write("\n")

        # Also create VTT file for web
        vtt_path = output_dir / f"{video_name}_captions.vtt"
        self._write_vtt(vtt_path, segments, style)

        # Create JSON metadata
        json_path = output_dir / f"{video_name}_captions.json"
        self._write_json(json_path, segments)

        print(f"   Captions saved: {srt_path}")
        return str(srt_path)

    def _create_segments(self, arabic: str, english: str) -> List[Dict]:
        """
        Create caption segments from full transcript

        Args:
            arabic: Full Arabic text
            english: Full English text

        Returns:
            List of segment dicts with timestamps and text
        """
        # Split into sentences
        arabic_sentences = self._split_sentences(arabic)
        english_sentences = self._split_sentences(english)

        # Align sentences
        num_segments = max(len(arabic_sentences), len(english_sentences))

        segments = []
        segment_duration = 2  # seconds per segment (estimate)

        for i in range(num_segments):
            start_time = i * segment_duration
            end_time = (i + 1) * segment_duration

            arabic_text = arabic_sentences[i] if i < len(arabic_sentences) else ""
            english_text = english_sentences[i] if i < len(english_sentences) else ""

            segments.append({
                "index": i + 1,
                "time_start": self._format_timestamp(start_time),
                "time_end": self._format_timestamp(end_time),
                "arabic": arabic_text.strip(),
                "english": english_text.strip(),
                "duration": segment_duration,
            })

        return segments

    def _split_sentences(self, text: str, max_length: int = 50) -> List[str]:
        """
        Split text into caption-friendly segments

        Args:
            text: Input text
            max_length: Maximum characters per segment

        Returns:
            List of text segments
        """
        if not text:
            return []

        # Split by Arabic/English sentence markers
        segments = []
        current = ""

        words = text.split()
        for word in words:
            if len(current) + len(word) + 1 > max_length:
                if current:
                    segments.append(current)
                current = word
            else:
                current += " " + word if current else word

        if current:
            segments.append(current)

        return segments

    def _write_vtt(self, path: Path, segments: List[Dict], style: str) -> None:
        """Write WebVTT format caption file"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write("WEBVTT\n\n")

            for segment in segments:
                f.write(f"{segment['time_start']} --> {segment['time_end']}\n")

                if style == "bilingual":
                    f.write(f"{segment['arabic']}\n{segment['english']}\n")
                elif style == "arabic_only":
                    f.write(f"{segment['arabic']}\n")
                elif style == "english_only":
                    f.write(f"{segment['english']}\n")

                f.write("\n")

    def _write_json(self, path: Path, segments: List[Dict]) -> None:
        """Write JSON metadata file"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump({
                "format": "json",
                "language": "ar-en",
                "segments": segments,
                "total_segments": len(segments),
            }, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _format_timestamp(seconds: float) -> str:
        """
        Format timestamp for caption file

        Args:
            seconds: Time in seconds

        Returns:
            Formatted timestamp (HH:MM:SS,mmm)
        """
        td = timedelta(seconds=seconds)
        hours = td.seconds // 3600
        minutes = (td.seconds % 3600) // 60
        secs = td.seconds % 60
        millis = int((seconds % 1) * 1000)

        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
