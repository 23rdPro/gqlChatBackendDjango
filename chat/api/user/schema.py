import graphene
from django.contrib.auth import get_user_model
from ..types import UserType
from .mutations import (
    RegisterUserMutation,
    LogoutUserMutation
)

User = get_user_model()


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType)

    @staticmethod
    def resolve_user(root, info, **kwargs):
        assert info.context.user.is_authenticated, \
            "User must be authenticated"
        return info.context.user

    @staticmethod
    def resolve_users(self, info, **kwargs):
        assert info.context.user.is_authenticated, \
            "User must be authenticated"
        return User.objects.all()


class Mutation(graphene.ObjectType):
    register = RegisterUserMutation.Field()
    logout = LogoutUserMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
