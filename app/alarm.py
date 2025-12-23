import threading
import time
import datetime
import re

alarms = []
alarm_thread_running = False


def parse_time(text):
    text = text.lower()

    # 6:30 or 6.30
    match = re.search(r'(\d{1,2})[:.](\d{2})', text)
    if match:
        return int(match.group(1)), int(match.group(2))

    # 630 or 0730
    match = re.search(r'\b(\d{3,4})\b', text)
    if match:
        num = match.group(1)
        if len(num) == 3:
            return int(num[0]), int(num[1:])
        else:
            return int(num[:2]), int(num[2:])

    # 2 am / 2 pm
    match = re.search(r'(\d{1,2})\s*(a\.?m\.?|p\.?m\.?)', text)
    if match:
        hour = int(match.group(1))
        if "p" in match.group(2) and hour != 12:
            hour += 12
        if "a" in match.group(2) and hour == 12:
            hour = 0
        return hour, 0

    return None


def add_alarm(hour, minute):
    alarms.append((hour, minute))
    return f"Alarm set for {hour:02d}:{minute:02d}."


def cancel_alarms():
    alarms.clear()
    return "All alarms have been cancelled."


def _alarm_loop(speak):
    global alarm_thread_running
    alarm_thread_running = True

    while True:
        now = datetime.datetime.now()
        current = (now.hour, now.minute)

        if current in alarms:
            alarms.remove(current)
            speak("⏰ Alarm ringing!")
            time.sleep(60)

        time.sleep(5)


def start_alarm_thread(speak):
    global alarm_thread_running
    if alarm_thread_running:
        return

    thread = threading.Thread(
        target=_alarm_loop,
        args=(speak,),
        daemon=True
    )
    thread.start()

