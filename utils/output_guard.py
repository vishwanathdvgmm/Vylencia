# utils/output_guard.py

FORBIDDEN_PHRASES = [
    "you must",
    "i command",
    "override",
    "ignore safety",
]

def validate(text: str) -> str:
    text = (text or "").strip()
    lowered = text.lower()
    for phrase in FORBIDDEN_PHRASES:
        if phrase in lowered:
            return "I’m here with you. Let’s slow this down and stay safe."
    return text
