import json
from django.shortcuts import render, reverse, redirect
from asgiref.sync import async_to_sync, sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponseForbidden,
    JsonResponse,
    HttpResponseBadRequest
)
from django.shortcuts import redirect, get_object_or_404

from ..models import Room


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


# @login_required
def online(request):
    user = get_user_model()
    friends = user.objects.exclude(pk=request.user.pk)
    context = {'friends': friends}
    return render(request, 'chat/index.html', context)


def chat_room(request, room_id):
    room = Room.objects.filter(id=room_id).get()
    if request.user not in (room.sender, room.receiver):
        raise HttpResponseForbidden
    return render(request, 'chat/room.html', {"room_id": room_id})


def create_room(request):
    if is_ajax(request):  # todo redirect in ajax
        if request.method == "POST":
            user = get_user_model()
            data = json.load(request)
            sender = get_object_or_404(user, username=data.get('sender'))
            receiver = get_object_or_404(user, username=data.get('receiver'))
            room, _ = Room.objects.get_or_create(
                sender=sender, receiver=receiver)
            return JsonResponse({"url": reverse('room', args=(room.id,))})
        return JsonResponse({"status": "Invalid request"}, status=400)
    return HttpResponseBadRequest("Invalid request")
