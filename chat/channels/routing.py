from django.urls import re_path

from chat.channels import consumer

websocket_urlpatterns = [
    # re_path(r"ws/(?P<room_name>\w+)/$", consumer.ChatConsumer.as_asgi()),
    # re_path(r"^(?P<room_id>\w+)/$", consumer.ChatConsumer.as_asgi()),
    re_path(r"^ws/rooms/(?P<room_id>[A-Za-z0-9_-]+)/$", consumer.ChatConsumer.as_asgi()),

]
