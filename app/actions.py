import datetime
import webbrowser
import random
import subprocess

def get_battery():
    try:
        output = subprocess.check_output(
            ["pmset", "-g", "batt"]
        ).decode()

        # Example output:
        # 'Now drawing from 'Battery Power'\n -InternalBattery-0 (id=1234567) 85%; discharging; 3:45 remaining\n'

        percent = output.split("\t")[-1].split(";")[0]
        return f"Your battery is at {percent}."

    except Exception:
        return "Sorry, I couldn't check the battery level."

def get_time():
    now = datetime.datetime.now()
    return f"The current time is {now.strftime('%I:%M %p')}"

def open_website(site):
    if not site.startswith("http"):
        site = "https://" + site
    webbrowser.open(site)
    return f"Opening {site}"

def create_note(text):
    with open("notes.txt", "a") as f:
        f.write(text + "\n")
    return "Note saved."

def tell_joke():
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "I told my computer I needed a break. It froze.",
        "Why was the Python developer sad? Because he had too many bugs."
    ]
    return random.choice(jokes)

def tell_quote():
    quotes = [
        "Believe in yourself and all that you are.",
        "Success is not final, failure is not fatal.",
        "Discipline is the bridge between goals and accomplishment.",
        "Dream big. Start small. Act now.",
        "Your limitation is only your imagination."
    ]
    return random.choice(quotes)

