# core/state.py

from datetime import datetime

from core.relationship import RelationshipState

class VylenciaState:
    def __init__(self):
        self.alive = True
        self.started_at = datetime.now()
        self.last_interaction = {"text": None, "timestamp": datetime.now()}
        self.mode = "IDLE"  # IDLE | COMFORT | CODE | KNOWLEDGE | GUARDIAN | etc.
        self.notes = {} # reserved for future cognitive annotations.
        self.last_mode = None
        self.relationship = RelationshipState()

    def update_interaction(self, text: str):
        self.last_interaction = {
            "text": text,
            "timestamp": datetime.now()
        }
