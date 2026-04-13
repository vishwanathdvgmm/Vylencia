from agents.base_agent import BaseAgent
from utils.logger import log

class LegalAgent(BaseAgent):

    def run(self, prompt, mode):
        log("LegalAgent handling request")

        return self.lang.compose(prompt, mode)