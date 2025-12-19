import whisper

# Load Whisper model once
model = whisper.load_model("base")

def transcribe_audio(filepath="samples/output.wav"):
    """
    Transcribes audio using Whisper.
    - Forces English
    - Avoids FP16 on CPU
    - Ignores silence / noise
    """

    result = model.transcribe(
        filepath,
        language="en",   # Force English
        fp16=False       # Required for CPU
    )

    text = result.get("text", "").strip()

    # Ignore silence / noise
    if len(text) < 2:
        return ""

    return text


# For quick testing: python app/asr.py
if __name__ == "__main__":
    print(transcribe_audio())

