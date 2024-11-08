import json

from channels.generic.websocket import AsyncWebsocketConsumer
import redis


client = redis.Redis(host="localhost", port=6379, db=0)


class AsyncConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        print("Connected .......")

        self.room_name = "test"
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))


class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Connecting .......")
        self.user_id = self.scope["user"].pk
        client.sadd("users", self.user_id)
        await self.channel_layer.group_add(f"user_{self.user_id}", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        client.srem("users", self.user_id)
        await self.channel_layer.group_discard(
            f"user_{self.user_id}", self.channel_name
        )

    async def receive(self, text_data):
        # text_data_json = json.loads(text_data)
        # message = text_data_json["message"]

        await self.channel_layer.group_send(
            f"user_{self.user_id}", {"type": "chat.message", "message": text_data}
        )

    async def chat_message(self, event):
        message = event["message"]

        await self.send(text_data=message)
