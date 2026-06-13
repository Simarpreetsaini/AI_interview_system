
import os
import json
import wave
import subprocess
import tempfile
from vosk import Model, KaldiRecognizer

model = None

def load_model():
    global model
    if model is not None:
        return
        
    model_name = "vosk-model-small-en-us-0.15"
    try:
        print(f"Loading Vosk model '{model_name}'...")
        model = Model(model_name=model_name)
        print("Vosk model loaded successfully.")
    except Exception as e:
        print(f"Vosk model load failed: {e}. Trying local fallback if exists...")
        if os.path.exists(model_name):
            try:
                model = Model(model_name)
                print("Vosk model loaded from local path.")
            except Exception as e2:
                print(f"Local Vosk model load failed: {e2}")
                model = "fallback"
        else:
            print("Vosk model loading failed completely.")
            model = "fallback"

def transcribe_audio(path):
    if not path or not os.path.exists(path):
        print(f"File path does not exist: {path}")
        return "No response captured."

    load_model()
    if model == "fallback" or model is None:
        return "[Transcription Fallback: Vosk model not loaded]"
        
    # Look for local ffmpeg directory in the workspace (for Windows local setup)
    workspace_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    local_ffmpeg_dir = os.path.join(workspace_dir, "ffmpeg-2026-03-12-git-9dc44b43b2-essentials_build", "bin")
    ffmpeg_exe = os.path.join(local_ffmpeg_dir, "ffmpeg.exe")
    
    ffmpeg_cmd = "ffmpeg"
    if os.path.exists(ffmpeg_exe):
        ffmpeg_cmd = ffmpeg_exe
    
    # Convert input file (WebM/MP4 etc) to PCM WAV 16kHz Mono using FFmpeg
    wav_path = tempfile.mktemp(suffix=".wav")
    
    cmd = [
        ffmpeg_cmd, "-y", "-i", path,
        "-ar", "16000",
        "-ac", "1",
        "-acodec", "pcm_s16le",
        wav_path
    ]
    
    try:
        print(f"Converting {path} to {wav_path} via FFmpeg using command: {ffmpeg_cmd}...")
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except Exception as e:
        print(f"FFmpeg audio conversion failed: {e}")
        if os.path.exists(wav_path):
            try:
                os.remove(wav_path)
            except:
                pass
        return "Audio conversion error."
        
    try:
        wf = wave.open(wav_path, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            print("Audio file must be WAV format mono PCM.")
            wf.close()
            return "Invalid audio format."
            
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(False)
        
        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res_obj = json.loads(rec.Result())
                results.append(res_obj.get("text", ""))
                
        res_obj = json.loads(rec.FinalResult())
        results.append(res_obj.get("text", ""))
        
        wf.close()
        text = " ".join([r for r in results if r]).strip()
        
        if not text:
            return "No response captured."
        return text
    except Exception as e:
        print(f"Vosk transcription failed: {e}")
        return "Transcription error."
    finally:
        if os.path.exists(wav_path):
            try:
                os.remove(wav_path)
            except Exception as e:
                print(f"Error removing temporary WAV file: {e}")
