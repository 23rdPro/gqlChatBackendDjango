from graphene_django.views import GraphQLView
from django.contrib.auth.mixins import LoginRequiredMixin


class GQLView(LoginRequiredMixin, GraphQLView):
    pass
