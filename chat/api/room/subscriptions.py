import asyncio
import uuid

import graphene
# import channels_graphql_ws
from django.contrib.auth import get_user_model
from notifications.signals import notify
from chat.models import Room

User = get_user_model()


# class OnNewMessageSubscription(channels_graphql_ws.Subscription):
#     room_id = graphene.String()
#     sender = graphene.String()
#     receiver = graphene.String()
#     message = graphene.String()
#
#     class Arguments:
#         room_id = graphene.String(required=True)
#         # message = graphene.String(required=True)
#
#     @staticmethod
#     def subscribe(root, info, **kwargs):
#         uid = uuid.UUID(kwargs.get('room_id'))
#         assert Room.objects.filter(id=uid).exists(), \
#             "Room is expected to have gone through mutation"
#         room = Room.objects.get(id=uid)
#         return room
#
#     @staticmethod
#     def publish(root, info, **kwargs):
#         uid = uuid.UUID(kwargs.get('room_id'))
#         room = Room.objects.filter(id=uid).get()
#         sender, receiver, message, room_id = (
#             room.sender.username,
#             room.receiver.username,
#             room.message.message,
#             room.id
#         )
#         if info.context.user == sender.username:
#             return OnNewMessageSubscription.SKIP
#         return OnNewMessageSubscription(
#             room_id=room_id,
#             sender=sender,
#             receiver=receiver,
#             message=message
#         )
#
#     @classmethod
#     async def new_chat_message(cls, info, **kwargs):
#         uid = uuid.UUID(kwargs.get('room_id'))
#         assert Room.objects.filter(id=uid).exists(), \
#             "Room is expected to have gone through mutation"
#         room = Room.objects.get(id=uid)
#         payload = {
#             "room_id": room.id,
#             "sender": room.sender.username,
#             "receiver": room.receiver.username,
#             "message": room.message.message
#         }
#         await cls.broadcast_async(group=payload["room_id"], payload=payload)
#         await asyncio.sleep(1)
#         await notify.send(
#             payload["sender"],
#             recipient=payload["receiver"],
#             verb="you have unread message(s)"
#         )
