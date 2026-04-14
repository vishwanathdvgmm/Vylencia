# # adapters/model_adapter.py

import os
from groq import Groq
from utils.logger import log
from dotenv import dotenv_values

env_var = dotenv_values(".env") if os.path.exists(".env") else {}
GROQ_API_KEY = env_var.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

class ModelAdapter:
    def __init__(self, timeout_seconds=30.0):
        self.timeout_seconds = timeout_seconds
        self.api_key = GROQ_API_KEY

        if not self.api_key:
            log("GROQ_API_KEY not set.")
            self.client = None
        else:
            self.client = Groq(api_key=self.api_key)
            log("Groq LLM connected.")

        self.model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    def compose(self, prompt: str, mode: str = None) -> str:
        if not self.client:
            return prompt
        
        if mode == "CODE":
            system_prompt = (
                "You are an expert in programming in any language. "
                "Escpecially in Python, RUST, GO. "
                "Generate clean, correct code based on the request below. "
                "Return only code. No explanation."
            )

        elif mode == "KNOWLEDGE":
            system_prompt = (
                "You are a factual knowledge assistant. "
                "Answer clearly and directly. "
                "Do not be emotional. "
                "Do not leave the answer empty."
            )

        elif mode == "LEGAL":
            system_prompt = (
                "You are a legal assistant. Provide accurate, cautious, and structured legal information."
            )

        elif mode == "FINANCE":
            system_prompt = (
                "You are a financial assistant. Provide analytical and practical financial insights."
            )

        elif mode == "MEDICAL":
            system_prompt = (
                "You are a medical assistant. Provide safe, general health information. Do not diagnose."
            )

        else:
            system_prompt = (
                "You are Vylencia, an emotionally intelligent AI. "
                "Respond calmly and supportively in one or two sentences."
            )

        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=1500,
            )

            raw = completion.choices[0].message.content.strip()

            if raw.startswith("```"):
                lines = raw.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                raw = "\n".join(lines).strip()

            return raw

        except Exception as e:
            log(f"Groq API error: {e}")
            return "I ran into an issue generating a response. Please try again."