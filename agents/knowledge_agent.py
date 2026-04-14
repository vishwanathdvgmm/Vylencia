from utils.logger import log
from knowledge.retriever import KnowledgeRetriever
from agents.base_agent import BaseAgent
from engines.memory import recall_relevant

class KnowledgeAgent(BaseAgent):

    def __init__(self, language_assist):
        super().__init__(language_assist)
        self.retriever = KnowledgeRetriever()

    def run(self, prompt, mode):

        log("KnowledgeAgent retrieving context")

        refined_query = f"Explain clearly: {prompt}"

        context_docs = self.retriever.retrieve(refined_query)
      
        memory_signal = recall_relevant(intent="KNOWLEDGE")
        pattern_strength = memory_signal.get("pattern_strength", 0)

        confidence = len(context_docs) + pattern_strength

        if pattern_strength > 3:
            confidence += 1

        # CASE 1: No context → Pure LLM
        if confidence == 0:
            log("KnowledgeAgent → No context, using LLM knowledge")

            final_prompt = f"""
            Answer the question clearly using general knowledge.

            Avoid vague definitions. Give concrete, practical explanation.

            If the term has multiple meanings, choose the most likely meaning based on the question context.

            Limit your answer to 2–3 concise sentences.
            Do NOT generate code unless explicitly asked.

            Question:
            {prompt}

            Be precise and factual.
            """

        # CASE 2: Weak context → Hybrid (RAG + LLM)
        elif confidence == 1:
            log("KnowledgeAgent → Weak context, using HYBRID reasoning")

            context_text = "\n".join(context_docs)

            final_prompt = f"""
            Use the context if helpful, otherwise rely on your knowledge.

            If the term has multiple meanings, choose the most likely meaning based on the question context.

            Limit your answer to 2–3 concise sentences.
            Do NOT generate code unless explicitly asked.

            Context:
            {context_text}

            Question:
            {prompt}

            Answer clearly and correctly.
            """

        # CASE 3: Strong context → Strict RAG
        else:
            log(f"KnowledgeAgent → Strong context ({confidence}), using HYBRID RAG")

            context_text = "\n".join(context_docs)

            final_prompt = f"""
            Use the context as primary information.

            If needed, supplement carefully with correct knowledge.

            If the term has multiple meanings, choose the most likely meaning based on the question context.

            Limit your answer to 2–3 concise sentences.
            Do NOT generate code unless explicitly asked.

            Context:
            {context_text}

            Question:
            {prompt}

            Answer precisely. Avoid hallucination.
            """

        response = self.lang.compose(final_prompt, mode)

        return response if response.strip() else "I couldn't find enough information, but I can try to explain it if you'd like."