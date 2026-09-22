# Tiba Sports Academy Video Editor
# محرّر أكاديمية طيبة الرياضية للفيديوهات

A specialized, intelligent video processing tool built for **Tiba Sports Academy** with advanced features for professional video content creation.

أداة معالجة فيديو متخصصة وذكية مصممة لـ **أكاديمية طيبة الرياضية** مع ميزات متقدمة لإنتاج محتوى فيديو احترافي.

---

## Features ✨ | الميزات

### 1. **Intelligent Video Type Detection** 🔍
- Automatically detects video content type:
  - **Speaker/Presenter**: Person speaking directly to camera
  - **Sports Action**: Movement and athletic activities
- Uses MediaPipe for accurate detection
- كشف ذكي لنوع محتوى الفيديو

### 2. **Arabic-English Captions** 📝
- Automatic speech-to-text transcription using OpenAI Whisper
- Live automatic translation (Arabic ↔ English)
- Dual-language captions (side-by-side or stacked)
- Professional caption styling with Academy branding colors
- كابشنات ثنائية اللغة مع ترجمة تلقائية

### 3. **Professional Audio Processing** 🔊
- Audio normalization to -14 LUFS (broadcast standard)
- Automatic music ducking during speech (background music lowers automatically)
- Background music volume control
- معايرة احترافية للصوت مع خفض تلقائي للموسيقى

### 4. **Academy Branding** 🎨
- Fixed logo overlay in corner (customizable position)
- Academy color scheme:
  - Navy Blue: #1A3A52
  - Orange: #FF6B35
- Professional watermark application
- شعار الأكاديمية مع الألوان الرسمية

### 5. **Batch Processing** ⚡
- Process multiple videos with one command
- Parallel processing support
- Progress tracking
- معالجة دفعات من الفيديوهات

---

## Requirements 📋 | المتطلبات

### System Requirements
- **Python**: 3.8 or higher
- **FFmpeg**: Latest version
- **OS**: macOS, Linux, or Windows
- **RAM**: 4GB minimum (8GB recommended)
- **GPU**: Optional (CUDA for faster processing)

### Python Dependencies
See `requirements.txt` for complete list:
- `openai-whisper` - Speech-to-text
- `google-cloud-translate` - Arabic-English translation
- `opencv-python` - Video processing
- `mediapipe` - Video type detection
- `librosa` - Audio analysis
- `pydub` - Audio manipulation
- `Pillow` - Image processing
- And more...

---

## Installation 🚀 | التثبيت

### Quick Start (Recommended)

```bash
# 1. Clone or navigate to project directory
cd tiba-sports-editor

# 2. Run setup script
chmod +x setup.sh
./setup.sh

# 3. Done! Ready to use
```

### Manual Installation

```bash
# 1. Install FFmpeg (if not already installed)
# macOS:
brew install ffmpeg

# Linux:
sudo apt-get install ffmpeg

# Windows:
choco install ffmpeg
```

```bash
# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Verify installation
python3 tiba_editor.py --help
```

### Google Translate API Setup

For translation features to work:

```bash
# Set Google credentials
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
```

Get credentials from: https://console.cloud.google.com/

---

## Usage 🎬 | الاستخدام

### Basic Usage

```bash
# Process a single video
python3 tiba_editor.py video.mp4

# Specify output file name
python3 tiba_editor.py video.mp4 -o "my_output.mp4"

# Specify output directory
python3 tiba_editor.py video.mp4 --output-dir "./processed"
```

### Advanced Options

```bash
# Help menu
python3 tiba_editor.py --help

# Custom output
python3 tiba_editor.py input.mp4 -o output.mp4 --output-dir /path/to/output
```

### Processing Pipeline

The tool automatically runs these steps:

1. **Video Type Detection** - Identifies content type
2. **Audio Transcription** - Converts speech to Arabic text (Whisper)
3. **Translation** - Translates to English (Google Translate)
4. **Caption Generation** - Creates styled bilingual captions
5. **Audio Processing** - Normalizes and ducks music
6. **Video Composition** - Adds logo, captions, and audio
7. **Output** - Saves final video

---

## Project Structure 📁

