import subprocess
import time

is_speaking = False

def speak(text: str):
    global is_speaking
    if not text:
        return

    is_speaking = True
    try:
        subprocess.run(
            ["say", "-v", "Samantha", "-r", "170", text],
            check=False
        )
    finally:
        time.sleep(0.4)
        is_speaking = False

