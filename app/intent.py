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
    # System info


     # Multi-command: open X and search Y
    if "open" in text and "search" in text:
        return "open_and_search", None

    if any(word in text for word in ["battery", "charge", "power level"]):
        return "get_battery", None

    # ---------- IDENTITY ----------
    if "your name" in text or "who are you" in text:
        return "assistant_name", None

    # ---------- GREETING ----------
    if any(word in text for word in ["hello", "hi", "hey"]):
        return "greeting", None

    # ---------- QUOTES / MOTIVATION ----------
    if any(word in text for word in ["quote", "motivate", "motivation", "inspire"]):
        return "tell_quote", None

    # ---------- SYSTEM INFO ----------
    if "battery" in text:
        return "battery", None

    if "cpu" in text:
        return "cpu", None

    if "memory" in text or "ram" in text:
        return "memory", None

    # ---------- FOLLOW-UP (PARTIAL COMMANDS) ----------
    if text in ["open", "open something"]:
        return "open_website", None

    if text in ["note", "make a note", "write a note"]:
        return "create_note", None

    # ---------- DIRECT WEBSITE ----------
    for site in KNOWN_SITES:
        if site in text:
            return "open_website", (KNOWN_SITES[site],)

    # ---------- REGEX PATTERNS ----------
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

