"""
Video Processing Module
وحدة معالجة الفيديو

Handles video composition, logo overlay, and caption embedding.
"""

import subprocess
import os
from pathlib import Path
from typing import Optional, Tuple


class VideoProcessor:
    """Process and compose final video with captions and logo"""

    # Tiba Academy brand colors
    BRAND_NAVY = "#1A3A52"
    BRAND_ORANGE = "#FF6B35"

    def __init__(self):
        """Initialize video processor"""
        self.logo_path = Path(__file__).parent.parent / "assets" / "tiba_logo.png"
        self.logo_size = 120  # pixels
        self.logo_position = "top_right"  # top_right, top_left, bottom_right, bottom_left

    def process(
        self,
        video_path: str,
        audio_path: str,
        caption_path: str,
        output_path: str,
        logo_path: Optional[str] = None
    ) -> None:
        """
        Compose final video with audio, captions, and logo

        Args:
            video_path: Original video file
            audio_path: Processed audio file
            caption_path: Caption file (SRT)
            output_path: Output video file
            logo_path: Optional custom logo path
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if logo_path:
            self.logo_path = Path(logo_path)

        # Build FFmpeg command
        ffmpeg_cmd = self._build_ffmpeg_command(
            video_path,
            audio_path,
            caption_path,
            str(output_path)
        )

        # Execute FFmpeg
        try:
            subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
            print(f"   Video processed: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  Video processing error: {e}")
            raise

    def _build_ffmpeg_command(
        self,
        video_path: str,
        audio_path: str,
        caption_path: str,
        output_path: str
    ) -> list:
        """
        Build FFmpeg command for video composition

        Args:
            video_path: Video input
            audio_path: Audio input
            caption_path: Caption file
            output_path: Output file

        Returns:
            FFmpeg command as list
        """
        # Get video info for logo positioning
        video_width, video_height = self._get_video_dimensions(video_path)

        # Calculate logo position (top right corner)
        logo_x = max(0, video_width - self.logo_size - 20)
        logo_y = 20

        # Build filter chain
        filter_chain = []

        # 1. Add logo overlay if exists
        if self.logo_path.exists():
            filter_chain.append(
                f"[0:v][1:v]overlay={logo_x}:{logo_y}:enable='between(t\\\\,0\\\\,9999)'"
                f"[v_with_logo]"
            )
        else:
            filter_chain.append("[0:v]copy[v_with_logo]")

        # 2. Add captions/subtitles
        filter_chain.append(
            f"[v_with_logo]subtitles={caption_path}:force_style='FontSize=32,PrimaryColour=&H00FFFFFF,"
            f"BackColour=&H80000000,Outline=2,Shadow=1,MarginL=10,MarginR=10,MarginV=20'"
            f"[v_final]"
        )

        # Build command
        cmd = ['ffmpeg', '-i', video_path]

        # Add audio input
        cmd.extend(['-i', audio_path])

        # Add logo input if exists
        if self.logo_path.exists():
            cmd.extend(['-i', str(self.logo_path)])

        # Add filter complex
        filter_str = ",".join(filter_chain)
        cmd.extend(['-filter_complex', filter_str])

        # Output settings
        cmd.extend([
            '-map', '[v_final]',  # Video stream
            '-map', '1:a',  # Audio stream from audio file
            '-c:v', 'libx264',  # H.264 codec
            '-c:a', 'aac',  # AAC audio codec
            '-b:a', '192k',  # Audio bitrate
            '-preset', 'medium',  # Encoding speed/quality tradeoff
            '-y',  # Overwrite output file
            output_path
        ])

        return cmd

    def _get_video_dimensions(self, video_path: str) -> Tuple[int, int]:
        """
        Get video dimensions using FFprobe

        Args:
            video_path: Video file path

        Returns:
            Tuple of (width, height)
        """
        try:
            cmd = [
                'ffprobe',
                '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height',
                '-of', 'csv=p=0',
                video_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            width, height = map(int, result.stdout.strip().split(','))
            return width, height

        except Exception as e:
            print(f"   ⚠️  Could not determine video dimensions: {e}")
            # Return default dimensions
            return 1920, 1080

    def add_watermark(
        self,
        video_path: str,
        watermark_text: str,
        output_path: str,
        position: str = "bottom_right"
    ) -> None:
        """
        Add text watermark to video

        Args:
            video_path: Input video
            watermark_text: Text to add
            output_path: Output video
            position: Watermark position
        """
        # Calculate text position
        positions = {
            "top_left": "(10,10)",
            "top_right": "(W-300,10)",
            "bottom_left": "(10,H-30)",
            "bottom_right": "(W-300,H-30)",
        }

        pos = positions.get(position, positions["bottom_right"])

        # FFmpeg filter for text watermark
        filter_str = (
            f"drawtext=text='{watermark_text}':"
            f"x={pos}:"
            f"y=x:fontsize=24:fontcolor=white:"
            f"borderw=2:bordercolor=black"
        )

        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', filter_str,
            '-c:a', 'copy',
            '-y',
            output_path
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"   Watermark added: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  Watermark error: {e}")

    def set_logo(self, logo_path: str, size: int = 120) -> None:
        """
        Set custom logo

        Args:
            logo_path: Path to logo image
            size: Logo size in pixels
        """
        self.logo_path = Path(logo_path)
        self.logo_size = size

    def set_logo_position(self, position: str) -> None:
        """
        Set logo position

        Args:
            position: top_right, top_left, bottom_right, bottom_left
        """
        valid_positions = ["top_right", "top_left", "bottom_right", "bottom_left"]
        if position in valid_positions:
            self.logo_position = position
        else:
            print(f"   ⚠️  Invalid position: {position}")
