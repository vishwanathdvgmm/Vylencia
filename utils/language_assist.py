# utils/language_assist.py
from utils.logger import log

class LanguageAssist:
    def __init__(self, adapter=None):
        self.adapter = adapter

    def interpret(self, text: str) -> str:
        return text

    def compose(self, draft: str, mode: str) -> str:
        if not self.adapter:
            return draft
        try:
            out = self.adapter.compose(draft, mode)

            if not isinstance(out, str) or not out.strip():
                log("LanguageAssist: Empty or invalid model output. Falling back.")
                return draft

            return out

        except Exception as e:
            log(f"LanguageAssist ERROR: {e}")
            return draft
