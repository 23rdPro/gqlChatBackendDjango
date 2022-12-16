import channels_graphql_ws
from .schema import schema


class ChatConsumer(channels_graphql_ws.GraphqlWsConsumer):
    schema = schema
    # send_keepalive_every = 1
