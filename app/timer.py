import time
import threading
from sounds import play_alarm_sound

active_timers = []

def start_timer(seconds):
    def timer_thread():
        time.sleep(seconds)
        play_alarm_sound()

    t = threading.Thread(target=timer_thread, daemon=True)
    t.start()
    active_timers.append(t)

    return f"Timer set for {seconds} seconds."

def cancel_timers():
    active_timers.clear()
    return "All timers cancelled."

