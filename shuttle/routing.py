from django.urls import path

from .consumers import LocationUpdateConsumer

websocket_urlpatterns = [
    path('locations/<str:device_id>/', LocationUpdateConsumer.as_asgi()),
]
