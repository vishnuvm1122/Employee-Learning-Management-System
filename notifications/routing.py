# notifications/routing.py
from django.urls import path
from .consumers import NotificationConsumer

websocket_urlpatterns = [
    # WebSocket route for real-time notifications
    path("ws/notifications/", NotificationConsumer.as_asgi()),
]