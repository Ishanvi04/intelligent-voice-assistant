from playsound import playsound
import os

BASE_DIR = os.path.dirname(__file__)

def play_start_sound():
    try:
        playsound(os.path.join(BASE_DIR, "start.wav"))
    except Exception as e:
        print("[SOUND ERROR]", e)

def play_stop_sound():
    try:
        playsound(os.path.join(BASE_DIR, "stop.wav"))
    except Exception as e:
        print("[SOUND ERROR]", e)

def play_alarm_sound():
    """
    Used by timer when time is up
    """
    try:
        playsound(os.path.join(BASE_DIR, "stop.wav"))
    except Exception as e:
        print("[SOUND ERROR]", e)

