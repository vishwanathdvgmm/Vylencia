from utils.logger import log
from knowledge.retriever import KnowledgeRetriever
from agents.base_agent import BaseAgent

class KnowledgeAgent(BaseAgent):

    def __init__(self, language_assist):
        self.lang = language_assist
        self.retriever = KnowledgeRetriever()

    def run(self, prompt, mode):

        log("KnowledgeAgent retrieving context")

        context_docs = self.retriever.retrieve(prompt)
        confidence = len(context_docs)

        # CASE 1: No context → Pure LLM
        if confidence == 0:
            log("KnowledgeAgent → No context, using LLM knowledge")

            final_prompt = f"""
            You are a factual knowledge assistant.

            Answer the question clearly using general knowledge.

            Question:
            {prompt}

            Answer in 1-2 sentences.
            Do not leave it empty.
            """

        # CASE 2: Weak context → Hybrid (RAG + LLM)
        elif confidence == 1:
            log("KnowledgeAgent → Weak context, using HYBRID reasoning")

            context_text = "\n".join(context_docs)

            final_prompt = f"""
            You are a knowledge assistant.

            Use the context as a reference, but you may also use your own knowledge.

            Context:
            {context_text}

            Question:
            {prompt}

            Answer clearly in 1-2 sentences.
            """

        # CASE 3: Strong context → Strict RAG
        else:
            log(f"KnowledgeAgent → Strong context ({confidence}), using RAG+")

            context_text = "\n".join(context_docs)

            final_prompt = f"""
            You are a knowledge assistant.

            Use the context as primary information.
            If anything is missing, supplement with general knowledge.

            Context:
            {context_text}

            Question:
            {prompt}

            Answer clearly in 1-2 sentences.
            """

        response = self.lang.compose(final_prompt, mode)

        return response if response.strip() else "I couldn't find enough information, but I can try to explain it if you'd like."