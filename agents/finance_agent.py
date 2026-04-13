from agents.base_agent import BaseAgent
from utils.logger import log

class FinanceAgent(BaseAgent):

    def run(self, prompt, mode):
        log("FinanceAgent handling request")

        return self.lang.compose(prompt, mode)