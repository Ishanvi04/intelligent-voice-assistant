import threading
import time
from app.sounds import play_alarm_sound
from app.tts import speak

_active_timers = []

def timer_thread(seconds):
    if seconds is None:
        return
    try:
        seconds = int(seconds)
    except Exception:
        return

    time.sleep(seconds)
    play_alarm_sound()
    speak("Time is up.")

def start_timer(seconds):
    if seconds is None:
        return "I couldn't understand the timer duration."

    try:
        seconds = int(seconds)
    except Exception:
        return "Please say the timer duration clearly."

    thread = threading.Thread(
        target=timer_thread,
        args=(seconds,),
        daemon=True
    )
    thread.start()

    _active_timers.append(thread)
    return f"Timer set for {seconds} seconds."

def cancel_timers():
    _active_timers.clear()
    return "All timers cancelled."

