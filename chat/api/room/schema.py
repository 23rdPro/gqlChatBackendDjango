import graphene
from django.contrib.auth import get_user_model
from ..types import RoomType
from chat.models import Room
from .mutation import RoomMutation
# from .subscriptions import OnNewMessageSubscription

User = get_user_model()


class Query(graphene.ObjectType):
    room = graphene.Field(RoomType, id=graphene.String())
    rooms = graphene.List(RoomType)

    @staticmethod
    def resolve_room(root, info, **kwargs):
        uid = kwargs.get('id')
        return Room.objects.get(id=uid)

    @staticmethod
    def resolve_rooms(root, info, **kwargs):
        return Room.objects.all()


class Mutation(graphene.ObjectType):
    mutate_room = RoomMutation.Field()


class Subscription(graphene.ObjectType):
    pass
    # on_new_message = OnNewMessageSubscription.Field()


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    # subscription=Subscription
)
