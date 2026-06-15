import os
import requests
import traceback
from dotenv import load_dotenv

load_dotenv()

def transcribe_audio(path):
    if not path or not os.path.exists(path):
        print(f"File path does not exist: {path}")
        return "No response captured."
        
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        err_msg = "Error: GROQ_API_KEY is not set."
        print(err_msg)
        raise ValueError(err_msg)
        
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    filename = os.path.basename(path)
    
    try:
        print(f"Sending audio file {path} to Groq Whisper API...")
        with open(path, "rb") as f:
            files = {
                "file": (filename, f, "audio/webm")
            }
            data = {
                "model": "whisper-large-v3-turbo",
                "temperature": "0.0",
                "response_format": "json"
            }
            response = requests.post(url, headers=headers, files=files, data=data, timeout=30)
            
        if response.status_code != 200:
            err_details = f"Groq API returned status code {response.status_code}: {response.text}"
            print(f"Groq API error: {err_details}")
            raise Exception(err_details)
            
        res_json = response.json()
        text = res_json.get("text", "").strip()
        print(f"Groq Whisper transcription success: '{text}'")
        return text
    except Exception as e:
        print("Backend transcription error with stack trace:")
        traceback.print_exc()
        raise e

def transcribe_numpy(audio_array):
    print("Warning: transcribe_numpy is deprecated and not supported in Groq-based transcription.")
    return ""
