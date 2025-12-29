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

    # ================= GOALS (HIGH PRIORITY) =================
    if any(phrase in text for phrase in [
        "help me relax",
        "i want to relax",
        "relax me",
        "make me relax"
    ]):
        return "goal_relax", None

    if any(phrase in text for phrase in [
        "help me study",
        "prepare me for studying",
        "i want to study"
    ]):
        return "goal_study", None

    # ================= SLEEP / WAKE =================
    if any(phrase in text for phrase in [
        "go to sleep",
        "sleep mode",
        "do not disturb"
    ]):
        return "sleep", None

    if any(phrase in text for phrase in [
        "wake up",
        "resume",
        "i'm back"
    ]):
        return "wake", None

    # ================= TIMER (REGEX FIRST — FIX) =================
    match = re.search(
        r"(set|start)?\s*(a)?\s*timer\s*(for|of)?\s*(\d+)\s*(second|seconds|minute|minutes|hour|hours)",
        text
    )
    if match:
        amount = int(match.group(4))
        unit = match.group(5)

        if "second" in unit:
            seconds = amount
        elif "minute" in unit:
            seconds = amount * 60
        elif "hour" in unit:
            seconds = amount * 3600
        else:
            seconds = amount

        return "set_timer", seconds

    # ================= ALARM =================
    if "cancel alarm" in text or "stop alarm" in text:
        return "cancel_alarm", None

    if "alarm" in text:
        return "set_alarm", None

    # ================= NAME MEMORY =================
    if text.startswith("my name is"):
        return "set_name", text.replace("my name is", "").strip()

    if any(phrase in text for phrase in [
        "what is my name",
        "what's my name"
    ]):
        return "get_name", None

    # ================= COMMAND HISTORY =================
    if any(phrase in text for phrase in [
        "command history",
        "show history",
        "what did i say",
        "what did i say earlier"
    ]):
        return "show_history", None

    if any(phrase in text for phrase in [
        "last command",
        "repeat last command"
    ]):
        return "last_command", None

    # ================= DIAGNOSTICS =================
    if any(word in text for word in [
        "diagnose",
        "diagnostics",
        "check yourself"
    ]):
        return "diagnose", None

    # ================= HELP =================
    if any(word in text for word in [
        "help",
        "what can you do",
        "commands"
    ]):
        return "help", None

    # ================= MULTI COMMAND =================
    if "open" in text and "search" in text:
        return "open_and_search", None

    # ================= SYSTEM INFO =================
    if any(word in text for word in [
        "battery",
        "charge",
        "power level"
    ]):
        return "get_battery", None

    # ================= DATE / TIME (AFTER TIMER — FIX) =================
    if any(word in text for word in ["date", "today", "day"]):
        return "get_date", None

    if "time" in text:
        return "get_time", None

    # ================= IDENTITY =================
    if any(phrase in text for phrase in [
        "your name",
        "who are you"
    ]):
        return "assistant_name", None

    # ================= GREETING =================
    if any(word in text for word in [
        "hello",
        "hi",
        "hey"
    ]):
        return "greeting", None

    # ================= QUOTES / JOKES =================
    if any(word in text for word in [
        "quote",
        "motivate",
        "motivation",
        "inspire"
    ]):
        return "tell_quote", None

    patterns = {
        "create_note": [r"note (.+)", r"remember (.+)"],
        "tell_joke": [r"\bjoke\b", r"make me laugh"]
    }

    for intent, rules in patterns.items():
        for rule in rules:
            match = re.search(rule, text)
            if match:
                return intent, match.groups()

    # ================= DIRECT WEBSITE =================
    for site in KNOWN_SITES:
        if site in text:
            return "open_website", (KNOWN_SITES[site],)

    # ================= SAFE FALLBACK =================
    return "unknown", None

