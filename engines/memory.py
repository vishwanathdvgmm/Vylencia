# engines/memory.py

import json
import os
from datetime import datetime

MEMORY_PATH = "data/memory.json"
MAX_EVENTS = 1000

def _load_memory():
    if not os.path.exists(MEMORY_PATH):
        return {"events": [], "patterns": {}}
    try:
        with open(MEMORY_PATH, "r") as f:
            data = json.load(f)
        return {
            "events": data.get("events", []),
            "patterns": data.get("patterns", {})
        }
    except Exception:
        return {"events": [], "patterns": {}}

def _save_memory(memory):
    os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)
    tmp = MEMORY_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(memory, f, indent=2)
    os.replace(tmp, MEMORY_PATH)

def decay_patterns(memory, decay_factor=0.95):
    for key in list(memory["patterns"].keys()):
        memory["patterns"][key] *= decay_factor
        if memory["patterns"][key] < 0.5:
            del memory["patterns"][key]

def update_memory(processed_input, decision, state):
    memory = _load_memory()

    emotion = processed_input["emotion"]
    intent = processed_input["intent"]
    mode = decision["mode"]

    event = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "emotion": emotion,
        "intent": intent,
        "mode": mode
    }

    memory["events"].append(event)
    if len(memory["events"]) > MAX_EVENTS:
        memory["events"] = memory["events"][-MAX_EVENTS:]

    pattern_key = f"{emotion}_{intent}"
    decay_patterns(memory)
    memory["patterns"][pattern_key] = memory["patterns"].get(pattern_key, 0) + 1

    _save_memory(memory)

def recall_relevant(emotion=None, intent=None):
    memory = _load_memory()
    patterns = memory.get("patterns", {})

    if not emotion or not intent:
        return {"pattern_count": 0}

    key = f"{emotion}_{intent}"
    return {
        "pattern_count": patterns.get(key, 0)
    }
