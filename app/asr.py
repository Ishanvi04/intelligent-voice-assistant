import whisper

model = whisper.load_model("base")

def transcribe_audio(filepath="samples/output.wav"):
    result = model.transcribe(filepath)
    return result["text"]

if __name__ == "__main__":
    print(transcribe_audio())
