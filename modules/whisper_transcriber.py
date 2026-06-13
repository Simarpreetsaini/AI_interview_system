
import os

model = None

def load_model():
    global model
    if model is not None:
        return
        
    try:
        from faster_whisper import WhisperModel
        print("Loading Faster-Whisper base model on CPU...")
        # Running on CPU, using int8 compute type for speed
        model = WhisperModel("base", device="cpu", compute_type="int8")
        model.type = "faster"
    except Exception as e:
        print(f"Faster-Whisper import/load failed: {e}. Falling back to standard Whisper...")
        try:
            import whisper
            model = whisper.load_model("base")
            model.type = "standard"
        except Exception as e2:
            print(f"Standard Whisper load failed: {e2}.")
            model = "fallback"

def transcribe_audio(path):
    load_model()
    if model == "fallback":
        return "[Transcription Fallback: Whisper/Faster-Whisper not loaded]"
        
    if getattr(model, "type", None) == "faster":
        # segments is a generator, transcribing on-the-fly
        segments, info = model.transcribe(path, beam_size=5)
        text = " ".join([segment.text for segment in segments])
        return text.strip()
    else:
        # Standard whisper fallback
        result = model.transcribe(path)
        return result["text"].strip()
