# Tiba Sports Academy Video Editor - Skill Guide
# محرّر أكاديمية طيبة - دليل الاستخدام

## Overview
Specialized video processing tool for Tiba Sports Academy with intelligent video detection, automatic transcription, translation, and professional output.

## Features at a Glance

1. **Intelligent Video Analysis**: Automatically detects video type (speaker vs. sports action)
2. **Automatic Transcription**: Converts Arabic speech to text using OpenAI Whisper
3. **Live Translation**: Translates Arabic captions to English in real-time
4. **Audio Normalization**: Ensures broadcast-standard audio levels (-14 LUFS)
5. **Music Ducking**: Automatically reduces background music during speech
6. **Professional Branding**: Adds academy logo with official color scheme
7. **Bilingual Captions**: Creates dual-language subtitle files (Arabic + English)

## Installation

### Quick Setup
```bash
cd tiba-sports-editor
chmod +x setup.sh
./setup.sh
```

### Manual Setup
```bash
# Install system dependencies
# macOS: brew install ffmpeg
# Linux: sudo apt-get install ffmpeg

# Install Python packages
pip install -r requirements.txt

# Set up Google credentials (for translation)
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
```

## Usage

### Basic Command
```bash
python3 tiba_editor.py input_video.mp4
```

### With Options
```bash
# Custom output name
python3 tiba_editor.py input.mp4 -o "academy_presentation.mp4"

# Custom output directory
python3 tiba_editor.py input.mp4 --output-dir ./processed_videos
```

### Processing Pipeline
The tool automatically:
1. Detects if video is speaker/presentation or sports action
2. Extracts and transcribes audio to Arabic text
3. Translates text to English
4. Generates SRT/VTT subtitle files
5. Normalizes audio to -14 LUFS
6. Applies music ducking during speech
7. Overlays academy logo
8. Embeds captions and audio
9. Outputs final video

## Configuration

### Audio Settings
Edit in `modules/audio_mix.py`:
```python
self.target_loudness = -14.0  # LUFS
self.duck_level = -15  # dB reduction
self.duck_speed = 0.3  # Fade speed
```

### Caption Style
Generated captions support three styles:
- **bilingual**: Arabic above, English below (default)
- **arabic_only**: Only Arabic text
- **english_only**: Only English text

### Logo Positioning
Edit in `modules/video_process.py`:
```python
self.logo_position = "top_right"  # or top_left, bottom_right, bottom_left
self.logo_size = 120  # pixels
```

## Project Structure

```
tiba-sports-editor/
├── tiba_editor.py              # Main entry point
├── requirements.txt            # Python dependencies
├── setup.sh                    # Installation script
├── README.md                   # Full documentation
├── SKILL.md                    # This file
│
├── modules/                    # Core functionality
│   ├── __init__.py
│   ├── detect_video_type.py    # Video analysis (MediaPipe)
│   ├── transcribe.py           # Speech-to-text (Whisper)
│   ├── translate.py            # Translation (Google Translate)
│   ├── captions.py             # Caption generation
│   ├── audio_mix.py            # Audio processing
│   └── video_process.py        # Video composition
│
├── assets/                     # Media files
│   ├── tiba_logo.png          # Academy logo (add your own)
│   ├── background_music.mp3   # Theme music (add your own)
│   └── README.md              # Asset instructions
│
└── output/                     # Generated files (auto-created)
```

## Adding Your Assets

### Step 1: Add Logo
```bash
# On your Mac
cp ~/Downloads/tiba_logo.png tiba-sports-editor/assets/

# Push to git
git add assets/tiba_logo.png
git commit -m "Add Tiba Academy logo"
git push
```

### Step 2: Add Background Music
```bash
# Rename your music to background_music.mp3
cp ~/Downloads/Impact_DNA.mp3 tiba-sports-editor/assets/background_music.mp3

# Push to git
git add assets/background_music.mp3
git commit -m "Add Tiba Academy theme music"
git push
```

## Troubleshooting

### FFmpeg Not Found
```bash
# macOS
brew install ffmpeg

# Ubuntu/Linux
sudo apt-get install ffmpeg

# Verify installation
ffmpeg -version
```

### Whisper Transcription Issues
- Ensure audio is clear in video
- Try with shorter video first to debug
- Whisper models download on first use (~2.7GB for base model)

### Google Translate API Errors
- Verify `GOOGLE_APPLICATION_CREDENTIALS` environment variable is set
- Check Google Cloud Console has Translate API enabled
- Ensure credentials JSON file is valid

### Memory Issues
- Process shorter videos first
- Increase system RAM
- Use `export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512` for CUDA

### Slow Processing
- Video type detection can take 10-15 seconds
- Transcription is the longest step (30-60 sec per minute)
- GPU acceleration (CUDA) speeds up Whisper 2-3x

## Advanced Usage

### Batch Processing
```bash
for video in videos/*.mp4; do
    python3 tiba_editor.py "$video"
done
```

### Custom Configuration File
Create `config.yaml`:
```yaml
whisper:
  model: base        # tiny, base, small, medium, large
  language: ar

google_translate:
  enabled: true
  credentials: /path/to/creds.json

audio:
  target_loudness: -14
  duck_level: -15

captions:
  style: bilingual
  font_size: 32
```

Use with:
```bash
python3 tiba_editor.py video.mp4 --config config.yaml
```

## Performance Benchmarks

Typical processing time per minute of video:
- Video Type Detection: 10-15 sec
- Transcription (Whisper): 30-60 sec
- Translation: 5-10 sec
- Audio Processing: 15-20 sec
- Video Composition: 30-60 sec
- **Total: ~2-4 minutes per 1 minute video**

With GPU (CUDA): ~1-2 minutes per minute

## Module API Reference

### VideoTypeDetector
```python
detector = VideoTypeDetector()
type = detector.detect("video.mp4")  # Returns "speaker" or "sports"
```

### Transcriber
```python
transcriber = Transcriber(model_name="base")
text = transcriber.transcribe("video.mp4", language="ar")
```

### Translator
```python
translator = Translator()
en_text = translator.translate(ar_text, source_lang="ar", target_lang="en")
```

### CaptionGenerator
```python
gen = CaptionGenerator()
gen.generate(transcript, translation, "video.mp4", "output/", style="bilingual")
```

### AudioMixer
```python
mixer = AudioMixer()
mixer.process("video.mp4", transcript, "output/")
```

### VideoProcessor
```python
proc = VideoProcessor()
proc.process("video.mp4", "audio.wav", "captions.srt", "output.mp4")
```

## Development & Contributing

### Running Tests
```bash
# Test with sample video
python3 tiba_editor.py samples/test_video.mp4

# Check output
ls -lh output/
file output/*.mp4
```

### Code Structure
- Modular design: each feature in separate module
- Consistent error handling with informative messages
- Bilingual comments (Arabic + English)
- Type hints for IDE support

## Brand Colors

- **Primary Navy**: #1A3A52
- **Accent Orange**: #FF6B35
- **Text White**: #FFFFFF
- **Text Dark**: #000000

## License & Credits

© 2024 Tiba Sports Academy
Built with Python, FFmpeg, Whisper, and Google Cloud APIs

## Support

For issues or questions:
1. Check README.md for detailed documentation
2. Review error messages carefully
3. Verify all dependencies are installed
4. Test with sample video first

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Maintained by**: Tiba Sports Academy
