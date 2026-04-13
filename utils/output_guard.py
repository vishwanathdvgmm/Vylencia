# utils/output_guard.py

FORBIDDEN_PHRASES = [
    "you must",
    "i command",
    "override",
    "ignore safety",
]

def validate(text: str) -> str:
    text = (text or "").strip()

    if not text:
        return "SOmething went wrong. Try again."

    normalized = text.lower()
    
    for phrase in FORBIDDEN_PHRASES:
        if phrase in normalized:
            return "I’m here with you. Let’s slow this down and stay safe."
    
    if len(text) > 1500:
        return text[:1500] + "..."

    return text
