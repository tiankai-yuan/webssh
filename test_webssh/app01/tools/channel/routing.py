from django.urls import path
from app01.tools.channel import websocket

websocket_urlpatterns = [
    path('webssh/', websocket.WebSSH),
]