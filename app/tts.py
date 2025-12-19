import pyttsx3

engine = pyttsx3.init()

# Get available voices
voices = engine.getProperty("voices")

# Try to select a female voice
female_voice = None
for voice in voices:
    if "female" in voice.name.lower() or "samantha" in voice.name.lower():
        female_voice = voice.id
        break

# Fallback
engine.setProperty("voice", female_voice if female_voice else voices[0].id)

# Tune voice
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

def speak(text):
    engine.say(text)
    engine.runAndWait()

