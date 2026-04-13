# engines/control.py

from utils.logger import log

def execute(decision, state):
    action = decision.get("action")

    if action is None:
        return None

    action_type = action.get("type")
    payload = action.get("payload", {})

    if action_type == "SIMULATE":
        log(f"CONTROL: Simulating action with payload={payload}")
        return {"status": "simulated"}

    if action_type == "LOG":
        log(f"CONTROL: Logged action payload={payload}")
        return {"status": "logged"}

    if action_type == "BLOCK":
        log("CONTROL: Action blocked for safety.")
        return {"status": "blocked"}

    log("CONTROL: Unknown action encountered; no-op.")
    return {"status": "noop"}
