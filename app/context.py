# app/context.py

last_intent = None
pending_question = None
pending_intent = None

def reset():
    global pending_question, pending_intent
    pending_question = None
    pending_intent = None

