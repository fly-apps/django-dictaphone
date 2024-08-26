from celery import shared_task
import os
import requests
from urllib.parse import urlparse

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

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

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('notify', {
        'type': 'notify',
        'message': 'New transcription available'
    })