# main.py

from core.state import VylenciaState
from core.clock import Clock

from utils.logger import log
from utils.response import format_response
from utils.language_assist import LanguageAssist
from utils.output_guard import validate
from utils.persistence import load_relationship, save_relationship

from adapters.model_adapter import ModelAdapter

from policies.personality import PersonalityPolicy

from engines.interaction import process_input
from engines.decision import decide
from engines.memory import update_memory
from engines.control import execute
from engines.governance import allow

from agents.general_agent import GeneralAgent
from agents.code_agent import CodeAgent
from agents.legal_agent import LegalAgent
from agents.finance_agent import FinanceAgent
from agents.medical_agent import MedicalAgent
from agents.knowledge_agent import KnowledgeAgent

DEBUG = True  # Set to False for normal operation

def print_title():
    """Print the VYLENCIA ASCII art title."""
    title = """

   ╔══════════════════════════════════════════════════════════════════════════╗
   ║                                                                          ║
   ║      ██╗   ██╗██╗   ██╗██╗     ███████╗███╗   ██╗ ██████╗██╗ █████╗      ║
   ║      ██║   ██║╚██╗ ██╔╝██║     ██╔════╝████╗  ██║██╔════╝██║██╔══██╗     ║
   ║      ██║   ██║ ╚████╔╝ ██║     █████╗  ██╔██╗ ██║██║     ██║███████║     ║
   ║      ╚██╗ ██╔╝  ╚██╔╝  ██║     ██╔══╝  ██║╚██╗██║██║     ██║██╔══██║     ║
   ║       ╚████╔╝    ██║   ███████╗███████╗██║ ╚████║╚██████╗██║██║  ██║     ║
   ║        ╚═══╝     ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═══╝ ╚═════╝╚═╝╚═╝  ╚═╝     ║
   ║                                                                          ║
   ║                Vylencia — An Intelligent Cognitive System                ║
   ║                                                                          ║
   ╚══════════════════════════════════════════════════════════════════════════╝
    """

    print(title)

