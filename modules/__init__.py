"""
Tiba Sports Academy Video Editor - Core Modules
محرّر أكاديمية طيبة الرياضية - المكتبات الأساسية

Modules for video processing, transcription, translation, and branding.
"""

__version__ = "1.0.0"
__author__ = "Tiba Sports Academy"

from .detect_video_type import VideoTypeDetector
from .transcribe import Transcriber
from .translate import Translator
from .captions import CaptionGenerator
from .audio_mix import AudioMixer
from .video_process import VideoProcessor

__all__ = [
    'VideoTypeDetector',
    'Transcriber',
    'Translator',
    'CaptionGenerator',
    'AudioMixer',
    'VideoProcessor',
]
