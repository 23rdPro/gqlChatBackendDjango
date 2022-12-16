import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path, re_path
from chat.api.consumer import ChatConsumer

from chat.channels.routing import websocket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'graphql_project.settings')

django_asgi_app = get_asgi_application()
# application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(
            [
                path("graphql/", ChatConsumer.as_asgi()),
                # re_path(r"^ws/rooms/(?P<room_id>[A-Za-z0-9_-]+)/$", ChatConsumer.as_asgi()),
            ]
        ))
    ),
})

