# utils/logger.py

from datetime import datetime

def log(message: str):
    timestamp = datetime.now().isoformat(timespec="seconds")
    print(f"[{timestamp}] {message}")
