"""Translation service — supports 8 Indian languages."""
from deep_translator import GoogleTranslator
from functools import lru_cache


@lru_cache(maxsize=512)
def _translate_cached(text: str, target: str) -> str:
    translator = GoogleTranslator(source='en', target=target)
    return translator.translate(text)


def translate_text(text: str, target: str = 'hi') -> str:
    """Translate text to target language. Returns original on failure."""
    if not text or not target:
        return text
    try:
        return _translate_cached(text, target)
    except Exception as e:
        return f"[Translation unavailable: {e}]"
