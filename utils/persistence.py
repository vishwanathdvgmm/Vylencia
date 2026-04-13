# utils/persistence.py

import json
import os

REL_PATH = "data/relationship.json"

DEFAULT_REL = {
    "familiarity": 0.0,
    "trust": 0.5,
    "warmth": 0.5,
    "last_mode": None,
    "last_phrase": None
}

def load_relationship():
    if not os.path.exists(REL_PATH):
        return DEFAULT_REL.copy()
    try:
        with open(REL_PATH, "r") as f:
            data = json.load(f)
        merged = DEFAULT_REL.copy()
        merged.update({k: data.get(k, merged[k]) for k in merged})
        return merged
    except Exception:
        return DEFAULT_REL.copy()

def save_relationship(rel_state):
    data = {
        "familiarity": rel_state.familiarity,
        "trust": rel_state.trust,
        "warmth": rel_state.warmth,
        "last_mode": rel_state.last_mode,
        "last_phrase": rel_state.last_phrase
    }
    os.makedirs(os.path.dirname(REL_PATH), exist_ok=True)
    tmp = REL_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, REL_PATH)
