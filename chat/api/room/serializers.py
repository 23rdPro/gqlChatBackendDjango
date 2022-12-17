from rest_framework import serializers
from django.contrib.auth import get_user_model
from notifications.models import Notification
from chat.models import Room, Message

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("sender", "receiver", )  # message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("message",)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("actor", "recipient", "verb")
