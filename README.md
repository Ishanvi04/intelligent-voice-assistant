# Lana — Intelligent Voice Assistant 🎙️

## ▶️ Run Locally in 30 Seconds

```bash
git clone https://github.com/Ishanvi04/intelligent-voice-assistant.git
cd intelligent-voice-assistant
pip install -r requirements.txt
python run_lana.py
```


Overview

Lana is a Python-based voice assistant that listens for a wake word, understands spoken commands, executes actions, and responds using speech.

The project is built with a modular architecture, making it easy to maintain and extend while demonstrating real-time voice interaction.



Key Features

- Wake-word based activation (“Lana”)

- Speech-to-text and text-to-speech pipeline

-Intent-based command handling

-Local execution for common tasks

-AI-based response support through a clean interface

-Stops listening when the user says “bye”


Architecture (Brief)

Audio Input: Records short audio clips from the microphone

ASR: Converts speech into text

Intent Detection: Determines the user’s request

Actions: Handles timers, jokes, system commands, etc.

LLM Interface: Answers open-ended questions

TTS: Speaks responses clearly without overlap

Run:
python run_lana.py


Say “Lana” to wake the assistant and “bye” to stop.
