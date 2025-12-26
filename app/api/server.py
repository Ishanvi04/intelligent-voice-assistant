from fastapi import FastAPI
import threading

from app.main import run

app = FastAPI()

lana_thread = None
running = False


@app.post("/start")
def start_lana():
    global lana_thread, running

    if running:
        return {"status": "already_running"}

    running = True
    lana_thread = threading.Thread(target=run, daemon=True)
    lana_thread.start()

    return {"status": "started"}


@app.post("/stop")
def stop_lana():
    global running
    running = False
    return {"status": "stopping"}

