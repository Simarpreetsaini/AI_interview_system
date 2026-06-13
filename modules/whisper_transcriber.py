
import os
import subprocess
import numpy as np

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

def load_audio_as_numpy(path, sample_rate=16000):
    try:
        command = [
            'ffmpeg',
            '-y',
            '-i', path,
            '-f', 'f32le',
            '-acodec', 'pcm_f32le',
            '-ar', str(sample_rate),
            '-ac', '1',
            '-'
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        stdout, _ = process.communicate()
        if process.returncode == 0:
            return np.frombuffer(stdout, dtype=np.float32)
    except Exception as e:
        print(f"Error loading audio via ffmpeg for VAD: {e}")
    return None

def transcribe_audio(path):
    # Run Silero VAD pre-screening check to filter out non-speech audios (saves CPU/RAM)
    try:
        from modules.vad_detector import is_speaking
        audio_data = load_audio_as_numpy(path)
        if audio_data is not None and len(audio_data) > 0:
            # If no speech detected by Silero VAD, bypass transcription entirely
            if not is_speaking(audio_data, sample_rate=16000, threshold=0.4):
                print(f"Silero VAD: No speech detected in {path}. Skipping transcription.")
                return "No response captured."
    except Exception as vad_err:
        print(f"Silero VAD speech pre-screen failed: {vad_err}")

    # Skip loading whisper on low-resource environments (like Render Free tier) to prevent OOM/CPU crash
    is_low_mem = os.getenv("RENDER") == "true" or os.getenv("DISABLE_ML") == "1"
    if is_low_mem:
        print("INFO: Low memory/Render environment detected. Bypassing Whisper model loading to prevent OOM crash.")
        return "No response captured."

    load_model()
    if model == "fallback":
        return "[Transcription Fallback: Whisper/Faster-Whisper not loaded]"
        
    if getattr(model, "type", None) == "faster":
        # segments is a generator, transcribing on-the-fly with Silero VAD filter enabled
        segments, info = model.transcribe(path, beam_size=5, vad_filter=True)
        text = " ".join([segment.text for segment in segments])
        return text.strip()
    else:
        # Standard whisper fallback
        result = model.transcribe(path)
        return result["text"].strip()
