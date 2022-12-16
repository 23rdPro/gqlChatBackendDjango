import graphene
from asgiref.sync import async_to_sync
from channels.auth import login, logout
from django.contrib.auth import get_user_model, authenticate
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
        token = get_token(instance)
        refresh_token = create_refresh_token(instance)
        return RegisterUserMutation(
            user=instance,
            token=token,
            refresh_token=refresh_token
        )


class UserLoginMutation(graphene.Mutation):
    verify_token = graphene.String()
    refresh_token = graphene.String()
    user = graphene.Field(UserType)
    logged_in = graphene.Boolean(required=True)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    @staticmethod
    def mutate(root, info, username, password):
        assert info.context.user is None, \
            "User has not been authenticated yet"
        user = authenticate(username=username, password=password)
        if user is None:
            return UserLoginMutation(logged_in=False)
        async_to_sync(login(info.context._asdict(), user))
        info.context.session.save()
        return UserLoginMutation(
            logged_in=True,
            verify_token=get_token(user),
            refresh_token=create_refresh_token(user),
            user=user
        )


class LogoutUserMutation(graphene.Mutation):
    logged_out = graphene.Boolean(required=True)

    class Arguments:
        pass

    @staticmethod
    def mutate(root, info):
        assert info.context.user.is_authenticated(), \
            "Something went wrong.."
        logout(info.context._asdict())
        if info.context.user.is_authenticated():
            return LogoutUserMutation(logged_in=False)
        return LogoutUserMutation(logged_out=True)