def main():
    log("Vylencia is starting.")
    print_title()
    
    state = VylenciaState()
    rel_data = load_relationship()
    state.relationship.familiarity = rel_data["familiarity"]
    state.relationship.trust = rel_data["trust"]
    state.relationship.warmth = rel_data["warmth"]
    state.relationship.last_mode = rel_data["last_mode"]
    state.relationship.last_phrase = rel_data["last_phrase"]
    clock = Clock()
    personality = PersonalityPolicy()
    adapter = ModelAdapter(timeout_seconds=30.0)
    lang = LanguageAssist(adapter=adapter)
    general_agent = GeneralAgent(lang)
    code_agent = CodeAgent(lang)
    legal_agent = LegalAgent(lang)
    finance_agent = FinanceAgent(lang)
    medical_agent = MedicalAgent(lang)
    knowledge_agent = KnowledgeAgent(lang)

    agent_map = {
        "general_agent": general_agent,
        "code_agent": code_agent,
        "legal_agent": legal_agent,
        "finance_agent": finance_agent,
        "medical_agent": medical_agent,
        "knowledge_agent": knowledge_agent,
    }

    MODE_TO_AGENT = {
        "CODE": "code_agent",
        "LEGAL": "legal_agent",
        "FINANCE": "finance_agent",
        "MEDICAL": "medical_agent",
        "KNOWLEDGE": "knowledge_agent",

        # default behaviors
        "GENERAL": "general_agent",
        "COMFORT": "general_agent",
        "COMFORT_GUIDANCE": "general_agent",
        "GUIDANCE": "general_agent",
        "ENTERTAINMENT": "general_agent",
    }

    log("Vylencia is alive.")

    while state.alive:
        try:
            user_input = input("\nYou: ").strip()

            if user_input.lower() in ("shutdown vylencia", "emergency stop", "exit"):
                save_relationship(state.relationship)
                log("EMERGENCY SHUTDOWN triggered.")
                state.alive = False
                break

            previous_input = state.last_interaction.get("text")

            interpreted_input = lang.interpret(user_input)
            state.update_interaction(interpreted_input)
            processed = process_input(interpreted_input, state)

            if DEBUG:
                log(f"Detected emotion={processed['emotion']} intent={processed['intent']} urgent={processed['urgent']}")

            decision = decide(processed, state)
            state.mode = decision["mode"]

            if DEBUG:
                log(f"Decision mode={decision['mode']}")

            if allow(decision, state):
                execute(decision, state)

            agent_name = MODE_TO_AGENT.get(decision["mode"], "general_agent")

            if decision["mode"] == "UNKNOWN":
                agent_name = "general_agent"

            update_memory(processed, decision, state)
            save_relationship(state.relationship)
            if DEBUG:
                log("Memory and relationship state updated.")

            if decision["mode"] in ["CODE", "KNOWLEDGE", "GENERAL"]:
                personalized = ""
            else:
                personalized = personality.apply(decision, processed, state)

            if decision["mode"] == "GUARDIAN":
                formatted = format_response(decision["mode"], personalized)
                final_text = validate(formatted)

            elif decision["mode"] == "KNOWLEDGE":
                agent = agent_map.get(agent_name, knowledge_agent)
                generated = agent.run(processed["raw_input"], "KNOWLEDGE")
                final_text = validate(generated.strip()) if generated else "Something went wrong."

            elif decision["mode"] == "ENTERTAINMENT":
                structured_prompt = (
                    "emotion=CALM; intent=ENTERTAINMENT; urgency=LOW; "
                    "situation=User asked for a joke\n\n"
                )
                agent = agent_map.get(agent_name, general_agent)
                generated = agent.run(structured_prompt, "ENTERTAINMENT")
                final_text = validate(generated).strip() if generated and generated.strip() else \
                    "Hmm… I was thinking of a joke, but my brain took too long 😅 Want me to try again?"

            else:
                if decision["mode"] == "CODE":
                    previous_code = state.last_interaction.get("text", "")

                    followup_keywords = ["same", "above", "previous", "modify", "update"]
                    if_followup = any(k in processed["raw_input"].lower() for k in followup_keywords)

                    context_block = previous_input if if_followup else ""

                    structured_prompt = f"""
                    You are a senior software engineer.

                    Task/Current request:
                    {processed["raw_input"]}

                    Context (previous code, if relevant):
                    {context_block}

                    Write complete, correct, working code.
                    
                    Requiremens:
                    - Return ONLY code.
                    - Use the language Requested.
                    - Modify or extend the previous code if needed.
                    - No placeholders.
                    - No incomplete code.
                    - No explanations.
                    - No repetition of previous code unless explicitly asked.
                    - Return full runnable code only.

                    If multiple languages are requested:
                    - Output them in separate code blocks.
                    - Order exactly as requested.
                    - Use correct syntax for each language.

                    Ensure correctness and completeness.                    
                    """
                else:
                    structured_prompt = (
                        f"mode={decision['mode']}; "
                        f"emotion={processed['emotion']}; "
                        f"intent={processed['intent']}; "
                        f"urgency={'HIGH' if processed['urgent'] else 'LOW'}; "
                        f"tone={personalized}; "
                        f"situation=User interaction\n\n"
                    )

                agent = agent_map.get(agent_name, general_agent)
                generated = agent.run(structured_prompt, decision["mode"])

                if decision["mode"] == "CODE":
                    final_text = validate(generated.strip()) if generated else "Something went wrong."
                else:
                    final_text = validate(generated.strip()) if generated and generated.strip() else "Something went wrong. Try again."

            print(f"Vylencia: {final_text}")

            state.last_mode = decision["mode"]
            state.mode = "IDLE"

        except KeyboardInterrupt:
            save_relationship(state.relationship)
            log("Forced shutdown.")
            state.alive = False

        clock.tick()

    save_relationship(state.relationship)
    log("Vylencia has stopped.")

if __name__ == "__main__":
    main()
