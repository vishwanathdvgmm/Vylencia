from utils.logger import log

class BaseAgent:
    def __init__(self, language_assist):
        self.lang = language_assist

    def run(self, prompt: str, mode: str):
        raise NotImplementedError
