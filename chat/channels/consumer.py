import json
from asgiref.sync import async_to_sync
from channels.consumer import AsyncConsumer
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from notifications.signals import notify
from chat.models import Message, Room


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.room_group_name = None
        self.room_name = None

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )
        await self.add_message(message)
        id = self.scope["url_route"]["kwargs"]["room_id"]
        room = Room.objects.get(id=id)

        notify.send(
            room.sender,
            recipient=room.receiver,
            verb="you have unread message(s)")

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def add_message(self, message):
        msg = Message.objects.create(message=message)
        id = self.scope["url_route"]["kwargs"]["room_id"]
        Room.objects.get(id=id).message.add(msg)
        return


# class ChatConsumer(WebsocketConsumer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(args, kwargs)
#         self.room_group_name = None
#         self.room_name = None
#
#     def connect(self):
#         print("__---____--:", self.scope["user"])
#         self.room_name = self.scope["url_route"]["kwargs"]["room_id"]
#         self.room_group_name = "chat_%s" % self.room_name
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name, self.channel_name
#         )
#         self.accept()
#
#     def disconnect(self, close_code):
#         # pass
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name, self.channel_name
#         )
#
#     def receive(self, text_data=None, bytes_data=None):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name, {"type": "chat_message", "message": message}
#         )
#
#         # self.send(text_data=json.dumps({"message": message}))
#
#     def chat_message(self, event):
#         message = event["message"]
#
#         # Send message to WebSocket
#         self.send(text_data=json.dumps({"message": message}))
