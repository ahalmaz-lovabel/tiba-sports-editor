# Assets Directory
# مجلد الأصول

This directory contains static media files for the Tiba Sports Academy video editor.

## Required Files | الملفات المطلوبة

### 1. `tiba_logo.png`
- **Description**: Tiba Academy logo
- **Format**: PNG with transparency
- **Recommended Size**: 400x400 pixels minimum
- **Purpose**: Overlaid on video corners
- **Note**: Add your academy logo image here

### 2. `background_music.mp3`
- **Description**: Default background/theme music
- **Format**: MP3
- **Recommended Length**: 30-60 seconds (loops if needed)
- **Purpose**: Background music that gets ducked during speech
- **Note**: Add your academy's theme music here

## How to Add Files

1. **On Mac** (your local machine):
   ```bash
   cd ~/Desktop/tiba-sports-editor
   
   # Copy logo
   cp ~/Downloads/tiba_logo.png assets/
   
   # Copy music
   cp ~/Downloads/background_music.mp3 assets/
   # or rename if your file has different name:
   cp ~/Downloads/your_music.mp3 assets/background_music.mp3
   ```

2. **Commit and Push**:
   ```bash
   git add assets/
   git commit -m "Add Tiba Academy brand assets"
   git push
   ```

## File Specifications

### Logo Requirements
- Transparent PNG recommended
- Minimum 400x400px
- Aspect ratio: preferably square
- Colors: Use academy colors or high contrast

### Music Requirements
- MP3 format (or WAV, FLAC)
- 44.1 kHz sample rate
- Stereo or Mono
- ~30-60 seconds recommended
- Make sure music can be "ducked" (reduced) during speech

## Notes
- These files are listed in `.gitignore` for large binary file management
- In production, consider using Git LFS (Large File Storage) for large media files
- Backup your media files separately
