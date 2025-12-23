# app/context.py

last_intent = None
pending_question = None
pending_intent = None
# app/context.py
pending_intent = None
pending_data = None

def reset():
    global pending_intent, pending_data
    pending_intent = None
    pending_data = None

