# utils/logger.py

from datetime import datetime

DEBUG = True

def log(message: str):
    if not DEBUG:
        return
    timestamp = datetime.now().isoformat(timespec="seconds")
    print(f"[{timestamp}] {message}")
