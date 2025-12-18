import time
from recorder import record_audio
from asr import transcribe_audio
from intent import detect_intent
import actions
from tts import speak

ASSISTANT_NAME = "lana"
WAKE_WORDS = ["lana", "laana", "lahna", "lanaah"]

def run():
    print(f"{ASSISTANT_NAME.capitalize()} is running. Say '{ASSISTANT_NAME}' to activate.")
    active = False  # assistant state

    try:
        while True:
            # -------- Passive listening --------
            record_audio()
            text = transcribe_audio().lower().strip()
            print("Heard:", text)

            # Hard exit (shutdown app)
            if any(word in text for word in ["shutdown app", "force exit"]):
                speak("Shutting down. Goodbye.")
                break

            # Wake up
            if not active and any(w in text for w in WAKE_WORDS):
                active = True
                speak("Yes?")
                time.sleep(0.6)
                print("Activated")
                continue

            # Ignore everything if sleeping
            if not active:
                continue

            # -------- Command listening --------
            record_audio()
            command = transcribe_audio().lower().strip()
            print("Command:", command)

            # Fallback if command empty
            if not command:
                command = text

            # Remove assistant name from command
            command = command.replace(ASSISTANT_NAME, "").strip()

            # Go back to sleep
            if any(word in command for word in ["bye", "goodbye", "exit", "quit"]):
                speak("Okay, going to sleep.")
                active = False
                continue

            # Detect intent
            intent, params = detect_intent(command)

            if intent == "get_time":
                response = actions.get_time()

            elif intent == "open_website":
                response = actions.open_website(params[0])

            elif intent == "create_note":
                response = actions.create_note(params[0])

            elif intent == "tell_joke":
                response = actions.tell_joke()

            elif intent == "tell_quote":
                response = actions.tell_quote()

            elif intent == "assistant_name":
                response = f"My name is {ASSISTANT_NAME.capitalize()}."

            elif intent == "greeting":
                response = "Hello! How can I help you?"

            else:
                response = "Sorry, I did not understand that."

            print("Assistant:", response)
            speak(response)

    except KeyboardInterrupt:
        print("\nAssistant stopped manually.")

if __name__ == "__main__":
    run()

