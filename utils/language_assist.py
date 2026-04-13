# utils/language_assist.py

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
            return out if isinstance(out, str) and out.strip() else draft
        except Exception:
            return draft
