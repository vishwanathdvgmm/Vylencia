# engines/router.py

from utils.logger import log

class CapabilityRouter:
    def __init__(self):
        self.routes = {
            "GENERAL": "general_agent",
            "ENTERTAINMENT": "general_agent",
            "GUIDANCE": "general_agent",
            "COMFORT": "general_agent",
            "CODE": "code_agent",
            "LEGAL": "legal_agent",
            "FINANCE": "finance_agent",
            "MEDICAL": "medical_agent",
            "KNOWLEDGE": "knowledge_agent"
        }

    def route(self, decision_mode: str, user_input: str = ""):

        text = user_input.lower()

        # HARD LOCK for critical modes
        if decision_mode in ["KNOWLEDGE", "CODE", "LEGAL", "FINANCE", "MEDICAL"]:
            agent = self.routes.get(decision_mode, "general_agent")
            log(f"Router selected agent={agent}")
            return agent

        # SOFT routing only for GENERAL modes
        if decision_mode in ["COMFORT", "GUIDANCE", "ENTERTAINMENT"]:

            if any(word in text for word in ["code", "program", "function", "debug", "error"]):
                agent = "code_agent"

            elif any(word in text for word in ["law", "legal", "contract", "court"]):
                agent = "legal_agent"

            elif any(word in text for word in ["money", "finance", "invest", "stock"]):
                agent = "finance_agent"

            elif any(word in text for word in ["health", "medical", "symptom", "doctor"]):
                agent = "medical_agent"

            else:
                agent = "general_agent"

            log(f"Router selected agent={agent}")
            return agent

        return "general_agent"