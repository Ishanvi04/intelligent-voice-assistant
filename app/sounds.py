import simpleaudio as sa
import os

BASE_DIR = os.path.dirname(__file__)

def _play(file):
    try:
        wave = sa.WaveObject.from_wave_file(file)
        wave.play()
    except Exception:
        # Fail silently (never crash Lana)
        pass

def play_start_sound():
    _play(os.path.join(BASE_DIR, "start.wav"))

def play_stop_sound():
    _play(os.path.join(BASE_DIR, "stop.wav"))

