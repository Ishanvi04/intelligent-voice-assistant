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

    # Direct site names (no "open")
    for site in KNOWN_SITES:
        if site in text:
            return "open_website", (KNOWN_SITES[site],)

    patterns = {
        "get_time": [r"\btime\b"],
        "create_note": [r"note (.+)", r"remember (.+)"],
        "tell_joke": [r"joke", r"make me laugh"]
    }

    for intent, rules in patterns.items():
        for rule in rules:
            match = re.search(rule, text)
            if match:
                return intent, match.groups()

    return "unknown", None

