import graphene
import graphql_jwt

from django.db.models import Q
from .types import NotificationType
from notifications.models import Notification
from .user.schema import (
    Query as UserQuery,
    Mutation as UserMutation
)

from .room.schema import (
    Query as RoomQuery,
    Mutation as RoomMutation,
    Subscription as RoomMessageSubscription,
)


class Query(
    UserQuery,
    RoomQuery,
    graphene.ObjectType
):
    notifications = graphene.List(NotificationType)

    @staticmethod
    def resolve_notifications(root, info, **kwargs):
        user = info.context.user.username
        return Notification.objects.filter(
            Q(actor=user) | Q(recipient=user)
        )


class Mutation(
    UserMutation,
    RoomMutation,
    graphene.ObjectType
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Subscription(
    RoomMessageSubscription,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription
)
