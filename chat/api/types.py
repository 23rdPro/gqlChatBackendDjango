import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model
from notifications.models import Notification
from ..models import Room, Message
from graphene import relay

User = get_user_model()


class NotificationType(DjangoObjectType):
    class Meta:
        model = Notification
        fields = ('recipient', 'actor', 'verb')


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ("password", )
        interfaces = (relay.Node, )


class MessageType(DjangoObjectType):
    class Meta:
        model = Message
        fields = '__all__'


class RoomType(DjangoObjectType):
    class Meta:
        model = Room
        fields = ("id", "sender", "receiver", )

    messages = graphene.List(MessageType)

    def resolve_messages(self, info, **kwargs):
        return self.message.all()
