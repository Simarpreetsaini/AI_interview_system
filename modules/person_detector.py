import os
import torch

pipeline = None

def load_pyannote_pipeline():
    global pipeline
    if pipeline is not None:
        return pipeline
    
    # Check if HF_TOKEN is available (pyannote requires token auth)
    token = os.getenv("HF_TOKEN")
    if not token:
        print("WARNING: HF_TOKEN environment variable not set. pyannote.audio will fallback to offline/mock detection.")
        pipeline = "fallback"
        return pipeline
        
    try:
        from pyannote.audio import Pipeline
        print("Loading pyannote.audio speaker diarization pipeline...")
        # Load the latest speaker diarization pipeline
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=token
        )
        # Check and send to GPU if available for maximum speed
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        pipeline.to(device)
        print("pyannote.audio speaker diarization pipeline loaded successfully.")
    except Exception as e:
        print(f"Failed to load pyannote.audio pipeline: {e}. Falling back...")
        pipeline = "fallback"
    return pipeline

def detect_multiple_speakers(audio_path):
    """
    Analyzes an audio file and returns True if multiple speakers are detected.
    Returns False if only 0/1 speakers are detected, or on error/fallback.
    """
    pipe = load_pyannote_pipeline()
    if pipe == "fallback" or pipe is None:
        return False
        
    try:
        # Run diarization on the audio file
        diarization = pipe(audio_path)
        
        # Collect distinct speaker labels detected in the recording
        speakers = set()
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            speakers.add(speaker)
            
        print(f"pyannote.audio: Detected speaker IDs: {speakers}")
        return len(speakers) > 1
    except Exception as e:
        print(f"Error running pyannote.audio diarization check: {e}")
        return False
