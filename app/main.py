import time
from history import add_to_history, get_full_history, get_last_command
import context
from history import add_to_history, get_full_history, get_last_command
from diagnostics import run_diagnostics
from logger import log_message
from sounds import play_start_sound, play_stop_sound
from emotion import detect_emotion, get_emotion_response
from recorder import record_audio
from asr import transcribe_audio
from intent import detect_intent
import actions
from tts import speak

ASSISTANT_NAME = "lana"
WAKE_WORDS = ["lana", "laana", "lanna", "lanaah"]
ACTIVE_TIMEOUT = 20
RECORD_DELAY = 1.0

# ---------- Terminal Colors ----------
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
PINK = "\033[95m"
# ---------- Safe Speaking Helper ----------
def speak_and_wait(text):
    speak(text)
    # Wait long enough so mic doesn't hear Lana's own voice
    time.sleep(max(1.5, len(text.split()) * 0.45))

def run():
    print(f"{ASSISTANT_NAME.capitalize()} is running. Say '{ASSISTANT_NAME}' to wake me up.")
    speak(f"Say {ASSISTANT_NAME} to wake me up.")
    time.sleep(1)

    active = False
    last_active_time = 0

    # ---------- GRACEFUL SHUTDOWN ----------
    def graceful_shutdown(message):
        play_stop_sound()
        print(f"{PINK}LANA:{RESET} {message}")
        log_message("LANA", message)
        speak(message)

        words = len(message.split())
        wait_time = max(3.0, words * 0.45)
        time.sleep(wait_time)

        raise SystemExit

    try:
        while True:
            response = None

            # -------- PASSIVE LISTENING --------
            time.sleep(RECORD_DELAY)
            play_start_sound()
            record_audio()

            text = transcribe_audio().lower().strip()
            if not text:
                continue

            print(f"{RED}HEARD:{RESET} {text}")
            log_message("YOU", text)

            # -------- EXIT ANYTIME --------
            if any(word in text for word in ["exit", "bye", "goodbye", "quit"]):
                graceful_shutdown(
                    "Goodbye. Take care. You can call me anytime."
                )

            # -------- WAKE MODE --------
            if not active:
                if any(w in text for w in WAKE_WORDS):
                    active = True
                    last_active_time = time.time()
                    print(f"{PINK}LANA:{RESET} Activated")
                    log_message("LANA", "Activated")
                    speak("Yes?")
                continue

            # -------- AUTO SLEEP --------
            if time.time() - last_active_time > ACTIVE_TIMEOUT:
                active = False
                log_message("SYSTEM", "Going to sleep")
                continue

            # -------- COMMAND MODE --------
            command = text.replace(ASSISTANT_NAME, "").strip()
            print(f"{GREEN}YOU:{RESET} {command}")

            # -------- EMOTION DETECTION --------
            emotion = detect_emotion(command)
            if emotion:
                response = get_emotion_response(emotion)
                print(f"{PINK}LANA:{RESET} {response}")
                log_message("LANA", response)
                speak(response)
                last_active_time = time.time()
                continue

            # -------- INTENT DETECTION --------
            intent, params = detect_intent(command)

            # ---- FOLLOW-UP QUESTIONS ----
            if intent == "open_website" and not params:
                context.pending_intent = "open_website"
                response = "What would you like me to open?"
                print(f"{PINK}LANA:{RESET} {response}")
                log_message("LANA", response)
                speak(response)
                continue

            if intent == "create_note" and not params:
                context.pending_intent = "create_note"
                response = "What should I write in the note?"
                print(f"{PINK}LANA:{RESET} {response}")
                log_message("LANA", response)
                speak(response)
                continue

            # ---- HANDLE FOLLOW-UP ANSWER ----
            if context.pending_intent:
                if context.pending_intent == "open_website":
                    response = actions.open_website(command)
                elif context.pending_intent == "create_note":
                    response = actions.create_note(command)

                context.reset()
                print(f"{PINK}LANA:{RESET} {response}")
                log_message("LANA", response)
                speak(response)
                last_active_time = time.time()
                continue

            # ---- NORMAL INTENTS ----
            if intent == "get_time":
                response = actions.get_time()
            elif intent == "show_history":
                response = get_full_history()

            elif intent == "last_command":
                response = get_last_command()

            elif intent == "get_date":
                response = actions.get_date()

            elif intent == "open_and_search":
                response = actions.open_and_search(command)

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
            elif intent == "help":
                response = (
                 "I can tell time and date, open websites, take notes, "
                 "tell jokes and quotes, check battery, detect emotions, "
                 "and run system diagnostics."
          )


            elif intent == "diagnose":
                response = "Running system diagnostics."
                print(f"{PINK}LANA:{RESET} {response}")
                add_to_history(command, response)
                log_message("LANA", response)
                speak(response)

                results, all_ok = run_diagnostics()
                for msg in results:
                    print(f"{PINK}LANA:{RESET} {msg}")
                    log_message("LANA", msg)
                    speak(msg)

                final = "All systems are operational." if all_ok else "Some systems need attention."
                print(f"{PINK}LANA:{RESET} {final}")
                log_message("LANA", final)
                speak(final)

                last_active_time = time.time()
                continue

            else:
                response = "Sorry, I didn't understand that."

            print(f"{PINK}LANA:{RESET} {response}")
            log_message("LANA", response)
            speak(response)
            last_active_time = time.time()

    except KeyboardInterrupt:
        play_stop_sound()
        print("\nAssistant stopped manually.")
        speak("Goodbye.")


if __name__ == "__main__":
    run()

