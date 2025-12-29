import sounddevice as sd
from scipy.io.wavfile import write
import time

def record_audio(
    filename="samples/output.wav",
    duration=5,
    fs=44100
):
    """
    Safe, single-stream recorder for macOS CoreAudio
    """

    try:
        print(f"Recording for {duration} seconds...")

        # Small delay to ensure mic is free
        time.sleep(0.4)

        audio = sd.rec(
            int(duration * fs),
            samplerate=fs,
            channels=1,
            dtype="float32"
        )

        sd.wait()  # BLOCK until done

        write(filename, fs, audio)
        print(f"Saved recording to {filename}")

        # Let CoreAudio fully release mic
        time.sleep(0.4)

    except Exception as e:
        print("[MIC ERROR]", e)
        time.sleep(1.0)

