# core/relationship.py

class RelationshipState:
    """
    Tracks how Vylencia relates to YOU over time.
    This is not emotion. This is familiarity and trust.
    """

    def __init__(self):
        self.familiarity = 0.0   # grows slowly
        self.trust = 0.5         # starts neutral-positive
        self.warmth = 0.5        # controls tone softness
        self.last_mode = None
        self.last_phrase = None

    def grow(self, delta=0.02):
        effective = delta * (1.0 - self.familiarity)
        self.familiarity = min(1.0, self.familiarity + effective)
        self.warmth = min(0.85, self.warmth + effective / 2)

    def adjust_trust(self, delta):
        self.trust = max(0.0, min(1.0, self.trust + delta))

    def clamp(self):
        self.warmth = max(0.0, min(self.warmth, 0.85))
        self.trust = max(0.0, min(self.trust, 0.9))
        self.familiarity = max(0.0, min(self.familiarity, 1.0))
