import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import sys
import threading


def _mic_waveform(duration, fs):
    """
    Live mic waveform visualizer in terminal
    """
    def callback(indata, frames, time, status):
        # Flatten audio and normalize
        data = indata[:, 0]
        data = data / np.max(np.abs(data) + 1e-6)

        # Downsample for terminal width
        step = max(1, len(data) // 30)
        sampled = data[::step][:30]

        # Map amplitude to waveform chars
        waveform = ""
        for x in sampled:
            if x > 0.6:
                waveform += "^"
            elif x > 0.3:
                waveform += "~"
            elif x > 0.1:
                waveform += "-"
            elif x < -0.6:
                waveform += "v"
            elif x < -0.3:
                waveform += "~"
            elif x < -0.1:
                waveform += "-"
            else:
                waveform += " "

        sys.stdout.write(f"\r🎙  {waveform}")
        sys.stdout.flush()

    with sd.InputStream(callback=callback, samplerate=fs, channels=1):
        sd.sleep(int(duration * 1000))

    sys.stdout.write("\r🎙  Recording finished.              \n")
    sys.stdout.flush()


def record_audio(filename="samples/output.wav", duration=5, fs=44100):
    print(f"Recording for {duration} seconds...")

    # Start waveform visualizer in parallel
    visual_thread = threading.Thread(
        target=_mic_waveform,
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

