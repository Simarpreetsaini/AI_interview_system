import numpy as np
import torch
import os

_vad_model = None
_vad_utils = None

def init_vad():
    global _vad_model, _vad_utils
    if _vad_model is not None:
        return True
        
    try:
        # Load pre-trained Silero VAD model
        print("Loading Silero VAD model via torch.hub...")
        model, utils = torch.hub.load(
            repo_or_dir='snakers4/silero-vad',
            model='silero_vad',
            trust_repo=True,
            verbose=False
        )
        _vad_model = model
        _vad_utils = utils
        print("Silero VAD model loaded successfully.")
        return True
    except Exception as e:
        print(f"Silero VAD initialization failed: {e}. Falling back to simple energy-based VAD.")
        _vad_model = "fallback"
        return False

def is_speaking(audio_chunk, sample_rate=16000, threshold=0.5):
    """
    Detect if the audio chunk contains active speech.
    
    Parameters:
    - audio_chunk: 1D numpy array of float32 values (normalized between -1.0 and 1.0)
    - sample_rate: target sample rate, usually 16000
    - threshold: confidence threshold for speech probability
    
    Returns:
    - bool: True if speech is detected, False otherwise
    """
    init_vad()
    
    if _vad_model == "fallback" or _vad_model is None:
        # Energy-based VAD fallback (Root Mean Square amplitude check)
        # Standard threshold for normalized voice activity: ~0.02
        if len(audio_chunk) == 0:
            return False
        rms = np.sqrt(np.mean(np.square(audio_chunk)))
        return rms > 0.025
        
    try:
        # Convert numpy array to torch tensor
        tensor_chunk = torch.from_numpy(audio_chunk)
        
        # Silero VAD expects torch tensor of floats
        with torch.no_grad():
            speech_prob = _vad_model(tensor_chunk, sample_rate).item()
            
        return speech_prob >= threshold
    except Exception as e:
        # Log and fallback to energy check
        rms = np.sqrt(np.mean(np.square(audio_chunk))) if len(audio_chunk) > 0 else 0
        return rms > 0.025
