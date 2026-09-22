"""
Audio Processing Module
وحدة معالجة الصوت

Handles audio normalization, music ducking, and mixing.
"""

import os
import subprocess
import numpy as np
import librosa
import soundfile as sf
from pathlib import Path
from typing import Optional, Tuple


class AudioMixer:
    """Process and mix audio with normalization and music ducking"""

    def __init__(self):
        """Initialize audio mixer"""
        self.target_loudness = -14.0  # LUFS (Loudness Units relative to Full Scale)
        self.duck_level = -15  # dB reduction for music during speech
        self.duck_speed = 0.3  # Fade speed (0-1)

    def process(
        self,
        video_path: str,
        transcript: str,
        output_path: str
    ) -> str:
        """
        Process audio: normalize loudness and duck music during speech

        Args:
            video_path: Path to input video
            transcript: Transcript text (used to identify speech segments)
            output_path: Path to save processed audio

        Returns:
            Path to processed audio file
        """
        video_path = Path(video_path)
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Extract audio from video
        audio_file = output_dir / f"{video_path.stem}_extracted.wav"
        self._extract_audio(str(video_path), str(audio_file))

        # Load and process audio
        y, sr = librosa.load(str(audio_file), sr=None)

        # Normalize loudness
        y_normalized = self._normalize_loudness(y, sr)

        # Apply music ducking (if background music exists)
        y_processed = self._apply_ducking(y_normalized, sr)

        # Save processed audio
        output_audio = output_dir / f"{video_path.stem}_processed.wav"
        sf.write(str(output_audio), y_processed, sr)

        # Clean up temporary files
        if audio_file.exists():
            audio_file.unlink()

        print(f"   Audio processed: {output_audio}")
        return str(output_audio)

    def _extract_audio(self, video_path: str, output_audio: str) -> None:
        """
        Extract audio track from video using FFmpeg

        Args:
            video_path: Path to video file
            output_audio: Path to save audio
        """
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-q:a', '9',
            '-n',  # Don't overwrite
            output_audio
        ]

        try:
            subprocess.run(cmd, capture_output=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  Audio extraction error: {e}")

    def _normalize_loudness(self, y: np.ndarray, sr: int) -> np.ndarray:
        """
        Normalize audio to target loudness (LUFS)

        Args:
            y: Audio signal
            sr: Sample rate

        Returns:
            Normalized audio signal
        """
        # Calculate current loudness
        # Simplified: use RMS for loudness estimation
        rms = np.sqrt(np.mean(y ** 2))

        # Target RMS value for -14 LUFS (approximate)
        # -14 LUFS ≈ -0.18 dBFS RMS (rough conversion)
        target_rms = 10 ** (self.target_loudness / 20)

        if rms > 0:
            gain = target_rms / rms
            y_normalized = y * gain

            # Prevent clipping
            max_val = np.max(np.abs(y_normalized))
            if max_val > 1.0:
                y_normalized = y_normalized / (max_val * 1.05)
        else:
            y_normalized = y

        return y_normalized

    def _apply_ducking(self, y: np.ndarray, sr: int) -> np.ndarray:
        """
        Apply automatic ducking (reduce volume during speech)

        Args:
            y: Audio signal
            sr: Sample rate

        Returns:
            Audio with ducking applied
        """
        # Detect speech activity using energy
        hop_length = 512
        S = librosa.stft(y, hop_length=hop_length)
        magnitude = np.abs(S)

        # Calculate energy in frequency bands
        power = np.mean(magnitude ** 2, axis=0)
        power_db = librosa.power_to_db(power, ref=np.max(power))

        # Simple speech detection threshold
        speech_threshold = -30  # dB
        speech_activity = power_db > speech_threshold

        # Create ducking envelope
        frame_length = len(speech_activity)
        duck_envelope = np.ones(frame_length)

        # Convert ducking level to linear gain
        duck_gain = 10 ** (self.duck_level / 20)

        for i in range(frame_length):
            if speech_activity[i]:
                duck_envelope[i] = duck_gain

        # Smooth the envelope to avoid clicks
        duck_envelope = self._smooth_envelope(duck_envelope)

        # Convert back to sample domain
        duck_samples = np.interp(
            np.arange(len(y)),
            np.linspace(0, len(y), len(duck_envelope)),
            duck_envelope
        )

        # Apply ducking
        y_ducked = y * duck_samples

        return y_ducked

    def _smooth_envelope(
        self,
        envelope: np.ndarray,
        window_size: int = 5
    ) -> np.ndarray:
        """
        Smooth envelope to prevent clicks

        Args:
            envelope: Envelope array
            window_size: Smoothing window size

        Returns:
            Smoothed envelope
        """
        from scipy.ndimage import uniform_filter1d
        return uniform_filter1d(envelope, size=window_size, mode='nearest')

    def get_stats(self, audio_path: str) -> dict:
        """
        Get audio statistics

        Args:
            audio_path: Path to audio file

        Returns:
            Dictionary with audio stats
        """
        y, sr = librosa.load(audio_path, sr=None)

        rms = np.sqrt(np.mean(y ** 2))
        peak = np.max(np.abs(y))
        duration = librosa.get_duration(y=y, sr=sr)

        return {
            "sample_rate": sr,
            "duration": duration,
            "rms_level": 20 * np.log10(rms + 1e-10),
            "peak_level": 20 * np.log10(peak + 1e-10),
        }
