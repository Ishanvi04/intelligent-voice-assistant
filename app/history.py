# app/history.py

MAX_HISTORY = 10

command_history = []  # list of dicts: {"user": "", "lana": ""}

def add_to_history(user_text, lana_text):
    command_history.append({
        "user": user_text,
        "lana": lana_text
    })

    # Keep only last N commands
    if len(command_history) > MAX_HISTORY:
        command_history.pop(0)

def get_full_history():
    if not command_history:
        return "You haven't said anything yet."

    lines = []
    for i, item in enumerate(command_history, 1):
        lines.append(
            f"{i}. You said: {item['user']} | I replied: {item['lana']}"
        )

    return "\n".join(lines)

def get_last_command():
    if not command_history:
        return "No previous commands found."

    last = command_history[-1]
    return f"You said: {last['user']} and I replied: {last['lana']}"

