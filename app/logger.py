from datetime import datetime

LOG_FILE = "logs/conversation.log"

def log_message(speaker, message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] {speaker}: {message}\n"

    with open(LOG_FILE, "a") as f:
        f.write(line)

