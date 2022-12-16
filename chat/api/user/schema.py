import graphene
from django.contrib.auth import get_user_model
from ..types import UserType
from graphql_jwt.shortcuts import (
    get_token,
    create_refresh_token
)
from .mutations import (
    RegisterUserMutation,
    UserLoginMutation,
    LogoutUserMutation
)


User = get_user_model()


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType)

    @staticmethod
    def resolve_user(root, info, **kwargs):
        assert info.context.user.is_authenticated(), \
            "User must be authenticated"
        return info.context.user

    @staticmethod
    def resolve_users(self, info, queryset, **kwargs):
        assert info.context.user.is_authenticated(), \
            "User must be authenticated"
        return queryset  # todo


class Mutation(graphene.ObjectType):
    register = RegisterUserMutation.Field()
    login = UserLoginMutation.Field()
    logout = LogoutUserMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)


# class AuthMutation(graphene.ObjectType):
#     register = relay.Register.Field()
#     verify_account = relay.VerifyAccount.Field()


# class VerifyAccountMutation(graphene.Mutation):  # by email
#     class Arguments:
#         token = graphene.String(required=True)
#
#     token = graphene.String()
#
#     def mutate(self, info, **kwargs):
#         token = kwargs.get("token")
#         u = user
#
# class Query(UserQuery, MeQuery, graphene.ObjectType):
#     pass
#
#
# class Mutation(graphene.ObjectType):
#     pass
#     # create_user = CreateUserMutation.Field()
#
#
# schema = graphene.Schema(query=Query, mutation=Mutation)



# class CreateUser(graphene.Mutation):
#     user = graphene.Field(UserType)
#     token = graphene.String()
#     refresh_token = graphene.String()
#
#     class Arguments:
#         username = graphene.String(required=True)
#         password = graphene.String(required=True)
#         email = graphene.String(required=True)
#
#     def mutate(self, info, username, password, email):
#         u = user(username=username, email=email)
#         u.set_password(password)
#         u.save()
#         token = get_token(u)
#         refresh_token = create_refresh_token(u)
#         return CreateUser(user=user, token=token, refresh_token=refresh_token)


# class AuthMutation(graphene.ObjectType):
#     register = mutations.Register.Field()
# verify_account = mutations.VerifyAccount.Field()
# resend_activation_email = mutations.ResendActivationEmail.Field()
# send_password_reset_email = mutations.SendPasswordResetEmail.Field()
# password_reset = mutations.PasswordReset.Field()
# password_set = mutations.PasswordReset.Field()
# password_change = mutations.PasswordChange.Field()
# update_account = mutations.UpdateAccount.Field()
# archive_account = mutations.ArchiveAccount.Field()
# delete_account = mutations.DeleteAccount.Field()
# send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
# verify_secondary_email = mutations.VerifySecondaryEmail.Field()
# swap_emails = mutations.SwapEmails.Field()
# remove_secondary_email = mutations.RemoveSecondaryEmail.Field()

# token_auth = mutations.ObtainJSONWebToken.Field()
# verify_token = mutations.VerifyToken.Field()
# refresh_token = mutations.RefreshToken.Field()
# revoke_token = mutations.RevokeToken.Field()


# class Query(graphene.ObjectType):
#     # pass
#     me = graphene.Field(UserType)
#     users = graphene.List(UserType)
#
#     def resolve_me(self, info):
#         u = info.context.user
#         if u.is_anonymous:
#             raise Exception("Authentication Failure: Your must be signed in")
#         return u
#
#     def resolve_users(self, info):
#         u = info.context.user
#         # if u.is_anonymous:
#         #     raise Exception("Authentication Failure: Your must be signed in")
#         return user.objects.all()

