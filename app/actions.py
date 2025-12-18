import datetime
import webbrowser
import random

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

