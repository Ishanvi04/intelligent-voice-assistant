import json
import os

PROFILE_PATH = "app/profile.json"

# ---------- LOAD PROFILE ----------
def load_profile():
    if not os.path.exists(PROFILE_PATH):
        return {}

    try:
        with open(PROFILE_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return {}

# ---------- SAVE PROFILE ----------
def save_profile(profile):
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=4)

# ---------- SET USER NAME ----------
def set_user_name(name):
    profile = load_profile()
    profile["name"] = name
    save_profile(profile)

# ---------- GET USER NAME ----------
def get_user_name():
    profile = load_profile()
    return profile.get("name")

# ---------- STORE LAST EMOTION ----------
def set_last_emotion(emotion):
    profile = load_profile()
    profile["last_emotion"] = emotion
    save_profile(profile)

# ---------- GET LAST EMOTION ----------
def get_last_emotion():
    profile = load_profile()
    return profile.get("last_emotion")

# ---------- SUMMARY MEMORY ----------
def get_memory_summary():
    profile = load_profile()

    if not profile:
        return "I don't have any memory about you yet."

    parts = []

    if "name" in profile:
        parts.append(f"Your name is {profile['name']}.")

    if "last_emotion" in profile:
        parts.append(f"Earlier you sounded {profile['last_emotion']}.")

    return " ".join(parts)

