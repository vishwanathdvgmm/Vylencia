# policies/personality.py

import random

class PersonalityPolicy:
    def apply(self, decision, processed_input, state):
        mode = decision["mode"]
        emotion = processed_input["emotion"]
        rel = state.relationship

        if rel.last_mode != mode:
            rel.grow()

        message = (decision.get("message") or "").strip()

        if not message and mode not in ["COMFORT", "COMFORT_GUIDANCE", "GUIDANCE", "GUARDIAN"]:
            return ""

        if mode == "COMFORT":
            message = self._comfort(message, emotion, rel)

        elif mode == "COMFORT_GUIDANCE":
            message = self._comfort_guidance(message, emotion, rel)

        elif mode == "GUIDANCE":
            message = self._guidance(message, rel)

        elif mode == "GUARDIAN":
            message = self._guardian(message, rel)

        rel.clamp()

        rel.last_mode = mode
        return message.strip()

    def _comfort(self, base, emotion, rel):
        variants = [
            "I'm right here with you.",
            "You don't have to go through this alone.",
            "Take your time. I'm with you.",
            "I hear you. You're not alone in this.",
            "It's okay to feel this way. I'm here.",
            "We'll get through this together."
        ]

        choices = [v for v in variants if v != rel.last_phrase]
        chosen = random.choice(choices) if choices else random.choice(variants)

        rel.last_phrase = chosen
        softness = chosen if rel.warmth > 0.4 else "I'm here."

        if emotion == "ANGRY":
            softness = "Let's slow this down together."
            rel.last_phrase = softness
        elif emotion == "SAD":
            softness = chosen
        
        if base.lower().startswith(softness.lower()):
            return base

        return f"{softness} {base}".strip()

    def _comfort_guidance(self, base, emotion, rel):
        lead = [
            "I understand how this feels.",
            "That sound really tough."
        ]
        if rel.warmth > 0.6:
            lead = [
                "I get why this is heavy for you.",
                "I can see why this matters to you."
            ]
        return f"{random.choice(lead)} {base}".strip()

    def _guidance(self, base, rel):
        if rel.trust > 0.7:
            leads = [
                "I trust your judgment. Let's refine this.",
                "You've got a good sense here. Let's sharpen it.",
            ]
        elif rel.trust > 0.5:
            leads = [
                "I'm with you. Let's think carefully.",
                "Let's slow this down and look at it clearly.",
            ]
        else:
            return f"Let's think this through. {base}".strip()

        return f"{random.choice(leads)} {base}".strip()

    def _guardian(self, base, rel):
        lead = "I need to pause this to keep you safe."
        if rel.trust > 0.6:
            lead = "I care about you too much to risk this."
        return f"{lead} {base}".strip()

