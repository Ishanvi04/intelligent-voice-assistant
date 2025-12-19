import time
import context
from sounds import play_start_sound, play_stop_sound
from emotion import detect_emotion, get_emotion_response
from recorder import record_audio
from asr import transcribe_audio
from intent import detect_intent
import actions
from tts import speak

ASSISTANT_NAME = "lana"
WAKE_WORDS = ["lana", "laana", "lanna", "lanaah"]
ACTIVE_TIMEOUT = 20        # seconds
RECORD_DELAY = 1.0        # prevents TTS + mic overlap


def run():
    print(f"{ASSISTANT_NAME.capitalize()} is running. Say '{ASSISTANT_NAME}' to wake me up.")

    active = False
    last_active_time = 0

    try:
        while True:
            # -------- PASSIVE LISTENING --------
            time.sleep(RECORD_DELAY)
            play_start_sound()
            record_audio()

            text = transcribe_audio().lower().strip()
            if not text:
                continue

            print("Heard:", text)

            # -------- EXIT ANYTIME --------
            if any(word in text for word in ["exit", "bye", "goodbye", "quit"]):
                play_stop_sound()
                speak("Goodbye. Shutting down.")
                print("Assistant stopped.")
                break

            # -------- WAKE MODE --------
            if not active:
                if any(w in text for w in WAKE_WORDS):
                    active = True
                    last_active_time = time.time()
                    speak("Yes?")
                    time.sleep(RECORD_DELAY)
                    print("Activated")
                continue

            # -------- AUTO SLEEP --------
            if time.time() - last_active_time > ACTIVE_TIMEOUT:
                active = False
                print("Going to sleep.")
                continue

            # -------- COMMAND MODE --------
            command = text.replace(ASSISTANT_NAME, "").strip()
            print("Command:", command)

            # -------- EMOTION DETECTION --------
            emotion = detect_emotion(command)
            if emotion:
                response = get_emotion_response(emotion)
                print("Emotion detected:", emotion)
                speak(response)
                time.sleep(RECORD_DELAY)
                last_active_time = time.time()
                continue

            # -------- INTENT DETECTION --------
            intent, params = detect_intent(command)

            # ---- FOLLOW-UP QUESTIONS ----
            if intent == "open_website" and not params:
                context.pending_intent = "open_website"
                speak("What would you like me to open?")
                continue

            if intent == "create_note" and not params:
                context.pending_intent = "create_note"
                speak("What should I write in the note?")
                continue

            # ---- HANDLE FOLLOW-UP ANSWER ----
            if context.pending_intent:
                if context.pending_intent == "open_website":
                    response = actions.open_website(command)
                elif context.pending_intent == "create_note":
                    response = actions.create_note(command)

                context.reset()
                speak(response)
                last_active_time = time.time()
                continue

            # ---- NORMAL INTENTS ----
            if intent == "get_time":
                response = actions.get_time()

            elif intent == "open_website":
                response = actions.open_website(params[0])

            elif intent == "create_note":
                response = actions.create_note(params[0])

            elif intent == "get_battery":
                response = actions.get_battery()

            elif intent == "tell_joke":
                response = actions.tell_joke()

            elif intent == "tell_quote":
                response = actions.tell_quote()

            elif intent == "assistant_name":
                response = f"My name is {ASSISTANT_NAME.capitalize()}."

            elif intent == "greeting":
                response = "Hello! How can I help you?"

            else:
                response = "Sorry, I didn't understand that."

            print("Assistant:", response)
            speak(response)
            time.sleep(RECORD_DELAY)
            last_active_time = time.time()

    except KeyboardInterrupt:
        play_stop_sound()
        print("\nAssistant stopped manually.")
        speak("Goodbye.")


if __name__ == "__main__":
    run()

