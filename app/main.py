from app.llm import ask_llm
from app.tts import is_speaking, speak
from app.goal import start_goal
from app.timer import start_timer
from app.memory import set_user_name, get_user_name
from app.logger import log_message
from app.sounds import play_start_sound
from app.recorder import record_audio
from app.asr import transcribe_audio
from app.intent import detect_intent
import app.actions as actions
from app.llm import ask_llm
import time
RECORD_DELAY = 0.5  # seconds between listens

ASSISTANT_NAME = "lana"
WAKE_WORDS = ["lana", "hey lana", "laana", "lanna"]

active = False
sleeping = False


# ==========================================================
# ✅ SINGLE INTERACTION — CALLED BY OVERLAY CLICK
# ==========================================================
def run():
    print("Lana is running. Say 'lana' to wake me up.")
    speak("Say lana to wake me up.")

    try:
        while True:
            result = handle_voice_interaction()

            if result and result.get("status") == "exit":
                print("Lana stopped.")
                break

            time.sleep(RECORD_DELAY)

    except KeyboardInterrupt:
        speak("Goodbye.")
def handle_voice_interaction():
    global active, sleeping

    # Wait if TTS is still speaking
    while is_speaking:
        time.sleep(0.05)

    play_start_sound()

    record_audio()
    text = transcribe_audio()

    if not text:
        return

    text = text.lower().strip()
    print(f"HEARD: {text}")
    log_message("YOU", text)

    # Exit
    if any(w in text for w in ["bye", "goodbye"]):
        speak("Okay. I'm here when you need me.")
        return {"status": "exit"}

    # Wake
    if not active:
        if any(w in text for w in WAKE_WORDS):
            active = True
            speak("Yes?")
        return

    command = text.replace(ASSISTANT_NAME, "").strip()
    intent, params = detect_intent(command)

    # === INTENTS ===
    if intent == "get_time":
        response = actions.get_time()

    elif intent == "get_date":
        response = actions.get_date()

    elif intent == "open_website":
        response = actions.open_website(params[0])

    elif intent == "set_timer":
        response = start_timer(params)

    elif intent == "set_name":
        set_user_name(params)
        response = f"Nice to meet you, {params}."

    elif intent == "get_name":
        name = get_user_name()
        response = f"Your name is {name}." if name else "I don't know your name yet."

    else:
        response = ask_llm(command)

    speak(response)

