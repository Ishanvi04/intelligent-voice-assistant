import os
from playsound import playsound

BASE_DIR = os.path.dirname(__file__)

def play_start_sound():
    try:
        playsound(os.path.join(BASE_DIR, "start.wav"), block=False)
    except Exception:
        pass

def play_stop_sound():
    try:
        playsound(os.path.join(BASE_DIR, "stop.wav"), block=False)
    except Exception:
        pass

def play_alarm_sound():
    try:
        playsound(os.path.join(BASE_DIR, "alarm.wav"), block=False)
    except Exception:
        pass

