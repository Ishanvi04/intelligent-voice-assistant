from recorder import record_audio
from asr import transcribe_audio
from intent import detect_intent
import actions

def run():
    record_audio()
    text = transcribe_audio()

    print("User:", text)

    intent, params = detect_intent(text)
    print("Intent:", intent)

    if intent == "get_time":
        response = actions.get_time()
    elif intent == "open_website":
        response = actions.open_website(params[0])
    elif intent == "create_note":
        response = actions.create_note(params[0])
    elif intent == "tell_joke":
        response = actions.tell_joke()
    else:
        response = "Sorry, I didn't understand."

    print("Assistant:", response)

if __name__ == "__main__":
    run()
