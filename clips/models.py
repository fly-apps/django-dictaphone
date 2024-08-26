from django.db import models

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class Clip(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField(null=True)
    mime = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def timestamp(self):
        return self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    
    def notify(self):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('notify', {
            'type': 'notify',
            'message': self.timestamp()
        })
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.notify()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.notify()