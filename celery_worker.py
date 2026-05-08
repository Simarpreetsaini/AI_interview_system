import os
from celery import Celery
from modules.whisper_transcriber import transcribe_audio

REDIS_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

@celery_app.task
def process_audio_transcription(file_path):
    # This will run the Whisper transcription in the background worker
    try:
        text = transcribe_audio(file_path)
        return {"success": True, "text": text}
    except Exception as e:
        return {"success": False, "error": str(e)}
