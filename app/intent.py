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

    # ---------- SELF DIAGNOSTICS ----------
    if any(word in text for word in ["diagnose", "diagnostics", "check yourself"]):
        return "diagnose", None

    # ---------- MULTI-COMMAND ----------
    if "open" in text and "search" in text:
        return "open_and_search", None

    # ---------- SYSTEM INFO ----------
    if any(word in text for word in ["battery", "charge", "power level"]):
        return "get_battery", None

    # ---------- DATE (CHECK FIRST) ----------
    if any(word in text for word in ["date", "today", "day"]):
        return "get_date", None

    # ---------- TIME ----------
    if "time" in text:
        return "get_time", None

    # ---------- IDENTITY ----------
    if any(phrase in text for phrase in ["your name", "who are you"]):
        return "assistant_name", None

    # ---------- GREETING ----------
    if any(word in text for word in ["hello", "hi", "hey"]):
        return "greeting", None

    # ---------- QUOTES ----------
    if any(word in text for word in ["quote", "motivate", "motivation", "inspire"]):
        return "tell_quote", None

    # ---------- FOLLOW-UP COMMANDS ----------
    if text in ["open", "open something"]:
        return "open_website", None

    if text in ["note", "make a note", "write a note"]:
        return "create_note", None

    # ---------- DIRECT WEBSITE ----------
    for site in KNOWN_SITES:
        if site in text:
            return "open_website", (KNOWN_SITES[site],)

    # ---------- REGEX COMMANDS ----------
    patterns = {
        "create_note": [r"note (.+)", r"remember (.+)"],
        "tell_joke": [r"\bjoke\b", r"make me laugh"]
    }

    for intent, rules in patterns.items():
        for rule in rules:
            match = re.search(rule, text)
            if match:
                return intent, match.groups()

    return "unknown", None

