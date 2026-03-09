"""ASR tool for converting speech to text with math-awareness."""

import io
import speech_recognition as sr


MATH_REPLACEMENTS = {
    "square root of": "sqrt(",
    "squared": "^2",
    "cubed": "^3",
    "raised to the power of": "^",
    "raised to": "^",
    "to the power": "^",
    "divided by": "/",
    "multiplied by": "*",
    "times": "*",
    "plus": "+",
    "minus": "-",
    "equals": "=",
    "is equal to": "=",
    "greater than or equal to": ">=",
    "less than or equal to": "<=",
    "greater than": ">",
    "less than": "<",
    "pi": "pi",
    "theta": "theta",
    "alpha": "alpha",
    "beta": "beta",
    "infinity": "inf",
    "integral of": "integral(",
    "derivative of": "d/dx(",
    "limit of": "lim(",
    "approaches": "->",
    "log base": "log_",
    "natural log": "ln",
    "factorial": "!",
    "x squared": "x^2",
    "x cubed": "x^3",
    "sine": "sin",
    "cosine": "cos",
    "tangent": "tan",
}


def transcribe_audio(audio_bytes: bytes, sample_rate: int = 44100) -> dict:
    """Transcribe audio bytes to math-aware text.

    Returns dict with keys: text, raw_text, confidence, needs_confirmation
    """
    recognizer = sr.Recognizer()
    try:
        audio_data = sr.AudioData(audio_bytes, sample_rate, 2)
        raw_text = recognizer.recognize_google(audio_data)
        math_text = _apply_math_replacements(raw_text)
        confidence = 0.85
        needs_confirmation = confidence < 0.8 or any(
            word in raw_text.lower() for word in ["unclear", "um", "uh"]
        )
        return {
            "text": math_text,
            "raw_text": raw_text,
            "confidence": confidence,
            "needs_confirmation": needs_confirmation,
        }
    except sr.UnknownValueError:
        return {
            "text": "",
            "raw_text": "",
            "confidence": 0.0,
            "needs_confirmation": True,
        }
    except sr.RequestError as e:
        return {
            "text": "",
            "raw_text": "",
            "confidence": 0.0,
            "needs_confirmation": True,
        }


def transcribe_audio_file(file_bytes: bytes, file_format: str = "wav") -> dict:
    """Transcribe an uploaded audio file."""
    recognizer = sr.Recognizer()
    try:
        audio_io = io.BytesIO(file_bytes)
        with sr.AudioFile(audio_io) as source:
            audio_data = recognizer.record(source)
        raw_text = recognizer.recognize_google(audio_data)
        math_text = _apply_math_replacements(raw_text)
        return {
            "text": math_text,
            "raw_text": raw_text,
            "confidence": 0.85,
            "needs_confirmation": False,
        }
    except Exception as e:
        return {
            "text": "",
            "raw_text": "",
            "confidence": 0.0,
            "needs_confirmation": True,
        }


def _apply_math_replacements(text: str) -> str:
    """Apply math-specific phrase replacements."""
    result = text.lower()
    for phrase, replacement in sorted(MATH_REPLACEMENTS.items(), key=lambda x: -len(x[0])):
        result = result.replace(phrase, replacement)
    return result
