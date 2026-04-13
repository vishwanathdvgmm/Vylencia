from agents.base_agent import BaseAgent
from utils.logger import log

class CodeAgent(BaseAgent):

    def run(self, prompt: str, mode: str):
        log("CodeAgent handling request")

        return self.lang.compose(prompt, mode)