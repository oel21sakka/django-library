import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BookAvailabilityConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract book_id from the query string or URL route
        self.book_id = self.scope['url_route']['kwargs']['book_id']
        self.book_group_name = f"book_availability_{self.book_id}"

        # Join the book-specific group
        await self.channel_layer.group_add(
            self.book_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the book-specific group
        await self.channel_layer.group_discard(
            self.book_group_name,
            self.channel_name
        )

    async def book_available(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
