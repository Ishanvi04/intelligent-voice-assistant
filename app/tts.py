import subprocess

def speak(text):
    try:
        subprocess.Popen(
            ["say", "-v", "Samantha", "-r", "170", text],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print("[TTS ERROR]", e)

