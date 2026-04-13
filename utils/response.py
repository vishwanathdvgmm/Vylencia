# utils/response.py

def format_response(mode: str, message: str) -> str:
    message = (message or "").strip()

    if not message:
        return ""

    prefixes = {
        "COMFORT": "I'm here with you.",
        "COMFORT_GUIDANCE": "I understand. Let's take this step by step.",
        "GUIDANCE": "Alright. Let's look at this calmly.",
        "GUARDIAN": "I've stepped in for your safety."
    }

    prefix = prefixes.get(mode, "")

    if not prefix:
        return message

    if message.lower().startswith(prefix.lower()):
        return message

    return f"{prefix} {message}".strip()
