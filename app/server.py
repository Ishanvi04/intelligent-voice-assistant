import threading
from fastapi import FastAPI
from app.main import handle_voice_interaction

app = FastAPI()

assistant_thread = None
running = False

def assistant_loop():
    global running
    while running:
        handle_voice_interaction()

@app.post("/start")
def start_assistant():
    global assistant_thread, running

    if running:
        return {"status": "already running"}

    running = True
    assistant_thread = threading.Thread(
        target=assistant_loop,
        daemon=True
    )
    assistant_thread.start()

    return {"status": "started"}

@app.post("/stop")
def stop_assistant():
    global running
    running = False
    return {"status": "stopped"}


