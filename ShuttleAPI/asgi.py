"""
ASGI config for ShuttleAPI project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ShuttleAPI.settings')
import os

async def application(scope, receive, send):
    if scope['type'] == 'http':
        await handle_async(scope, receive, send)
    elif scope['type'] == 'websocket':
        await handle_websocket(scope, receive, send)
    else:
        await handle_async(scope, receive, send)

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
import location.routing  # Replace with your app's routing

application = ProtocolTypeRouter({
  'http': handle_async,
  'websocket': URLRouter(location.routing.websocket_urlpatterns),
})

