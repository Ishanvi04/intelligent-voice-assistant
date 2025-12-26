from app.tts import is_speaking, speak
from app.goal import goal, start_goal
from app.timer import start_timer
from app.alarm import add_alarm, parse_time, cancel_alarms, start_alarm_thread
from app.correction import suggest_correction
import time
from app.memory import set_user_name, get_user_name
from app.logger import log_message
from app.sounds import play_start_sound, play_stop_sound
from app.emotion import detect_emotion, get_emotion_response
from app.recorder import record_audio
from app.asr import transcribe_audio
from app.intent import detect_intent
import app.actions as actions
from app.llm import ask_llm

ASSISTANT_NAME = "lana"
WAKE_WORDS = ["lana", "hey lana", "laana", "lanna"]
ACTIVE_TIMEOUT = 25
RECORD_DELAY = 0.5

active = False
last_active_time = 0
sleeping = False


# ==========================================================
# 🔁 ONE COMPLETE VOICE INTERACTION (USED BY API + UI)
# ==========================================================
def handle_voice_interaction():
    global active, last_active_time, sleeping

    # 🔇 Wait if Lana is speaking
    while is_speaking:
        time.sleep(0.05)

    time.sleep(0.2)

    # 🎙 Record
    play_start_sound()
    record_audio()
    text = transcribe_audio().lower().strip()

    if not text:
        return {"status": "no_input"}

    print(f"HEARD: {text}")
    log_message("YOU", text)

    # ❌ Exit
    if any(w in text for w in ["bye", "goodbye"]):
        speak("Okay. I'm here if you need me.")
        active = False
        continue

    # 😴 Sleep mode
    if sleeping and not any(w in text for w in WAKE_WORDS):
        return {"status": "sleeping"}

    # 🟣 Wake word
    if not active:
        if any(w in text for w in WAKE_WORDS):
            active = True
            last_active_time = time.time()
            speak("Yes?")
            return {"status": "awake"}
        return {"status": "idle"}

    # ⏱ Auto sleep
    if time.time() - last_active_time > ACTIVE_TIMEOUT:
        active = False
        return {"status": "timeout"}

    command = text.replace(ASSISTANT_NAME, "").strip()
    print(f"YOU: {command}")

    intent, params = detect_intent(command)

    # 🎯 GOALS
    if intent == "goal_relax":
        start_goal("relax", [
            ("open_website", "youtube.com"),
            ("open_and_search", "lo-fi chill music"),
        ])
        speak("Okay. I’ll help you relax.")
        return {"status": "goal"}

    if intent == "goal_study":
        start_goal("study", [
            ("open_website", "google.com"),
            ("open_and_search", "pomodoro timer"),
            ("open_and_search", "focus music"),
        ])
        speak("Alright. Let’s get you ready to study.")
        return {"status": "goal"}

    # ⏲ Timers / actions
    if intent == "set_timer" and isinstance(params, int):
        response = start_timer(params)

    elif intent == "sleep":
        sleeping = True
        response = "Okay. I’ll stay quiet."

    elif intent == "wake":
        sleeping = False
        response = "I’m awake."

    elif intent == "get_time":
        response = actions.get_time()

    elif intent == "get_date":
        response = actions.get_date()

    elif intent == "open_website" and params:
        response = actions.open_website(params[0])

    elif intent == "open_and_search":
        response = actions.open_and_search(command)

    elif intent == "assistant_name":
        response = "My name is Lana."

    elif intent == "set_name":
        set_user_name(params)
        response = f"Nice to meet you, {params}."

    elif intent == "get_name":
        name = get_user_name()
        response = f"Your name is {name}." if name else "I don't know your name yet."

    elif intent == "tell_joke":
        response = actions.tell_joke()

    elif intent == "tell_quote":
        response = actions.tell_quote()

    else:
        # 🤖 LLM fallback
        response = ask_llm(command)

    speak(response)
    last_active_time = time.time()

    return {"status": "responded", "response": response}


# ==========================================================
# 🖥 TERMINAL MODE (UNCHANGED BEHAVIOR)
# ==========================================================
def run():
    print("Lana is running. Say 'lana' to wake me up.")
    speak("Say lana to wake me up.")

    try:
        while True:
            handle_voice_interaction()
            time.sleep(RECORD_DELAY)
    except KeyboardInterrupt:
        speak("Goodbye.")


if __name__ == "__main__":
    run()

