def ask_llm(prompt: str) -> str:
    p = prompt.lower().strip()

    if "bye" in p:
        return "Goodbye. Shutting down now."

    if "time" in p:
        from datetime import datetime
        return f"The time is {datetime.now().strftime('%I:%M %p')}."

    if "joke" in p:
        return "Why did the computer catch a cold? Because it forgot to close its Windows."

    if "black hole" in p:
        return "A black hole is a region in space where gravity is so strong that nothing can escape."

    if "lunar eclipse" in p:
        return "A lunar eclipse happens when the Earth moves between the Sun and the Moon."

    if "photosynthesis" in p:
        return "Photosynthesis is how plants use sunlight to make food from carbon dioxide and water."

    if "your name" in p:
        return "My name is Lana."

    if "my name" in p:
        return "I don't have memory yet, but you can tell me your name."

    # 🔥 SMART FALLBACK
    return f"I heard you say '{prompt}', but I am still learning that topic."

