# engines/governance.py

from utils.logger import log

ALLOWED_ACTIONS = {"SIMULATE", "LOG", "BLOCK"}

def allow(decision, state):
    action = decision.get("action")

    if action is None:
        return True

    action_type = action.get("type", "")

    if action_type not in ALLOWED_ACTIONS:
        log(f"GOVERNANCE: Blocked unknown action type={action_type}")
        return False

    if decision.get("mode") == "GUARDIAN":
        log("GOVERNANCE: Guardian Mode active — action allowed under containment.")
        return True

    if state.mode == "GUARDIAN":
        if action_type not in {"BLOCK", "LOG"}:
            log("GOVERNANCE: Non-safe action blocked during Guardian Mode")
            return False

    return True
