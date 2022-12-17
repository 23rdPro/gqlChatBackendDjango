import graphene
from asgiref.sync import async_to_sync
# from channels.auth import login, logout
from django.contrib.auth import get_user_model, logout
from graphql_jwt.shortcuts import get_token, create_refresh_token
from ..types import UserType

User = get_user_model()


class RegisterUserMutation(graphene.Mutation):
    token = graphene.String()
    user = graphene.Field(UserType)
    refresh_token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    @staticmethod
    def mutate(root, info, username, password, email):
        instance = User(username=username, email=email)
        instance.set_password(password)
        instance.save()
        instance.is_active = True
        token = get_token(instance)
        refresh_token = create_refresh_token(instance)
        return RegisterUserMutation(
            user=instance,
            token=token,
            refresh_token=refresh_token
        )


class LogoutUserMutation(graphene.Mutation):
    logged_out = graphene.Boolean(required=True)

    class Arguments:
        pass

    @staticmethod
    def mutate(root, info):
        assert info.context.user.is_authenticated, \
            "Something went wrong.."
        async_to_sync(logout(info.context))
        if info.context.user.is_authenticated:
            return LogoutUserMutation(logged_out=False)
        return LogoutUserMutation(logged_out=True)
