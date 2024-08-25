from celery import shared_task
import os
import requests
from urllib.parse import urlparse

@shared_task
def transcribe(clip):
    input_data = {'audio': clip.file.url}

    response = requests.put(
        os.getenv('WHISPER_URL'),
        headers={'Content-Type': 'application/json'},
        json={'input': input_data}
    )

    results = response.json()
    clip.update(text=results['output']['transcription'])