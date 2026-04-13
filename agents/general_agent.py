from agents.base_agent import BaseAgent
from utils.logger import log
from knowledge.retriever import KnowledgeRetriever

class GeneralAgent(BaseAgent):

    def __init__(self, language_assist):
        super().__init__(language_assist)
        self.retriever = KnowledgeRetriever()

    def run(self, prompt, mode):

        log("GeneralAgent retrieving memory")

        # 🔹 Retrieve relevant memory
        memory_docs = []

        memory_text = "\n".join(memory_docs) if memory_docs else ""

        # 🔹 Build augmented prompt
        final_prompt = f"""
        
            You are Vylencia.

            You MUST follow this rule:
            - If memory is clearly relevant → USE it.
            - If memory is NOT relevant → IGNORE it completely.
            - Do NOT mention memory to user.
            - Never say "I don't have memory" or any similar things.
            - Respond naturally and helpfully.

            Memory:
            {memory_text}

            User Input:
            {prompt}

            Respond naturally in 1-2 sentences using the memory if possible.
        """

        return self.lang.compose(final_prompt, mode)