from celery import shared_task
import os
import requests

from clips.models import Clip

@shared_task
def transcribe(id):
    clip = Clip.objects.get(id=id)

    results = requests.put(
        os.getenv('WHISPER_URL'),
        headers={'Content-Type': 'application/json'},
        json={'input': {'audio': clip.file.url}}
    ).json()

    clip.text = results['output']['transcription']
    clip.save()
