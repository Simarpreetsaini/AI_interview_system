
import os

model = None

def load_model():
    global model
    if model is not None:
        return
        
    # Use 'tiny' model on resource-constrained environments like Render to prevent OOM crashes
    is_low_mem = os.getenv("RENDER") == "true" or os.getenv("DISABLE_ML") == "1"
    model_size = "tiny" if is_low_mem else "base"
        
    try:
        from faster_whisper import WhisperModel
        print(f"Loading Faster-Whisper {model_size} model on CPU...")
        # Running on CPU, using int8 compute type for speed
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        model.type = "faster"
    except Exception as e:
        print(f"Faster-Whisper import/load failed: {e}. Falling back to standard Whisper...")
        try:
            import whisper
            model = whisper.load_model(model_size)
            model.type = "standard"
        except Exception as e2:
            print(f"Standard Whisper load failed: {e2}.")
            model = "fallback"

def transcribe_audio(path):
    # Skip loading whisper on low-resource environments (like Render Free tier) to prevent OOM/CPU crash
    is_low_mem = os.getenv("RENDER") == "true" or os.getenv("DISABLE_ML") == "1"
    if is_low_mem:
        print("INFO: Low memory/Render environment detected. Bypassing Whisper model loading to prevent OOM crash.")
        return "No response captured."

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
