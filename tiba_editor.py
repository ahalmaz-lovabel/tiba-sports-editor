#!/usr/bin/env python3
"""
Tiba Sports Academy Video Editor - Main Program
محرّر أكاديمية طيبة الرياضية - البرنامج الرئيسي

A specialized video processing tool for Tiba Sports Academy with:
- Intelligent video type detection
- Arabic-English captions with automatic translation
- Audio normalization (-14 LUFS)
- Automatic music ducking during speech
- Academy logo overlay
"""

import argparse
import sys
from pathlib import Path
from modules.detect_video_type import VideoTypeDetector
from modules.transcribe import Transcriber
from modules.translate import Translator
from modules.captions import CaptionGenerator
from modules.audio_mix import AudioMixer
from modules.video_process import VideoProcessor


class TibaEditor:
    def __init__(self, output_dir="output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.detector = VideoTypeDetector()
        self.transcriber = Transcriber()
        self.translator = Translator()
        self.caption_gen = CaptionGenerator()
        self.audio_mixer = AudioMixer()
        self.video_proc = VideoProcessor()

    def process(self, video_path, output_name=None):
        """Process video with complete pipeline"""
        video_path = Path(video_path)

        if not video_path.exists():
            print(f"❌ Error: Video file not found: {video_path}")
            return False

        print(f"🎬 Processing video: {video_path.name}")

        # Step 1: Detect video type
        print("🔍 Detecting video type...")
        video_type = self.detector.detect(str(video_path))
        print(f"   Type: {video_type}")

        # Step 2: Transcribe audio
        print("🗣️  Transcribing audio...")
        transcript = self.transcriber.transcribe(str(video_path))
        if not transcript:
            print("❌ Transcription failed")
            return False

        # Step 3: Translate to English
        print("🌐 Translating to English...")
        translation = self.translator.translate(transcript, source_lang="ar", target_lang="en")

        # Step 4: Generate captions
        print("📝 Generating captions...")
        caption_file = self.caption_gen.generate(
            transcript=transcript,
            translation=translation,
            video_path=str(video_path),
            output_path=str(self.output_dir)
        )

        # Step 5: Process audio (normalize + duck music)
        print("🔊 Processing audio...")
        audio_file = self.audio_mixer.process(
            video_path=str(video_path),
            transcript=transcript,
            output_path=str(self.output_dir)
        )

        # Step 6: Add logo and process video
        print("🎨 Adding logo and processing video...")
        output_file = output_name or f"tiba_{video_path.stem}_final.mp4"
        output_path = self.output_dir / output_file

        self.video_proc.process(
            video_path=str(video_path),
            audio_path=audio_file,
            caption_path=caption_file,
            output_path=str(output_path)
        )

        print(f"✅ Done! Output: {output_path}")
        return True


def main():
    parser = argparse.ArgumentParser(
        description='Tiba Sports Academy Video Editor - محرّر أكاديمية طيبة الرياضية'
    )

    parser.add_argument('video', help='Video file path')
    parser.add_argument('-o', '--output', help='Output file name', default=None)
    parser.add_argument('--output-dir', help='Output directory', default='output')

    args = parser.parse_args()

    editor = TibaEditor(output_dir=args.output_dir)
    success = editor.process(args.video, output_name=args.output)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