```
tiba-sports-editor/
├── tiba_editor.py           # Main program
├── setup.sh                 # Installation script
├── requirements.txt         # Python dependencies
├── README.md               # This file
│
├── modules/                # Python modules
│   ├── __init__.py
│   ├── detect_video_type.py    # Video type detection
│   ├── transcribe.py           # Speech-to-text (Whisper)
│   ├── translate.py            # Translation (Google)
│   ├── captions.py             # Caption generation
│   ├── audio_mix.py            # Audio processing
│   └── video_process.py        # Video composition
│
├── assets/                 # Static assets
│   ├── tiba_logo.png      # Academy logo
│   ├── background_music.mp3   # Default background music
│   └── README.md          # Asset instructions
│
└── output/                # Processed videos (created automatically)
```

---

## Configuration ⚙️ | الإعدادات

### Color Scheme
```yaml
colors:
  primary: "#1A3A52"      # Navy Blue
  accent: "#FF6B35"       # Orange
  text_light: "#FFFFFF"   # White
  text_dark: "#000000"    # Black
```

### Audio Settings
```yaml
audio:
  target_loudness: -14    # LUFS (Loudness Units)
  music_duck_level: -15   # dB reduction during speech
  music_duck_speed: 0.3   # Fade speed (0-1)
```

### Caption Settings
```yaml
captions:
  font_size: 32
  background_opacity: 0.8
  position: "bottom"      # top, middle, bottom
  style: "bilingual"      # bilingual, arabic_only, english_only
```

---

## Troubleshooting 🔧

### FFmpeg not found
```bash
# Install FFmpeg
# macOS: brew install ffmpeg
# Linux: sudo apt-get install ffmpeg
# Windows: choco install ffmpeg
```

### Google Translate API error
- Verify credentials file exists and is valid
- Check API is enabled in Google Cloud Console
- Ensure project has Translate API enabled

### Audio processing issues
- Verify input video has valid audio track
- Check audio format compatibility with FFmpeg
- Try with sample video first

### Memory issues with large videos
- Process in smaller chunks (if supported)
- Reduce video resolution before processing
- Increase system RAM or add swap

---

## Advanced Usage 🚀

### Processing Multiple Videos

```bash
# Process all videos in a folder
for file in videos/*.mp4; do
    python3 tiba_editor.py "$file" --output-dir processed/
done
```

### Custom Configuration

Create `config.yaml`:
```yaml
video_type_detection:
  confidence_threshold: 0.7

audio:
  target_loudness: -14
  music_duck_level: -15

captions:
  language_primary: ar
  language_secondary: en
  font_size: 32
```

Then use:
```bash
python3 tiba_editor.py video.mp4 --config config.yaml
```

---

## Performance 📊

### Typical Processing Times (per minute of video)
- **Video Type Detection**: 10-15 seconds
- **Transcription (Whisper)**: 30-60 seconds
- **Translation**: 5-10 seconds
- **Caption Generation**: 10-15 seconds
- **Audio Processing**: 15-20 seconds
- **Video Composition**: 30-60 seconds

**Total**: ~2-4 minutes per minute of video (CPU dependent)

With GPU acceleration (CUDA): ~1-2 minutes per minute of video

---

## Development 👨‍💻

### Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and test thoroughly
3. Commit with clear messages
4. Push and create pull request

### Testing

```bash
# Run with sample video
python3 tiba_editor.py samples/test_video.mp4

# Check output
ls -lh output/
```

---

## API Reference 📚

### VideoTypeDetector
```python
from modules.detect_video_type import VideoTypeDetector

detector = VideoTypeDetector()
video_type = detector.detect("video.mp4")
# Returns: "speaker" or "sports"
```

### Transcriber
```python
from modules.transcribe import Transcriber

transcriber = Transcriber()
text = transcriber.transcribe("video.mp4")
# Returns: Arabic text transcript
```

### Translator
```python
from modules.translate import Translator

translator = Translator()
english_text = translator.translate(arabic_text, "ar", "en")
# Returns: English translation
```

---

## License 📄

© 2024 Tiba Sports Academy
All rights reserved.

---

## Support 💬

For issues, questions, or feature requests:
- Email: support@tiba-academy.com
- Website: https://tiba-academy.com

---

## Version History 📖

### v1.0.0 (2024)
- Initial release
- Core features: transcription, translation, captions
- Audio normalization and music ducking
- Logo overlay and branding

---

**Built with ❤️ for Tiba Sports Academy** 🏆
