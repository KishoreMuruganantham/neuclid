"""OCR tool using Gemini Vision as primary, EasyOCR as fallback."""

import base64
from google import genai
from config import GOOGLE_API_KEY, GEMINI_VISION_MODEL


def extract_text_from_image(image_bytes: bytes, filename: str = "image.png") -> dict:
    """Extract math text from an image using Gemini Vision.

    Returns dict with keys: text, confidence, method
    """
    try:
        client = genai.Client(api_key=GOOGLE_API_KEY)
        ext = filename.rsplit(".", 1)[-1].lower()
        mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
                "gif": "image/gif", "webp": "image/webp"}.get(ext, "image/png")

        response = client.models.generate_content(
            model=GEMINI_VISION_MODEL,
            contents=[
                genai.types.Part.from_bytes(data=image_bytes, mime_type=mime),
                (
                    "Extract ALL mathematical text from this image exactly as written. "
                    "Preserve mathematical notation using standard symbols (^, sqrt, /, etc). "
                    "If there are multiple problems, number them. "
                    "Output ONLY the extracted math text, nothing else. "
                    "If you cannot read parts clearly, mark them as [unclear]."
                ),
            ],
        )
        text = response.text.strip()
        has_unclear = "[unclear]" in text.lower()
        confidence = 0.6 if has_unclear else 0.92
        return {"text": text, "confidence": confidence, "method": "gemini-vision"}

    except Exception as e:
        try:
            import easyocr
            reader = easyocr.Reader(["en"], gpu=False)
            import tempfile, os
            with tempfile.NamedTemporaryFile(suffix=f".{ext}", delete=False) as f:
                f.write(image_bytes)
                tmp_path = f.name
            results = reader.readtext(tmp_path)
            os.unlink(tmp_path)
            text = " ".join([r[1] for r in results])
            avg_conf = sum(r[2] for r in results) / len(results) if results else 0
            return {"text": text, "confidence": round(avg_conf, 2), "method": "easyocr"}
        except Exception as e2:
            return {"text": "", "confidence": 0.0, "method": f"failed: {e}; {e2}"}
