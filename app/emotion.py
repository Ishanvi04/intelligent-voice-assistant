EMOTION_KEYWORDS = {
    "sad": ["sad", "down", "depressed", "low"],
    "happy": ["happy", "excited", "great", "awesome"],
    "tired": ["tired", "sleepy", "exhausted", "burnt"],
    "stressed": ["stressed", "anxious", "overwhelmed"],
    "angry": ["angry", "mad", "frustrated"]
}

EMOTION_RESPONSES = {
    "sad": "I'm sorry you're feeling sad. Do you want to talk about it?",
    "happy": "That's wonderful to hear! Keep smiling.",
    "tired": "Sounds like you need some rest. Want a short motivation instead?",
    "stressed": "That sounds stressful. Take a deep breath with me.",
    "angry": "I can hear the frustration. Want me to help calm things down?"
}

def detect_emotion(text):
    text = text.lower()
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for word in keywords:
            if word in text:
                return emotion
    return None

def get_emotion_response(emotion):
    return EMOTION_RESPONSES.get(emotion)

