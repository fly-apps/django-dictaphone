# chat/routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("websocket", consumers.NotifyConsumer.as_asgi()),
]