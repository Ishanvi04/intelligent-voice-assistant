from emotion import detect_emotion, get_emotion_response
import time
from recorder import record_audio
from asr import transcribe_audio
from intent import detect_intent
import actions
from tts import speak

ASSISTANT_NAME = "lana"
WAKE_WORDS = ["lana", "laana", "lanna", "lanaah"]
ACTIVE_TIMEOUT = 20        # seconds
SPEAK_COOLDOWN = 1.2       # seconds (prevents hearing itself)

def run():
    print(f"{ASSISTANT_NAME.capitalize()} is running. Say '{ASSISTANT_NAME}' to wake me up.")

    active = False
    last_active_time = 0

    try:
        while True:
            # -------- PASSIVE LISTENING --------
            record_audio()
            text = transcribe_audio().lower().strip()
            print("Heard:", text)

            # -------- EXIT ANYTIME --------
            if any(word in text for word in ["exit", "bye", "goodbye", "quit"]):
                speak("Goodbye. Shutting down.")
                print("Assistant stopped.")
                break

            # -------- SLEEP MODE --------
            if not active:
                if any(w in text for w in WAKE_WORDS):
                    active = True
                    last_active_time = time.time()
                    speak("Yes?")
                    time.sleep(SPEAK_COOLDOWN)
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
           
            emotion = detect_emotion(command)
            if emotion:
               response = get_emotion_response(emotion)
               print("Emotion detected:", emotion)
               speak(response)
               time.sleep(1)
               continue


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
                response = "Sorry, I didn't understand that."

            speak(response)
            print("Assistant:", response)

            time.sleep(SPEAK_COOLDOWN)
            last_active_time = time.time()

    except KeyboardInterrupt:
        print("\nAssistant stopped manually.")
        speak("Goodbye.")

if __name__ == "__main__":
    run()

