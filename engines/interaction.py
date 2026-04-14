# engines/interaction.py

import re
import difflib
from embeddings.bge_embedder import BgeEmbedder
import numpy as np

embedder = BgeEmbedder()

SHORT_INPUTS = ["hi", "hello", "hey", "yo", "hey there", "hi there"]

CASUAL_PATTERNS = [
    "how are you",
    "what's up",
    "how's it going",
    "how are you doing",
    "how's it going"
]

INTENT_PROTOTYPES = {
    "KNOWLEDGE": [
        "ask about a topic",
        "explain something",
        "compare two things",
        "give information",
        "what is something",
        "performance comparison",
        "benchmark comparison",
        "technical explanation"
    ],
    "CODE_GENERATION": [
        "write code",
        "generate code",
        "create function",
        "implement algorithm",
        "give code example"
    ],
    "SOCIAL": [
        "talk casually",
        "chat with assiatant",
        "personal interaction",
        "ask about assistant",
        "name you",
        "call you",
    ],
    "CODE_CONCEPT": [
        "can we build",
        "how does this work",
        "what is possible with",
        "is it possible to",
        "explain system design",
        "compare programming languages"
    ],
    "VENTING": [
        "express feelings",
        "talk about stress",
        "emotional support",
        "feeling sad or overwhelmed"
    ],
    "ENTERTAINMENT": [
        "tell a joke",
        "make me laugh",
        "entertain me"
    ],
    "SEEK_ADVICE": [
        "what should I do",
        "give advice",
        "help me decide"
    ]
}

INTENT_EMBEDS = {
    intent: embedder.embed(texts)
    for intent, texts in INTENT_PROTOTYPES.items()
}

EMOTION_KEYWORDS = {
    "SAD": ["sad", "down", "depressed", "hurt", "lonely", "tired"],
    "ANGRY": ["angry", "mad", "furious", "annoyed", "irritated"],
    "STRESSED": ["stressed", "pressure", "overwhelmed", "anxious"],
    "CONFUSED": ["confused", "lost", "don't know", "unsure"],
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

def cosine(a, b):
    return float(np.dot(a, b))

def detect_intent(text: str) -> str:
    lowered = text.lower().strip()

    # greeting
    if lowered in SHORT_INPUTS:
        return "GREETING"
    
    if any(lowered.startswith(greet) for greet in SHORT_INPUTS):
        return "GREETING"

    # casual
    for phrase in CASUAL_PATTERNS:
        if phrase in lowered:
            return "GENERAL"

    # short queries → treat as knowledge
    if len(lowered.split()) <= 2:
        return "KNOWLEDGE"

    query_vec = embedder.embed(text, is_query=True)

    best_intent = "UNKNOWN"
    best_score = -1

    for intent, vectors in INTENT_EMBEDS.items():
        for vec in vectors:
            score = cosine(query_vec, vec)

            if score > best_score:
                best_score = score
                best_intent = intent

    if best_score < 0.45:
        return "UNKNOWN"

    # conceptual override
    if best_intent == "CODE_GENERATION":
        if any(kw in lowered for kw in ["can", "what", "how", "is it possible"]):
            best_intent = "CODE_CONCEPT"

    return best_intent

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
