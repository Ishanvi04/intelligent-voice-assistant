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
def play_alarm_sound():
    try:
        wave = sa.WaveObject.from_wave_file("app/sounds/alarm.wav")
        wave.play()
    except Exception:
        print("⚠️ Alarm sound failed")

