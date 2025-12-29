import sounddevice as sd
import numpy as np

WAKE_WORDS = ["hey lana", "lana"]

def listen_for_wake():
    print("🎙️ Listening for wake word...")
    duration = 3
    fs = 16000

    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    audio = np.squeeze(audio)
    energy = np.mean(np.abs(audio))

    if energy > 0.01:
        print("⚡ Audio detected (simulated wake)")
        return True

    return False

