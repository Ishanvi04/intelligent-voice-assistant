import urllib.parse
import time
import datetime
import webbrowser
import random
import subprocess
import datetime

def get_date():
    today = datetime.date.today()
    return today.strftime("Today is %A, %B %d, %Y.")
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

def open_and_search(command):
    command = command.lower()

    if "youtube" in command:
        site = "https://www.youtube.com"
        search_base = "https://www.youtube.com/results?search_query="
    elif "google" in command:
        site = "https://www.google.com"
        search_base = "https://www.google.com/search?q="
    else:
        return "Sorry, I don't know where to search."

    # Extract search query
    if "search" in command:
        query = command.split("search", 1)[1].strip()
        if not query:
            return "What should I search for?"

        webbrowser.open(site)
        time.sleep(1)
        webbrowser.open(search_base + urllib.parse.quote(query))
        return f"Searching {query}."

    return "Sorry, I couldn't complete that."
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

