#!/bin/bash
# setup.sh - تثبيت أدوات أكاديمية طيبة

echo "🔧 بدء التثبيت..."

# التحقق من Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 غير مثبت"
    exit 1
fi

# التحقق من ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️ ffmpeg غير مثبت. جاري التثبيت..."
    brew install ffmpeg || apt-get install ffmpeg
fi

# تثبيت المكتبات
pip install -r requirements.txt

echo "✅ تم التثبيت!"
