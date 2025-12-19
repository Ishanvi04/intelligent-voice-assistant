import sounddevice as sd
import numpy as np
import sys

def mic_visualizer(duration=5, samplerate=44100):
    """
    Shows live mic activity in terminal while recording
    """
    def callback(indata, frames, time, status):
        volume = np.linalg.norm(indata) * 10
        bars = int(min(volume, 30))
        meter = "█" * bars
        sys.stdout.write(f"\r🎙 Listening {meter:<30}")
        sys.stdout.flush()

    with sd.InputStream(callback=callback, samplerate=samplerate):
        sd.sleep(int(duration * 1000))

    sys.stdout.write("\r🎙 Recording finished.            \n")

