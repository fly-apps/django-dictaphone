# notify/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class NotifyConsumer(WebsocketConsumer):
    def connect(self):
        # Join channel
        async_to_sync(self.channel_layer.group_add)(
            'notify', self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave channel
        async_to_sync(self.channel_layer.group_discard)(
            'notify', self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))

    def notify(self, event):
        message = event["message"]

        self.send(text_data=json.dumps({"message": message}))
