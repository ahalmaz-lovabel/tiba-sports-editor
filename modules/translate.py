"""
Translation Module - Arabic to English
وحدة الترجمة - من العربية إلى الإنجليزية

Uses Google Cloud Translation API for accurate bilingual content.
"""

from google.cloud import translate_v2
import os
from typing import Optional


class Translator:
    """Translate text using Google Cloud Translation"""

    def __init__(self, project_id: Optional[str] = None):
        """
        Initialize translator

        Args:
            project_id: Google Cloud project ID (optional)
        """
        # Initialize Google Cloud client
        # Credentials should be set via GOOGLE_APPLICATION_CREDENTIALS env var
        self.client = translate_v2.Client(project_id=project_id)
        self.source_language = "ar"
        self.target_language = "en"

    def translate(
        self,
        text: str,
        source_lang: str = "ar",
        target_lang: str = "en"
    ) -> str:
        """
        Translate text from source to target language

        Args:
            text: Text to translate
            source_lang: Source language code (default: "ar")
            target_lang: Target language code (default: "en")

        Returns:
            Translated text
        """
        if not text or not text.strip():
            return ""

        try:
            result = self.client.translate_text(
                text,
                source_language=source_lang,
                target_language=target_lang
            )

            translated_text = result.get("translatedText", text)
            return translated_text

        except Exception as e:
            print(f"   ⚠️  Translation error: {e}")
            print(f"   Using original text (fallback)")
            return text

    def translate_segments(
        self,
        segments: list,
        source_lang: str = "ar",
        target_lang: str = "en"
    ) -> list:
        """
        Translate multiple text segments (with timestamps)

        Args:
            segments: List of dicts with "text", "start", "end"
            source_lang: Source language code
            target_lang: Target language code

        Returns:
            Segments with added "translation" field
        """
        translated = []

        for segment in segments:
            translated_segment = segment.copy()
            translated_segment["translation"] = self.translate(
                segment.get("text", ""),
                source_lang,
                target_lang
            )
            translated.append(translated_segment)

        return translated

    def batch_translate(
        self,
        texts: list,
        source_lang: str = "ar",
        target_lang: str = "en"
    ) -> list:
        """
        Translate multiple texts efficiently

        Args:
            texts: List of strings to translate
            source_lang: Source language code
            target_lang: Target language code

        Returns:
            List of translated strings
        """
        if not texts:
            return []

        # Filter out empty strings
        non_empty = [t for t in texts if t and t.strip()]

        if not non_empty:
            return [""] * len(texts)

        try:
            results = self.client.translate_text(
                non_empty,
                source_language=source_lang,
                target_language=target_lang
            )

            translations = [r.get("translatedText", t) for r, t in zip(results, non_empty)]

            # Map back to original list with empty strings
            final_translations = []
            translation_idx = 0

            for text in texts:
                if text and text.strip():
                    final_translations.append(translations[translation_idx])
                    translation_idx += 1
                else:
                    final_translations.append("")

            return final_translations

        except Exception as e:
            print(f"   ⚠️  Batch translation error: {e}")
            return texts

    def is_configured(self) -> bool:
        """Check if Google credentials are properly configured"""
        try:
            # Try a simple translation to verify configuration
            self.client.translate_text("تجربة", source_language="ar", target_language="en")
            return True
        except Exception:
            return False
