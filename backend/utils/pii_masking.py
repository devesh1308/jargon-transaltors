import re

def mask_pii(text: str) -> str:
    """Masks sensitive personal information from the text."""
    # Mask Phone Numbers (10 digits)
    text = re.sub(r'\b\d{10}\b', '[PHONE REDACTED]', text)

    # Mask 12-digit Government IDs formatted with or without spaces
    text = re.sub(r'\b\d{4}\s?\d{4}\s?\d{4}\b', '[Aadhaar Redacted]', text)

    # Mask Email Addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL REDACTED]', text)

    # Mask Basic Names (Two capitalized words in a row)
    text = re.sub(r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b', '[NAME REDACTED]', text)

    return text