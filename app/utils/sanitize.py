import re

def sanitize_input(text: str) -> str:
    """Basic sanitization to avoid prompt injection and weird characters."""
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r"[^\S\r\n]+", " ", text)  # normalize spaces
    return text