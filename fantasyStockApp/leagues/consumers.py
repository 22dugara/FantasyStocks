import json
from channels.generic.websocket import AsyncWebsocketConsumer
import re

class LeagueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.league_name = self.scope['url_route']['kwargs']['league_name']
        self.league_group_name = f'league_{re.sub(r"[^a-zA-Z0-9_-]", "_", self.league_name)}'

        await self.channel_layer.group_add(
            self.league_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.league_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        await self.channel_layer.group_send(
            self.league_group_name,
            {
                'type': 'league_message',
                'message': message
            }
        )

    async def league_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
