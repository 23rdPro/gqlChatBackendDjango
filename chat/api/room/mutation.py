import uuid

import graphene
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import transaction
from chat.models import Room, Message
from .subscriptions import OnNewMessageSubscription
from ..types import RoomType, UserType

User = get_user_model()


class RoomInput(graphene.InputObjectType):
    sender = graphene.String()
    receiver = graphene.String()


class RoomMutation(graphene.Mutation):
    class Arguments:
        fields = RoomInput(required=True)

    room = graphene.Field(RoomType)
    sender = graphene.Field(UserType)
    receiver = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, fields=None):
        sender = get_object_or_404(
            User,
            username=fields.sender
        )
        receiver = get_object_or_404(
            User,
            username=fields.receiver
        )
        room, _ = Room.objects.get_or_create(
            sender=sender, receiver=receiver)
        return RoomMutation(
            room=room,
            sender=sender,
            receiver=receiver
        )


class SendMessageMutation(graphene.Mutation):
    sent = graphene.Boolean()

    class Arguments:
        room = graphene.String()
        message = graphene.String()

    @staticmethod
    def mutate(root, info, **kwargs):
        uid = uuid.UUID(kwargs.get('room_id'))
        assert Room.objects.filter(id=uid).exists(), \
            "Room is expected to have gone through mutation"
        msg = kwargs.get('message')
        room = Room.objects.get(id=uid)

        with transaction.atomic(durable=True):
            instance = Message.objects.create(message=msg)
            room.message.add(instance)

        OnNewMessageSubscription.new_chat_message(
            room_id=room.id,
            sender=room.sender.username,
            receiver=room.receiver.username,
            message=room.message.message
        )
        return SendMessageMutation(sent=True)
