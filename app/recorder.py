import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import sys
import threading


def _mic_visualizer(duration, fs):
    """
    Live mic activity indicator while recording
    """
    def callback(indata, frames, time, status):
        volume = np.linalg.norm(indata) * 10
        bars = min(int(volume), 30)
        meter = "█" * bars
        sys.stdout.write(f"\r🎙 Listening {meter:<30}")
        sys.stdout.flush()

    with sd.InputStream(callback=callback, samplerate=fs, channels=1):
        sd.sleep(int(duration * 1000))

    sys.stdout.write("\r🎙 Recording finished.            \n")
    sys.stdout.flush()


def record_audio(filename="samples/output.wav", duration=5, fs=44100):
    print(f"Recording for {duration} seconds...")

    # Start mic visualizer in parallel
    visual_thread = threading.Thread(
        target=_mic_visualizer,
        args=(duration, fs),
        daemon=True
    )
    visual_thread.start()

    # Record audio
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    visual_thread.join()

    write(filename, fs, audio)
    print(f"Saved recording to {filename}")


if __name__ == "__main__":
    record_audio()

