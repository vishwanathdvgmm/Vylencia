# engines/interaction.py

import re
import difflib

EMOTION_KEYWORDS = {
    "SAD": ["sad", "down", "depressed", "hurt", "lonely", "tired"],
    "ANGRY": ["angry", "mad", "furious", "annoyed", "irritated"],
    "STRESSED": ["stressed", "pressure", "overwhelmed", "anxious"],
    "CONFUSED": ["confused", "lost", "don't know", "unsure"],
}

INTENT_KEYWORDS = {
    "VENTING": ["feel", "feeling", "just vent", "need to talk"],
    "SEEK_ADVICE": ["should i", "what should", "how do i", "advice"],
    "COMMAND": ["run ", "start ", "stop ", "make ", "create "],
    "REFLECTION": ["thinking", "realize", "i think", "i believe"],
    "ENTERTAINMENT": ["joke", "funny", "make me laugh", "entertain"],
    "KNOWLEDGE": ["what is", "who is", "tell me about", "explain", "define", "how does", "why is"],
    "CODE": ["code", "function", "program", "debug", "fix bug", "write code"],
}

def detect_emotion(text: str) -> str:
    lowered = text.lower()

    for emotion, keywords in EMOTION_KEYWORDS.items():
        for word in keywords:

            if word in lowered:
                return emotion
            
            matches = difflib.get_close_matches(word, lowered.split(), n=1, cutoff=0.7)
            if matches:
                return emotion

    return "CALM"

def detect_intent(text: str) -> str:
    lowered = text.lower()

    for intent in ["CODE", "KNOWLEDGE", "ENTERTAINMENT", "SEEK_ADVICE", "COMMAND", "REFLECTION", "VENTING"]:
        for phrase in INTENT_KEYWORDS.get(intent, []):
            if phrase in lowered:
                return intent
    return "UNKNOWN"

def detect_urgency(text: str) -> bool:
    return bool(re.search(r"\b(now|urgent|immediately|asap)\b", text.lower()))

def process_input(user_input: str, state):
    emotion = detect_emotion(user_input)
    intent = detect_intent(user_input)
    urgent = detect_urgency(user_input)

    return {
        "raw_input": user_input,
        "emotion": emotion,
        "intent": intent,
        "urgent": urgent,
        "timestamp": state.last_interaction["timestamp"] if state.last_interaction else None,
    }
