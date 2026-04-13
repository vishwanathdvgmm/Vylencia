from agents.base_agent import BaseAgent
from utils.logger import log

class MedicalAgent(BaseAgent):

    def run(self, prompt, mode):
        log("MedicalAgent handling request")

        return self.lang.compose(prompt, mode)