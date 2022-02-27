from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/camera', consumers.CameraConsumer.as_asgi()),
]
