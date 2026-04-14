# engines/decision.py

def decide(processed_input: dict, state):
    emotion = processed_input["emotion"]
    intent = processed_input["intent"]
    urgent = processed_input["urgent"]

    if urgent and intent == "COMMAND" and emotion != "CALM":
        return {
            "mode": "GUARDIAN",
            "action": {
                "type": "BLOCK",
                "payload": {"reason": "emotional instability with urgent command"}
            },
            "message": "Let’s pause. I need to keep things safe right now."
        }

    if intent == "ENTERTAINMENT":
        return {
            "mode": "ENTERTAINMENT",
            "action": None,
            "message": "Here’s something to make you smile."
        }
    
    if intent == "CODE_GENERATION":
        return {
            "mode": "CODE",
            "action": None,
            "message": ""
        }
    
    if intent == "CODE_CONCEPT":
        return {
            "mode": "KNOWLEDGE",
            "action": None,
            "message": ""
        }
    
    if intent == "KNOWLEDGE":
        return {
            "mode": "KNOWLEDGE",
            "action": None,
            "message": ""
        }
    
    if intent in ("GENERAL", "GREETING"):
        return {
            "mode": "GENERAL",
            "action": None,
            "message": ""
        }
    
    if intent == "SOCIAL":
        mode = "GENERAL"

    if emotion in ("SAD", "ANGRY", "STRESSED", "CONFUSED"):
        if intent == "SEEK_ADVICE":
            return {
                "mode": "COMFORT_GUIDANCE",
                "action": None,
                "message": "I’m here with you. Let’s slow down and look at this together."
            }
        else:
            return {
                "mode": "COMFORT",
                "action": None,
                "message": "I hear you. You don’t have to handle this alone."
            }

    if intent == "SEEK_ADVICE":
        return {
            "mode": "GUIDANCE",
            "action": None,
            "message": "Let’s think this through step by step."
        }

    if intent == "COMMAND":
        return {
            "mode": "GUIDANCE",
            "action": None,
            "message": "I understand what you want to do. Let’s make sure it’s the right approach."
        }
        
    return {
        "mode": "COMFORT",
        "action": None,
        "message": "I’m here. Tell me a little more."
    }

