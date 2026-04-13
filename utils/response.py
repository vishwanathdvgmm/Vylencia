# utils/response.py

def format_response(mode: str, message: str) -> str:
    message = (message or "").strip()
    prefix = ""

    if mode == "COMFORT":
        prefix = "I’m here with you. "
    elif mode == "COMFORT_GUIDANCE":
        prefix = "I understand. Let’s take this step by step. "
    elif mode == "GUIDANCE":
        prefix = "Alright. Let’s look at this calmly. "
    elif mode == "GUARDIAN":
        prefix = "I’ve stepped in for your safety. "
    else:
        prefix = ""

    if prefix and message.lower().startswith(prefix.lower()):
        return message

    return f"{prefix}{message}"
