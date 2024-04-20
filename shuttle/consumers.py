import json

from asgi_django.websocket import AsyncWebsocketConsumer
from channels.db_manager.django.ops import create_connection
from django.contrib.gis.geos import Point

from .models import LocationUpdate


class LocationUpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.device_id = self.scope['url_route']['kwargs']['device_id']
        self.location_group_name = f'locations_{self.device_id}'

        # Connect to the database
        await create_connection()

        # Join the group for this device
        await self.channel_layer.group_add(self.location_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(self.location_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Handle potential messages from the client (optional)

    async def location_update(self, event):
        location_update = event['location_update']
        # Process or visualize the received location data
        await self.send(text_data=json.dumps(location_update))
