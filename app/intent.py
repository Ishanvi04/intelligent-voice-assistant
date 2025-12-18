import re

KNOWN_SITES = {
    "google": "google.com",
    "youtube": "youtube.com",
    "spotify": "spotify.com",
    "github": "github.com",
    "gmail": "gmail.com"
}

def detect_intent(text):
    text = text.lower().strip()

    if "your name" in text or "who are you" in text:
        return "assistant_name", None

    if any(word in text for word in ["hello", "hi", "hey"]):
        return "greeting", None

    if any(word in text for word in ["quote", "motivate", "motivation", "inspire"]):
        return "tell_quote", None

    for site in KNOWN_SITES:
        if site in text:
            return "open_website", (KNOWN_SITES[site],)

    patterns = {
        "get_time": [r"\btime\b", r"\bdate\b"],
        "create_note": [r"note (.+)", r"remember (.+)"],
        "tell_joke": [r"joke", r"make me laugh"]
    }

    for intent, rules in patterns.items():
        for rule in rules:
            match = re.search(rule, text)
            if match:
                return intent, match.groups()

    return "unknown", None

