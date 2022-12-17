import notifications.urls
from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView
# from chat.api.views import GQLView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("chat.urls")),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    re_path('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]
