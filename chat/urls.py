from django.urls import path
from .channels import views as chl_view


urlpatterns = [
    path("", chl_view.online, name="online"),
    path("ws/rooms/<uuid:room_id>/", chl_view.chat_room, name="room"),
    path("create/room/", chl_view.create_room, name="create-room"),
]
