import sounddevice as sd
import numpy as np
import socket
from asr import transcribe_audio
from recorder import record_audio
from tts import speak


def check_microphone():
    try:
        duration = 1
        fs = 44100
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        volume = np.linalg.norm(audio)
        if volume > 0.01:
            return True, "Microphone is working."
        else:
            return False, "Microphone is not detecting sound."
    except Exception:
        return False, "Microphone check failed."


def check_speaker():
    try:
        speak("Testing speaker.")
        return True, "Speaker is working."
    except Exception:
        return False, "Speaker test failed."


def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True, "Internet connection is active."
    except Exception:
        return False, "No internet connection."


def check_asr():
    try:
        record_audio(duration=2)
        text = transcribe_audio()
        if text:
            return True, "Speech recognition is responding."
        else:
            return False, "Speech recognition did not return text."
    except Exception:
        return False, "Speech recognition check failed."


def run_diagnostics():
    results = []

    mic_ok, mic_msg = check_microphone()
    results.append(mic_msg)

    speaker_ok, speaker_msg = check_speaker()
    results.append(speaker_msg)

    net_ok, net_msg = check_internet()
    results.append(net_msg)

    asr_ok, asr_msg = check_asr()
    results.append(asr_msg)

    all_ok = mic_ok and speaker_ok and net_ok and asr_ok

    return results, all_ok

