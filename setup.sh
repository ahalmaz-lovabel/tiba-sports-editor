#!/bin/bash
# Tiba Sports Academy Editor - Setup Script
# محرّر أكاديمية طيبة - سكريبت التثبيت

set -e

echo "🔧 بدء التثبيت... (Starting setup...)"
echo "================================"

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 غير مثبت (Python 3 is not installed)"
    exit 1
fi
echo "✅ Python 3 موجود"

# Check FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg غير مثبت (FFmpeg is not installed)"
    echo "جاري المحاولة... (Attempting to install...)"

    if command -v brew &> /dev/null; then
        brew install ffmpeg
    elif command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y ffmpeg
    else
        echo "❌ لا يمكن تثبيت FFmpeg تلقائياً (Cannot install FFmpeg automatically)"
        echo "الرجاء التثبيت يدويًا (Please install FFmpeg manually)"
        exit 1
    fi
fi
echo "✅ FFmpeg موجود"

# Install Python dependencies
echo ""
echo "📦 تثبيت المكتبات... (Installing dependencies...)"
pip install -r requirements.txt

echo ""
echo "✅ التثبيت اكتمل بنجاح! (Setup completed successfully!)"
echo "================================"
echo "الاستخدام: (Usage:)"
echo "  python3 tiba_editor.py <video_file>"
echo ""
