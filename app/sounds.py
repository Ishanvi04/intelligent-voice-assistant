import simpleaudio as sa
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOUND_DIR = os.path.join(BASE_DIR, "sounds")

def play_start_sound():
    wave = sa.WaveObject.from_wave_file(
        os.path.join(SOUND_DIR, "start.wav")
    )
    wave.play()

def play_stop_sound():
    wave = sa.WaveObject.from_wave_file(
        os.path.join(SOUND_DIR, "stop.wav")
    )
    wave.play()


