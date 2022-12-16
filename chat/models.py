from uuid import uuid4
from django.db import models
from django.conf import settings
from django.utils.timezone import now


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sender"
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="receiver"
    )
    on = models.DateTimeField(default=now)
    message = models.ManyToManyField('Message', blank=True)
    objects = models.Manager()


class Message(models.Model):
    message = models.TextField(max_length=244)
    objects = models.Manager()

    def __str__(self):
        return self.message
